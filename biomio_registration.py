from coreapi.biomio_messaging_api import BiomioMessagingAPI


class BiomioRegistration(object):
    def __init__(self, host, port):
        self._host = host
        self._port = port

    def register(self, secret, app_type, os_id='', dev_id=''):
        api = BiomioMessagingAPI(host=self._host, port=self._port, app_type=app_type, app_id='',
                                 dev_id=dev_id, os_id=os_id)
        response = api.hello(**{'secret': secret})
        if response and response.msg.oid == 'serverHello':
            api.ack()
            return {
                'app_type': app_type,
                'app_id': response.msg.fingerprint,
                'os_id': os_id,
                'dev_id': dev_id,
                'private_key': response.msg.key
            }
        return None
