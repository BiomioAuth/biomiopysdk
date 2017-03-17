CONNECT = "biomio::client::connect"
DISCONNECT = "biomio::client::disconnect"
RESOURCE_REQUEST = "biomio::client::resource_request"
TRY_REQUEST = "biomio::client::try_request"
REPEAT_REQUEST = "biomio::client::repeat_request"
CLIENT_ERROR = "biomio::client::client_error"
REQUEST_TYPE_LIST = [CONNECT, DISCONNECT, RESOURCE_REQUEST, TRY_REQUEST, CLIENT_ERROR]


class BaseClient(object):
    """
    Base class for BiomioClient which provides backend methods for communication and
    callback mechanism support.
    """
    def __init__(self):
        self._is_connected = False
        self._registered_callbacks = {}
        self._messaging_api = None
        self._received_messages = {
            'bye': self._receive_bye,
            'try': self._receive_try,
            'getResources': self._receive_resource,
            'again': self._receive_repeat
        }
        self._additional_messages = {}
        self._temp_callback = None

    def _handle_request(self, request):
        if request:
            receiver = self._received_messages.get(request.msg.oid, None)
            if receiver is not None:
                request_type, data = receiver(request)
                self._call_callback(request_type, **data)
            else:
                self._additional_callback(request)

    def _call_callback(self, request_type, **kwargs):
        callback = self._registered_callbacks.get(request_type, None)
        if callback is not None:
            callback(kwargs)

    def _receive_bye(self, request):
        self._is_connected = request.msg.oid != "bye"
        res = {'connected': self._is_connected, 'status': request.status}
        if not self._is_connected:
            self._messaging_api.clear_session_token()
        if self._temp_callback is not None:
            self._temp_callback(res)
            self._temp_callback = None
        return DISCONNECT, res

    def _receive_try(self, request):
        req = {'msg': request.msg, 'callback': self._try_callback}
        return TRY_REQUEST, req

    def _receive_resource(self, request):
        req = {'callback': self._resource_callback}
        return RESOURCE_REQUEST, req

    def _receive_repeat(self, request):
        self._messaging_api.repeat()
        return None, {}

    def _additional_callback(self, request):
        if request:
            callback = self._additional_messages.get(request.msg.oid, None)
            if callback is not None:
                callback(request)

    def _try_callback(self, **kwargs):
        self._messaging_api.probe_response(**kwargs)

    def _resource_callback(self, **kwargs):
        self._messaging_api.resources(**kwargs)
