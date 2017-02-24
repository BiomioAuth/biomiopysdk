from coreapi.biomio_messaging_api import BiomioMessagingAPI
from threading import Timer


CONNECT = "biomio::client::connect"
DISCONNECT = "biomio::client::disconnect"
RESOURCE_REQUEST = "biomio::client::resource_request"
TRY_REQUEST = "biomio::client::try_request"
CLIENT_ERROR = "biomio::client::client_error"
REQUEST_TYPE_LIST = [CONNECT, DISCONNECT, RESOURCE_REQUEST, TRY_REQUEST, CLIENT_ERROR]


class BiomioClient(object):
    def __init__(self, private_key, auto_receiving=False, timeout=0):
        self._private_key = private_key
        self._is_connected = False
        self._registered_callbacks = {}
        self._auto_receiving = auto_receiving
        self._timer = None
        if self._auto_receiving:
            self._timer = Timer(timeout, self.receive, ())
        self._messaging_api = BiomioMessagingAPI()
        self._received_messages = {
            'bye': self._receive_bye,
            'try': self._receive_try,
            'getResources': self._receive_resource,

        }

    def connect(self, callback=None):
        self._is_connected = self._messaging_api.handshake(self._private_key)
        res = {'connected': self._is_connected}
        if callback is not None:
            callback(res)
        self._call_callback(CONNECT, res)
        if self._auto_receiving:
            self._timer.start()

    def disconnect(self, callback=None):
        self._is_connected = not self._messaging_api.close()
        res = {'connected': self._is_connected}
        if callback is not None:
            callback(res)
        self._call_callback(DISCONNECT, res)
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
        if callback is not None:
            callback(**kwargs)

    def receive(self):
        request = self._messaging_api.receive()
        receiver = self._received_messages.get(request.header.oid, None)
        if receiver is not None:
            request_type, data = receiver(request)
            self._call_callback(request_type, data)
        if self._auto_receiving:
            self._timer.start()

    def _receive_bye(self, request):
        self._is_connected = False
        return DISCONNECT, {}
