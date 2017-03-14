from base_client import BaseClient, CONNECT, REQUEST_TYPE_LIST
from coreapi.biomio_messaging_api import BiomioMessagingAPI


class BiomioClient(BaseClient):
    """
    Communication class with provide client-side communication interface.

    Usage::

        >>> from BiomioPySDK import BiomioClient
        >>> private_key = "..."
        >>> app_id = "..."
        >>> client = BiomioClient(private_key, app_type="probe", app_id=app_id, os_id="web")
        >>> client.connect()
        >>> ...
        >>> client.disconnect()

    Parameters:
        private_key: str
            RSA Private Key.
        app_type: str
            Type of client application.
        app_id: str
            Identifier of client application.
        os_id: str
            Operation System identifier. Default is ''.
        dev_id: str
            Developer identifier. Default is ''.
            Note: Uses only for some kind of client application.
    """
    def __init__(self, host, port, private_key, app_type, app_id=None, os_id='', dev_id=''):
        BaseClient.__init__(self)
        self._private_key = private_key
        self._messaging_api = BiomioMessagingAPI(host=host, port=port, app_type=app_type, app_id=app_id,
                                                 os_id=os_id, dev_id=dev_id)

    def connect(self, callback=None):
        """
        Connect client to the server.

        Start regular handshake and connect client to the server. If ``callback`` isn't None or
        ``CONNECT`` callback is registered call them with connection status.

        :param callback: The reference on callback function.
        """
        self._is_connected = self._messaging_api.handshake(self._private_key)
        res = {'connected': self._is_connected}
        if callback is not None:
            callback(res)
        self._call_callback(CONNECT, **res)

    def disconnect(self, callback=None):
        """
        Disconnect client from the server.

        Close connection with the server. If ``callback`` isn't None or ``DISCONNECT`` callback is
        registered call them with connection status.

        :param callback: The reference on callback function.
        """
        if self._is_connected:
            self._temp_callback = callback
            self._messaging_api.bye()

    def is_connected(self):
        """Return connection status."""
        return self._is_connected

    def register(self, request_type, callback):
        if REQUEST_TYPE_LIST.__contains__(request_type) and callback is not None:
            self._registered_callbacks[request_type] = callback
            return True
        return False

    def request(self, session_id, on_behalf_of, namespace, call, data, callback):
        if callback is not None:
            self._additional_messages['rpcResp'] = callback
        self._messaging_api.rpc_request(session_id=session_id, on_behalf_of=on_behalf_of,
                                        namespace=namespace, call=call, data=data)

    def enum_ns_request(self, callback):
        if callback is not None:
            self._additional_messages['rpcEnumNsResp'] = callback
        self._messaging_api.rpc_enum_ns_request()

    def enum_calls_request(self, ns, callback):
        if callback is not None:
            self._additional_messages['rpcEnumCallsResp'] = callback
        self._messaging_api.rpc_enum_calls_request(ns)

    def receive(self):
        request = self._messaging_api.select()
        self._handle_request(request)

    def run(self):
        if not self._is_connected:
            self.connect()
        while self._is_connected:
            request = self._messaging_api.select(3)
            self._handle_request(request)
            if self._is_connected and request is None:
                self._messaging_api.nop()

    def probe(self, try_id, try_type, probe_status, probe_data=None):
        self._messaging_api.probe_response(try_id, try_type, probe_status, probe_data)

    def resources(self, data, push_token=None):
        self._messaging_api.resources(data, push_token)

    def last_request(self):
        return self._messaging_api.last_sent_message()

    def last_response(self):
        return self._messaging_api.last_read_message()
