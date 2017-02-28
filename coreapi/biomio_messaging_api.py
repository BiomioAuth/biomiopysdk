from base_messaging_api import BaseMessagingAPI
from message import BiomioMessageBuilder


MODE_SERVER_API = "api::server"
MODE_CLIENT_API = "api::client"


class BiomioMessagingAPI(BaseMessagingAPI):
    def __init__(self, app_type, app_id=None, os_id='', dev_id='', mode=MODE_CLIENT_API):
        BaseMessagingAPI.__init__(self)
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
        self._builder = BiomioMessageBuilder(header)

    def nop(self):
        message = self._builder.create_message(oid='nop')
        self._send_message(websocket=self._get_curr_connection(), message=message, wait_for_response=False)

    def ack(self):
        message = self._builder.create_message(oid='ack')
        self._send_message(websocket=self._get_curr_connection(), message=message, wait_for_response=False)

    def bye(self):
        message = self._builder.create_message(oid='bye')
        return self._send_message(websocket=self._get_curr_connection(), message=message)

    def again(self):
        message = self._builder.create_message(oid='again')
        self._send_message(websocket=self._get_curr_connection(), message=message, wait_for_response=False)

    def get_resources(self):
        message = self._builder.create_message(oid='getResources')
        self._send_message(websocket=self._get_curr_connection(), message=message, wait_for_response=False)

    def resources(self, data, push_token=None):
        body = {'oid': 'resources', 'data': data}
        if push_token is not None:
            body.update(push_token=push_token)
        message = self._builder.create_message(body)
        self._send_message(websocket=self._get_curr_connection(), message=message, wait_for_response=False)

    def try_request(self, try_id, auth_timeout, policy=None, try_info=None, resource=None, message=None):
        body = {'oid': 'try', 'try_id': try_id, 'auth_timeout': auth_timeout}
        if policy is not None:
            body.update(policy=policy)
        if try_info is not None:
            body.update(try_info=try_info)
        if resource is not None:
            body.update(resource=resource)
        if message is not None:
            body.update(message=message)
        message = self._builder.create_message(body)
        self._send_message(websocket=self._get_curr_connection(), message=message, wait_for_response=False)

    def probe_response(self, try_id, try_type, probe_status, probe_data=None):
        body = {'oid': 'probeStatus', 'try_id': try_id, 'try_type': try_type,
                'probeStatus': probe_status}
        if probe_data is not None:
            body.update(probeData=probe_data)
        message = self._builder.create_message(body)
        self._send_message(websocket=self._get_curr_connection(), message=message, wait_for_response=False)

    def hello(self, **kwargs):
        body = kwargs.copy()
        if self._mode == MODE_CLIENT_API:
            body['oid'] = 'clientHello'
        elif self._mode == MODE_SERVER_API:
            body['oid'] = 'serverHello'
        message = self._builder.create_message(body)
        response = self._send_message(websocket=self._get_curr_connection(), message=message)
        self._check_tokens(response, oid='serverHello')
        return response

    def auth(self, **kwargs):
        body = kwargs.copy()
        body.update(oid='auth')
        message = self._builder.create_message(body)
        self._send_message(websocket=self._get_curr_connection(), message=message, wait_for_response=False)

    def rpc_request(self, session_id, on_behalf_of, namespace, call, data={}):
        message = self._builder.create_message(oid='rpcReq', session_id=session_id, onBehalfOf=on_behalf_of,
                                               namespace=namespace, call=call, data=data)
        response = self._send_message(websocket=self._get_curr_connection(), message=message)
        if response and response.header.oid == 'rpcResp':
            return response
        return None

    def rpc_enum_ns_request(self):
        message = self._builder.create_message(oid='rpcEnumNsReq')
        response = self._send_message(websocket=self._get_curr_connection(), message=message)
        if response and response.header.oid == 'rpcEnumNsResp':
            return response
        return None

    def rpc_enum_calls_request(self, ns):
        message = self._builder.create_message(oid='rpcEnumCallsReq', ns=ns)
        response = self._send_message(websocket=self._get_curr_connection(), message=message)
        if response and response.header.oid == 'rpcEnumCallsResp':
            return response
        return None

    def handshake(self, private_key, **kwargs):
        response = self.hello(kwargs)
        if response and response.header.oid == 'serverHello':
            self.auth(key=self._get_digest_for_next_message(private_key=private_key))
            return True
        return False

    def restore(self):
        response = self.hello()
        if response and response.header.oid == 'serverHello':
            return True
        return False

    def repeat(self):
        self._send_message(message=self._last_send_message, websocket=self._get_curr_connection(),
                           wait_for_response=False)

    def close(self):
        response = self.bye()
        if response and response.header.oid == 'bye':
            return True
        return False
