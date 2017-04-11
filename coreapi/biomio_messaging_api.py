from base_messaging_api import BaseMessagingAPI
from message import BiomioMessageBuilder


MODE_SERVER_API = "api::server"
MODE_CLIENT_API = "api::client"


class BiomioMessagingAPI(BaseMessagingAPI):
    """
    Biomio messaging application programming interface for sending and receiving messages.

    Class implements Biomio Protocol and provides low-level API for sending and receiving Biomio Protocol messages.

    :param str host: Biomio back-end address.
    :param str port: Biomio back-end port number.
    :param str app_type: Type of client application (e.g. "extension", "probe").
    :param str app_id: Identifier of client application.
    :param str os_id: Operation System identifier. Default is ''.
    :param str dev_id: Developer identifier. Default is ''. Note: Uses only for some kind of client application.
    :param enum mode: Message generation mode. Available modes: MODE_CLIENT_API and MODE_SERVER_API. Default is
    MODE_CLIENT_API.
    """
    def __init__(self, host, port, app_type, app_id, os_id='', dev_id='', mode=MODE_CLIENT_API):
        BaseMessagingAPI.__init__(self, host=host, port=port)
        self._mode = mode
        self._create_builder(app_type, app_id, os_id, dev_id)

    def _create_builder(self, app_type, app_id, os_id, dev_id):
        header = {'protoVer': '1.0', 'osId': os_id, 'devId': dev_id, 'appType': app_type}
        if app_id:
            header.update(appId=app_id)
        if self._mode == MODE_CLIENT_API:
            header.update({'oid': 'clientHeader', 'seq': 0})
        elif self._mode == MODE_SERVER_API:
            header.update({'oid': 'serverHeader', 'seq': 1})
        self._builder = BiomioMessageBuilder(**header)

    def nop(self):
        """
        Biomio Protocol ``nop`` message sender.

        Create ``nop`` message and send it. About ``nop`` message see Biomio Protocol Documentation.
        """
        message = self._builder.create_message(oid='nop')
        self._send_message(websocket=self._get_curr_connection(), message=message, wait_for_response=False)

    def ack(self):
        """
        Biomio Protocol ``ack`` message sender.

        Create ``ack`` message and send it. About ``ack`` message see Biomio Protocol Documentation.
        """
        message = self._builder.create_message(oid='ack')
        self._send_message(websocket=self._get_curr_connection(), message=message, wait_for_response=False)

    def bye(self):
        """
        Biomio Protocol ``bye`` message sender.

        Create ``bye`` message and send it. About ``bye`` message see Biomio Protocol Documentation.
        """
        message = self._builder.create_message(oid='bye')
        return self._send_message(websocket=self._get_curr_connection(), message=message, wait_for_response=False)

    def again(self):
        """
        Biomio Protocol ``again`` message sender.

        Create ``again`` message and send it. About ``again`` message see Biomio Protocol Documentation.
        """
        message = self._builder.create_message(oid='again')
        self._send_message(websocket=self._get_curr_connection(), message=message, wait_for_response=False)

    def get_resources(self):
        """
        Biomio Protocol ``getResources`` message sender.

        Create ``getResources`` message and send it. About ``getResources`` message see Biomio Protocol Documentation.
        """
        message = self._builder.create_message(oid='getResources')
        self._send_message(websocket=self._get_curr_connection(), message=message, wait_for_response=False)

    def resources(self, data, push_token=None):
        """
        Biomio Protocol ``resources`` message sender.

        Create ``resources`` message and send it. About ``resources`` message see Biomio Protocol Documentation.

        :param list data: A list of dictionary with resource description.
        :param str push_token: Push Notification Token for probe client device (for example,
        APNs Token on iOS devices).
        """
        body = {'oid': 'resources', 'data': data}
        if push_token is not None:
            body.update(push_token=push_token)
        message = self._builder.create_message(**body)
        self._send_message(websocket=self._get_curr_connection(), message=message, wait_for_response=False)

    def try_request(self, try_id, auth_timeout, policy=None, try_info=None, resource=None, message=None):
        """
        Biomio Protocol ``try`` message sender.

        Create ``try`` message and send it. About ``try`` message see Biomio Protocol Documentation.

        :param str try_id: A try request identifier.
        :param int auth_timeout:
        :param dict policy:
        :param try_info:
        :param resource:
        :param message:
        """
        body = {'oid': 'try', 'try_id': try_id, 'auth_timeout': auth_timeout}
        if policy is not None:
            body.update(policy=policy)
        if try_info is not None:
            body.update(try_info=try_info)
        if resource is not None:
            body.update(resource=resource)
        if message is not None:
            body.update(message=message)
        message = self._builder.create_message(**body)
        self._send_message(websocket=self._get_curr_connection(), message=message, wait_for_response=False)

    def probe_response(self, try_id, try_type, probe_status, probe_data=None):
        """
        Biomio Protocol ``probe`` message sender.

        Create ``probe`` message and send it. About ``probe`` message see Biomio Protocol Documentation.

        :param str try_id: A try request identifier.
        :param str try_type: A try request type.
        :param str probe_status: A result of try request.
        :param dict probe_data: A try required data. Default is ``None``.
        """
        body = {'oid': 'probe', 'try_id': try_id, 'tType': try_type, 'probeStatus': probe_status}
        if probe_data is not None:
            body.update(probeData=probe_data)
        message = self._builder.create_message(**body)
        self._send_message(websocket=self._get_curr_connection(), message=message, wait_for_response=False)

    def hello(self, **kwargs):
        """
        Biomio Protocol ``clientHello`` or ``serverHello`` message sender.

        Create ``clientHello`` or ``serverHello`` message and send it. Type of sent message depends on ``mode``
        of Biomio Messaging API. About ``clientHello`` or ``serverHello`` message see Biomio Protocol Documentation.

        :param dict kwargs: A message data.
        :return: The response message.
        """
        body = kwargs.copy()
        if self._mode == MODE_CLIENT_API:
            body['oid'] = 'clientHello'
        elif self._mode == MODE_SERVER_API:
            body['oid'] = 'serverHello'
        message = self._builder.create_message(**body)
        response = self._send_message(websocket=self._get_curr_connection(), message=message)
        self._check_tokens(response, oid='serverHello')
        return response

    def auth(self, **kwargs):
        """
        Biomio Protocol ``auth`` message sender.

        Create ``auth`` message and send it. About ``auth`` message see Biomio Protocol Documentation.

        :param dict kwargs: A message data.
        :return:
        """
        body = kwargs.copy()
        body.update(oid='auth')
        message = self._builder.create_message(**body)
        self._send_message(websocket=self._get_curr_connection(), message=message, wait_for_response=False)

    def rpc_request(self, session_id, on_behalf_of, namespace, call, data={}):
        """
        Biomio Protocol ``rpcReq`` message sender.

        Create ``rpcReq`` message and send it. About ``rpcReq`` message see Biomio Protocol Documentation.

        :param str session_id: The session identifier.
        :param str on_behalf_of: The client identifier.
        :param str namespace: The namespace name.
        :param str call: The name of the callable function from ``namespace``.
        :param dict data: Request data dictionary.
        """
        message = self._builder.create_message(oid='rpcReq', session_id=session_id, onBehalfOf=on_behalf_of,
                                               namespace=namespace, call=call, data=data)
        self._send_message(websocket=self._get_curr_connection(), message=message, wait_for_response=False)

    def rpc_enum_ns_request(self):
        """
        Biomio Protocol ``rpcEnumNsReq`` message sender.

        Create ``rpcEnumNsReq`` message and send it. About ``rpcEnumNsReq`` message see Biomio Protocol Documentation.
        """
        message = self._builder.create_message(oid='rpcEnumNsReq')
        self._send_message(websocket=self._get_curr_connection(), message=message, wait_for_response=False)

    def rpc_enum_calls_request(self, ns):
        """
        Biomio Protocol ``rpcEnumCallsReq`` message sender.

        Create ``rpcEnumCallsReq`` message and send it. About ``rpcEnumCallsReq`` message see
        Biomio Protocol Documentation.

        :param str ns: The namespace name.
        """
        message = self._builder.create_message(oid='rpcEnumCallsReq', ns=ns)
        self._send_message(websocket=self._get_curr_connection(), message=message, wait_for_response=False)

    def handshake(self, private_key, **kwargs):
        """
        Regular handshake for Biomio Authentication Flow.

        Implement regular handshake for Biomio Authentication Flow. About regular handshake see
        Biomio Protocol Documentation.
        If regular handshake is successful, returns ``True``. Otherwise, returns ``False``.

        :param str private_key: RSA private key.
        :param dict kwargs: A message data.
        :return: The regular handshake status.
        :rtype: boolean
        """
        response = self.hello(**kwargs)
        print dict(response)
        if response and response.msg.oid == 'serverHello':
            self.auth(key=self._get_digest_for_next_message(private_key=private_key))
            return True
        return False

    def repeat(self):
        """Re-send the last message sent."""
        self._send_message(message=self._last_sent_message, websocket=self._get_curr_connection(),
                           wait_for_response=False)

    def last_sent_message(self):
        """Return last sent message."""
        return self._last_sent_message

    def last_read_message(self):
        """Return last read message."""
        return self._last_read_message
