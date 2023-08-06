import base64
from io import BytesIO
import json
from typing import List, Tuple

import dill
import numpy as np
import pandas as pd

from terality_serde import CallableWrapper
from common_client_scheduler import (
    StructRef, IndexColNames, PandasIndexMetadata, PandasSeriesMetadata, PandasDFMetadata
)
from .. import Connection, DataTransfer


def _serialize_ndarray(array: np.ndarray) -> str:
    data_bytes = BytesIO()
    # noinspection PyTypeChecker
    np.save(data_bytes, array)
    import_id = DataTransfer.upload_bytes(Connection.session.upload_config, data_bytes)
    return import_id


def _check_if_col_needs_json_encoding(col: pd.Series) -> bool:
    if isinstance(col.dtype, np.dtype) and col.dtype.hasobject:
        # Collect the types of all values in the column.
        dtypes = set()
        for value in col:
            dtypes.add(type(value))
        # Ignore absent values: they are gracefully handled by the Parquet format.
        dtypes -= {type(None)}

        # Based on the combination of types, decide if we need to JSON-encode.
        need_json = len(dtypes) > 1 or any(dtype in dtypes for dtype in [list, dict])
        return need_json
    return False


def _prepare_for_parquet(df: pd.DataFrame) -> Tuple[pd.DataFrame, List[bool]]:
    is_col_json = []
    for col_num in range(len(df.columns)):
        col_needs_json = _check_if_col_needs_json_encoding(df.iloc[:, col_num])
        if col_needs_json:
            df.iloc[:, col_num] = df.iloc[:, col_num].apply(json.dumps)
        is_col_json.append(col_needs_json)
    return df, is_col_json


def _upload_df(df: pd.DataFrame) -> Tuple[str, List[bool]]:
    """ Parquet only supports dataframes so we transmit all pandas structures as dataframes """
    # WARNING: Parquet only accepts string column names
    # => We replace non-string column names with placeholders and pass the columns "out of band" (in the metadata).
    df = df.rename(columns={df.columns[col_num]: str(col_num) for col_num in range(len(df.columns))}, copy=False)

    df, is_col_json = _prepare_for_parquet(df)
    row_group_size = _estimate_row_group_size(df, 1024 ** 3)

    data_bytes = BytesIO()
    df.to_parquet(data_bytes, version='2.0', row_group_size=row_group_size)
    import_id = DataTransfer.upload_bytes(Connection.session.upload_config, data_bytes)
    return import_id, is_col_json


def _estimate_row_group_size(df: pd.DataFrame, max_memory_per_row_group_bytes=1024**3) -> int:
    """Estimate the size of a parquet row group that can be processed in memory for this dataframe,
    index included.

    In other words, split the dataframe in row groups, each row group not exceeding
    `max_memory_per_row_group_bytes`, and return the size (in rows) of a row group.

    Server-side, we can only process parquet files by row group. We can not split a parquet file in the
    middle of a row group. This means that a whole uncompressed row group must fit in memory. In order to
    maximize parallelisation server-side, this function returns how many rows per row group the parquet file
    should contain.

    We still want this value to be as high as possible to improve compression and reduce the bandwidth
    used, but err on the side of caution - an incorrect split means we can't easily process the uploaded
    files (we risk returning memory errors, which would be unfortunate for Terality :) ).

    We also want this operation to be as fast as possible, so we don't use `memory_usage(deep=True)`, which
    is costly on big datasets. Instead, for columns with dtype = object, we take a guess based on a small
    sample and hope it covers all real-world usage. This function may fail on dataframes that have a wide
    distribution of object sizes.
    """
    # as a safety measure, never include more than this many rows per row group.
    # this should give us a safety net even if our memory usage estimation is wildly inaccurate.
    MAX_ROWS_PER_ROW_GROUP = 2_000_000_000

    memory_usage_bytes = _estimate_dataframe_memory_usage_bytes(df)
    rows_per_row_group = (len(df) * max_memory_per_row_group_bytes) // memory_usage_bytes

    return min(rows_per_row_group, MAX_ROWS_PER_ROW_GROUP)


def _estimate_dataframe_memory_usage_bytes(df: pd.DataFrame, max_samples_per_column: int = 500, random_state=None) -> int:
    """Estimate the memory usage of a DataFrame, in bytes.

    See _estimate_column_memory_usage_bytes for the difference with `memory_usage(deep=True)`.
    """
    # Get memory usage for all columns, except when dtype = object.
    memory_usage = df.memory_usage(deep=False)
    total_memory_bytes = 0
    for column, dtype in df.dtypes.iteritems():
        if dtype == "object":
            # Sample columns with dtype = object, and hope that our sample is representative.
            total_memory_bytes += _estimate_column_memory_usage_bytes(
                df, column, max_samples_per_column, random_state
            )
        else:
            total_memory_bytes += memory_usage[column]
    total_memory_bytes += memory_usage["Index"]
    return total_memory_bytes


def _estimate_column_memory_usage_bytes(df: pd.DataFrame, column: str, max_samples: int = 200, random_state=None) -> int:
    """Estimate the memory usage of a column in a DataFrame, in bytes.

    Unlike memory_usage(deep=True), this function samples rows and extrapolate the memory usage from these
    rows only. This makes it faster, but inaccurate.

    The sample is random, and thus the results of this function are not reproducible unless random_state is
    provided.
    """
    df_column: pd.Series = df[column]  # type: ignore
    samples_count: int = min(max_samples, len(df_column))  # type: ignore
    samples: pd.Series = df_column.sample(n=samples_count, random_state=random_state)  # type: ignore
    return samples.memory_usage(deep=True, index=False) / samples_count * len(df_column)  # type: ignore


def _make_index_col_names(index: pd.Index) -> IndexColNames:
    return IndexColNames(names=list(index.names), name=index.name)


def _serialize_index(index: pd.Index) -> PandasIndexMetadata:
    transfer_id, is_col_json = _upload_df(index.to_frame(index=False))
    return PandasIndexMetadata(
            transfer_id=transfer_id,
            cols_json_encoded=is_col_json,
            index_col_names=_make_index_col_names(index)
        )


def _serialize_series(series: pd.Series) -> PandasSeriesMetadata:
    transfer_id, is_col_json = _upload_df(series.copy(deep=True).to_frame())
    return PandasSeriesMetadata(
        transfer_id=transfer_id,
        cols_json_encoded=is_col_json,
        index_col_names=_make_index_col_names(series.index),
        series_name=series.name
    )


def _serialize_df(df: pd.DataFrame) -> PandasDFMetadata:
    transfer_id, is_col_json = _upload_df(df.copy(deep=True))
    return PandasDFMetadata(
        transfer_id=transfer_id,
        cols_json_encoded=is_col_json,
        index_col_names=_make_index_col_names(df.index),
        col_names=list(df.columns)
    )


encoder = {
    np.ndarray: _serialize_ndarray,
    pd.Index: _serialize_index,
    pd.Series: _serialize_series,
    pd.DataFrame: _serialize_df,
}


def encode(o):
    from terality import Index, Series, DataFrame  # Avoid circular dependencies
    from terality._terality.terality_structures import DataFrameGroupBy
    if isinstance(o, (Index, Series, DataFrame, DataFrameGroupBy)):
        # noinspection PyProtectedMember
        return StructRef(id=o._id, type=o._class_name)
    if type(o) in encoder:
        return encoder[type(o)](o)
    elif callable(o) and not isinstance(o, type):  # avoid types, which are also callables
        return CallableWrapper(dill_payload=base64.b64encode(dill.dumps(o)).decode())
    else:
        return o
