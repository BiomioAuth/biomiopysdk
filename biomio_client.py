from coreapi.biomio_messaging_api import BiomioMessagingAPI
from threading import Timer


CONNECT = "biomio::client::connect"
DISCONNECT = "biomio::client::disconnect"
RESOURCE_REQUEST = "biomio::client::resource_request"
TRY_REQUEST = "biomio::client::try_request"
REPEAT_REQUEST = "biomio::client::repeat_request"
CLIENT_ERROR = "biomio::client::client_error"
REQUEST_TYPE_LIST = [CONNECT, DISCONNECT, RESOURCE_REQUEST, TRY_REQUEST, REPEAT_REQUEST, CLIENT_ERROR]


class BiomioClient(object):
    def __init__(self, private_key, app_type, app_id=None, os_id='', dev_id='', auto_receiving=False, timeout=0):
        self._private_key = private_key
        self._is_connected = False
        self._registered_callbacks = {}
        self._auto_receiving = auto_receiving
        self._timer = None
        self._timeout = timeout
        self._messaging_api = BiomioMessagingAPI(app_type=app_type, app_id=app_id, os_id=os_id, dev_id=dev_id)
        self._received_messages = {
            'bye': self._receive_bye,
            'try': self._receive_try,
            'getResources': self._receive_resource
        }

    def connect(self, callback=None):
        self._is_connected = self._messaging_api.handshake(self._private_key)
        res = {'connected': self._is_connected}
        if callback is not None:
            callback(res)
        self._call_callback(CONNECT, **res)
        if self._auto_receiving:
            self._timer = Timer(self._timeout, self.receive, ())
            self._timer.start()

    def disconnect(self, callback=None):
        print "disconnect"
        self._is_connected = not self._messaging_api.close()
        res = {'connected': self._is_connected}
        if callback is not None:
            callback(res)
        self._call_callback(DISCONNECT, **res)
        if self._auto_receiving:
            self._timer.cancel()

    def is_connected(self):
        return self._is_connected

    def register(self, request_type, callback):
        if REQUEST_TYPE_LIST.__contains__(request_type) and callback is not None:
            self._registered_callbacks[request_type] = callback
            return True
        return False

    def request(self, session_id, on_behalf_of, namespace, call, data, callback):
        response = self._messaging_api.rpc_request(session_id=session_id, on_behalf_of=on_behalf_of,
                                                   namespace=namespace, call=call, data=data)
        if callback is not None:
            callback(response)

    def enum_ns_request(self, callback):
        response = self._messaging_api.rpc_enum_ns_request()
        if callback is not None:
            callback(response)

    def enum_calls_request(self, ns, callback):
        response = self._messaging_api.rpc_enum_calls_request(ns)
        if callback is not None:
            callback(response)

    def _call_callback(self, request_type, **kwargs):
        callback = self._registered_callbacks.get(request_type, None)
        print callback, request_type, kwargs
        if callback is not None:
            callback(kwargs)

    def receive(self):
        request = self._messaging_api.receive()
        if request:
            receiver = self._received_messages.get(request.msg.oid, None)
            if receiver is not None:
                request_type, data = receiver(request)
                self._call_callback(request_type, **data)
            else:
                print request, dict(request)
        self._messaging_api.nop()
        if self._auto_receiving:
            self._timer = Timer(self._timeout, self.receive, ())
            self._timer.start()

    def _receive_bye(self, request):
        self._is_connected = False
        res = {'connected': self._is_connected}
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

    def _try_callback(self, data):
        self._messaging_api.probe_response(**data)

    def _resource_callback(self, data):
        self._messaging_api.resources(data)

    def probe(self, data):
        self._try_callback(data)

    def resources(self, data):
        self._resource_callback(data)
