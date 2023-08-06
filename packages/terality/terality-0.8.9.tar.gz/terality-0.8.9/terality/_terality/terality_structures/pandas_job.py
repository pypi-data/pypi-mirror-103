from typing import Optional, Any

from terality_serde import apply_func_on_object_recursively
from common_client_scheduler import (
    ComputationResponse, PendingComputationResponse, PandasFunctionRequest, TeralityInternalError
)

# from terality.exceptions import TeralityNotFoundError
from .. import Connection, encode, decode


def call_pandas_function(function_type: str, function_prefix: Optional[str], function_name: str,
                         *args, **kwargs) -> Any:
    args = [] if args is None else args
    args_encoded = apply_func_on_object_recursively(args, encode)
    kwargs = {} if kwargs is None else kwargs
    kwargs_encoded = apply_func_on_object_recursively(kwargs, encode)
    job = PandasFunctionRequest(function_type=function_type, function_accessor=function_prefix,
                                function_name=function_name, args=args_encoded, kwargs=kwargs_encoded)
    response = Connection.send_request('compute', job)

    # remaining_retries = 1

    # Poll the server until the result is available.
    while isinstance(response, PendingComputationResponse):
        function_id = response.pending_computation_id
        # try:
        response = Connection.send_request('follow_up', {'function_id': function_id})
        # except TeralityNotFoundError as e:
        #     # The server somehow lost the result of the job (this may be due to an internal server error).
        #     # To retry, we need to call /compute again.
        #     if remaining_retries <= 0:
        #         # This is really a server error (we know our client is OK),
        #         # so transform the exception appropriately.
        #         raise TeralityInternalError(f"Could not get results of job '{function_id}'") from e
        #     response = Connection.send_request('compute', job)
        #     remaining_retries = remaining_retries - 1

    if isinstance(response, ComputationResponse):
        result = response.result
        result = apply_func_on_object_recursively(result, decode)

        # Handle in-place modification of data structures.
        # NOTE: Because `inplace` is only available on methods, the first argument is guaranteed to be positional
        # (`self`).
        if response.inplace:
            from terality._terality.terality_structures.structure import Struct  # break cyclic import
            if not isinstance(args[0], Struct):
                raise TeralityInternalError('Received in-place response but the target is not a data structure')
            target = args[0]
            if not isinstance(result, Struct):
                raise TeralityInternalError('Received in-place response but the result is not a data structure')
            # noinspection PyProtectedMember
            target._assign(result)
            result = None
        return result

    raise TeralityInternalError(f'Received unexpected response {response}')
