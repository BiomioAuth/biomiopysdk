CONNECT = "biomio::client::connect"
DISCONNECT = "biomio::client::disconnect"
RESOURCE_REQUEST = "biomio::client::resource_request"
TRY_REQUEST = "biomio::client::try_request"
REPEAT_REQUEST = "biomio::client::repeat_request"
CLIENT_ERROR = "biomio::client::client_error"
REQUEST_TYPE_LIST = [CONNECT, DISCONNECT, RESOURCE_REQUEST, TRY_REQUEST, REPEAT_REQUEST, CLIENT_ERROR]


class BaseClient(object):
    def __init__(self):
        self._is_connected = False
        self._registered_callbacks = {}
        self._messaging_api = None
        self._received_messages = {
            'bye': self._receive_bye,
            'try': self._receive_try,
            'getResources': self._receive_resource
        }

    def _call_callback(self, request_type, **kwargs):
        callback = self._registered_callbacks.get(request_type, None)
        print callback, request_type, kwargs
        if callback is not None:
            callback(kwargs)

    def _receive_bye(self, request):
        self._is_connected = False
        res = {'connected': self._is_connected}
        # if self._auto_receiving:
        #     self._timer.cancel()
        return DISCONNECT, res

    def _receive_try(self, request):
        req = {'msg': request.msg, 'callback': self._try_callback}
        return TRY_REQUEST, req

    def _receive_resource(self, request):
        req = {'callback': self._resource_callback}
        return RESOURCE_REQUEST, req

    def _receive_repeat(self, request):
        self._messaging_api.repeat()
        return REPEAT_REQUEST, {}

    def _try_callback(self, **kwargs):
        self._messaging_api.probe_response(**kwargs)

    def _resource_callback(self, **kwargs):
        self._messaging_api.resources(**kwargs)
