from base_client import BaseClient, CONNECT, REQUEST_TYPE_LIST
from coreapi.biomio_messaging_api import BiomioMessagingAPI


class BiomioClient(BaseClient):
    """
    Communication class which provides client-side communication interface.

    Usage::

        >>> from biomiopysdk import BiomioClient, TRY_REQUEST
        >>>
        >>> def try_callback(request)
        >>>     ...
        >>>
        >>> private_key = "..."
        >>> app_id = "..."
        >>> client = BiomioClient(private_key, app_type="probe", app_id=app_id, os_id="web")
        >>> client.register(TRY_REQUEST, try_callback)
        >>> client.run()

    :param str host: Biomio back-end address.
    :param str port: Biomio back-end port number.
    :param str private_key: RSA Private Key.
    :param str app_type: Type of client application (e.g. "extension", "probe").
    :param str app_id: Identifier of client application.
    :param str os_id: Operation System identifier. Default is ''.
    :param str dev_id: Developer identifier. Default is ''. Note: Uses only for some kind of client application.
    """
    def __init__(self, host, port, private_key, app_type, app_id, os_id='', dev_id=''):
        BaseClient.__init__(self)
        self._private_key = private_key
        self._messaging_api = BiomioMessagingAPI(host=host, port=port, app_type=app_type, app_id=app_id,
                                                 os_id=os_id, dev_id=dev_id)

    def connect(self, callback=None):
        """
        Connect client to the server.

        Start regular handshake and connect client to the server. If ``callback`` isn't None or
        ``CONNECT`` callback is registered they are called with connection status.

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
        registered they are called with connection status.

        :param callback: The reference on callback function.
        """
        if self._is_connected:
            self._temp_callback = callback
            self._messaging_api.bye()

    def is_connected(self):
        """Return connection status."""
        return self._is_connected

    def register(self, request_type, callback):
        """
        Register callback function for some request type.

        Register ``callback`` function for given ``request_type``. If there already is a callback function
        registered, it will be replaced on given one.
        If a ``callback`` function is successfully registered, method returns True. Otherwise, the method
        returns False.

        :param str request_type: Available request type.
        :param callback callback: The reference on callback function.
        :return: The registration status.
        :rtype: boolean
        """
        if REQUEST_TYPE_LIST.__contains__(request_type) and callback is not None:
            self._registered_callbacks[request_type] = callback
            return True
        return False

    def request(self, session_id, on_behalf_of, namespace, call, data, callback):
        """
        Send RPC request to the server.

        Send RPC request to the server to call ``call`` function from given ``namespace`` with given ``data``.
        If ``callback`` isn't None, it's called with the request response.

        :param str session_id: The session identifier.
        :param str on_behalf_of: The client identifier.
        :param str namespace: The namespace name.
        :param str call: The name of the callable function from ``namespace``.
        :param dict data: Request data dictionary.
        :param callback callback: The reference on callback function.
        """
        if callback is not None:
            self._additional_messages['rpcResp'] = callback
        self._messaging_api.rpc_request(session_id=session_id, on_behalf_of=on_behalf_of,
                                        namespace=namespace, call=call, data=data)

    def enum_ns_request(self, callback):
        """
        Send RPC enum ns request to the server.

        Send RPC enum ns request to the server. If ``callback`` isn't None, it's called with the request response.

        :param callback callback: The reference on callback function.
        """
        if callback is not None:
            self._additional_messages['rpcEnumNsResp'] = callback
        self._messaging_api.rpc_enum_ns_request()

    def enum_calls_request(self, ns, callback):
        """
        Send RPC enum calls request to the server.

        Send RPC enum calls request to the server with given ``ns``. If ``callback`` isn't None, it's called
        with the request response.

        :param str ns: The namespace name.
        :param callback callback: The reference on callback function.
        """
        if callback is not None:
            self._additional_messages['rpcEnumCallsResp'] = callback
        self._messaging_api.rpc_enum_calls_request(ns)

    def receive(self):
        """
        Try to receive message from the server.

        Try to receive message from the server and if message is received, it calls the registered callback
        function.
        """
        request = self._messaging_api.select()
        self._handle_request(request)

    def run(self):
        """
        Run event loop for BiomioClient which listens websocket and processes received messages.

        Run event loop for BiomioClient which listens websocket and processes received messages. This event
        loop is alive during websocket keeps connection. If websocket was disconnected when event loop is
        started, it tries to connect to the server and if it's successfully connected, starts event loop.
        """
        if not self._is_connected:
            self.connect()
        while self._is_connected:
            request = self._messaging_api.select(3)
            self._handle_request(request)
            if self._is_connected and request is None:
                self._messaging_api.nop()

    def probe(self, try_id, try_type, probe_status, probe_data=None):
        """
        Try response. Send try required data to the server.

        :param str try_id: A try request identifier.
        :param str try_type: A try request type.
        :param str probe_status: A result of try request.
        :param dict probe_data: A try required data.
        """
        self._messaging_api.probe_response(try_id, try_type, probe_status, probe_data)

    def resources(self, data, push_token=None):
        """
        Resources response. Send resources data to the server.

        :param list data: A list of dictionary with resource description.
        :param str push_token: Push Notification Token for probe client device (for example,
               APNs Token on iOS devices).
        """
        self._messaging_api.resources(data, push_token)

    def last_request(self):
        """Return last client request message."""
        return self._messaging_api.last_sent_message()

    def last_response(self):
        """Return last server response message."""
        return self._messaging_api.last_read_message()
