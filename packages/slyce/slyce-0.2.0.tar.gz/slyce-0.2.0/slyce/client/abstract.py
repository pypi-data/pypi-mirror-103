import inspect

from abc import ABC
from datetime import datetime
from functools import reduce
from typing import Dict
from typing import List
from typing import Tuple

from google.rpc.error_details_pb2 import BadRequest
from google.protobuf.json_format import MessageToDict
from google.protobuf.struct_pb2 import Struct
from grpclib.client import Channel
from grpclib.exceptions import GRPCError
from grpclib.events import SendRequest
from grpclib.events import listen


from slyce.credentials import SlyceCredentials
from slyce.exception import InvalidCredentials
from slyce.exception import ExecuteWorkflowError
from slyce.exception import UploadImageError
from slyce.protobufgen.auth_grpc import AuthStub
from slyce.protobufgen.auth_pb2 import GetAuthTokenRequest
from slyce.protobufgen.common_pb2 import Point
from slyce.protobufgen.image_grpc import ImageStub
from slyce.protobufgen.image_pb2 import UploadImageRequest
from slyce.protobufgen.workflow_grpc import WorkflowStub
from slyce.protobufgen.workflow_pb2 import ExecuteWorkflowRequest


def inject_fingerprint(f):
    _, _, _, _, kwarg_names, _, _ = inspect.getfullargspec(f)

    def inner(self, *args, **kwargs):
        if 'fingerprint' in kwarg_names:
            try:
                kwargs['fingerprint'] = kwargs.get('fingerprint', self._fingerprint)
            except Exception:
                pass
        return f(self, *args, **kwargs)
    return inner


def decorate_all(decorator):
    def decorate(cls):
        for attr in cls.__dict__:
            if callable(getattr(cls, attr)):
                setattr(cls, attr, decorator(getattr(cls, attr)))
        return cls
    return decorate


@decorate_all(inject_fingerprint)
class AbstractSlyceClient(ABC):
    def __init__(self, credentials: SlyceCredentials, fingerprint: str = None):
        if not isinstance(credentials, SlyceCredentials):
            raise InvalidCredentials

        self._credentials = credentials
        self._fingerprint = fingerprint

        self._auth_token = None
        self._auth_token_expiry = None

        self._channel = Channel('forgex.slyce.it', 443, ssl=True)

        listen(self._channel, SendRequest, self._send_request)

    def __enter__(self):
        return self

    def __exit__(self, *args, **kwargs):
        self.close()

    async def _send_request(self, event):
        try:
            if event.method_name == '/Auth/GetAuthToken':
                return

            if not self._auth_token or self._auth_token_expiry - int(datetime.utcnow().timestamp() * 1000) < 30:
                stub = AuthStub(self._channel)
                async with stub.GetAuthToken.open() as stream:
                    await stream.send_message(GetAuthTokenRequest(
                        api_key=self._credentials.api_key,
                        account_id=self._credentials.account_id
                    ))
                    res = await stream.recv_message()
                    self._auth_token = res.token
                    self._auth_token_expiry = res.expiry

            event.metadata['auth-token'] = self._auth_token
        except Exception as e:
            print(e)

    def close(self):
        self._channel.close()

    async def _execute_workflow(self,
                                account_id: str,
                                space_id: str,
                                *,
                                workflow_id: str = None,
                                weld_statement: str = None,
                                image_id: str = None,
                                language_code: str = None,
                                country_code: str = None,
                                anchor: Tuple[int, int] = None,
                                roi: List[Tuple[int, int]] = None,
                                options: Dict = None,
                                fingerprint=None,
                                **_) -> Dict:

        try:
            workflow_options = Struct()
            workflow_options.update(options or {})

            request = ExecuteWorkflowRequest(
                account_id=account_id,
                space_id=space_id,
                image_id=image_id,
                fingerprint=fingerprint,
                language_code=language_code,
                country_code=country_code,
                workflow_options=workflow_options,
                anchor=Point(x=anchor[0], y=anchor[1]) if anchor else None,
                roi=[Point(x=p[0], y=p[1]) for p in roi] if roi else None
            )

            if workflow_id:
                request.workflow_id = workflow_id
                print(workflow_id)
            elif weld_statement:
                request.weld_statement = weld_statement

            stub = WorkflowStub(self._channel)

            res = await stub.ExecuteWorkflow(request)

            if res.errors:
                raise ExecuteWorkflowError(res.errors)

            data = MessageToDict(getattr(res, res.WhichOneof('data')), preserving_proto_field_name=True)
            data['results'] = data.get('results')
            return_value = MessageToDict(res, preserving_proto_field_name=True)
            return_value.pop('search_data', None)
            return_value.pop('classifier_data', None)
            return_value['data'] = data
            return return_value

        except GRPCError as e:
            if not e.details:
                raise Exception

            details = reduce(
                lambda res, detail: {
                    **res,
                    **{v.field: v.description for v in detail.field_violations}
                },
                [detail for detail in e.details if isinstance(detail, BadRequest)],
                {}
            )

            raise ExecuteWorkflowError(details)

        except ExecuteWorkflowError as e:
            raise e
        except Exception:
            raise ExecuteWorkflowError('An unknown error occured.')

    async def execute_workflow(self,
                               account_id: str,
                               space_id: str,
                               workflow_id: str,
                               *_,
                               **kwargs) -> Dict:
        kwargs['workflow_id'] = workflow_id
        return await self._execute_workflow(account_id, space_id, **kwargs)

    async def upload_image(self,
                           account_id: str,
                           filepath: str = None,
                           *,
                           url: str = None,
                           fingerprint: str = None,
                           **_) -> str:

        if not filepath and not url:
            raise ValueError("A 'filepath' or 'url' must be specified.")

        try:
            stub = ImageStub(self._channel)
            async with stub.UploadImage.open() as stream:
                if url:
                    await stream.send_message(
                        UploadImageRequest(
                            account_id=account_id,
                            fingerprint=fingerprint,
                            url=url
                        )
                    )
                else:
                    f = open(filepath, 'rb') if isinstance(filepath, str) else filepath
                    try:
                        while True:
                            data = f.read(1024 * 1024)

                            if not data:
                                break

                            await stream.send_message(UploadImageRequest(
                                account_id=account_id,
                                fingerprint=fingerprint,
                                data=data
                            ))
                    finally:
                        try:
                            f.close()
                        except Exception:
                            pass

                await stream.end()
                res = await stream.recv_message()
                return res.id
        except Exception as e:
            raise e
            if isinstance(e, UploadImageError):
                raise e
            if isinstance(e, FileNotFoundError):
                raise e
            raise UploadImageError('An unknown error occured.')
