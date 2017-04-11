from biomio_messaging_api import BiomioMessagingAPI, MODE_CLIENT_API
import json


class TestMessagingAPI(BiomioMessagingAPI):
    def __init__(self, host, port, app_type, app_id, os_id='', dev_id='', mode=MODE_CLIENT_API):
        BiomioMessagingAPI.__init__(self, host=host, port=port, app_type=app_type, app_id=app_id, os_id=os_id,
                                    dev_id=dev_id, mode=mode)
        self._mode = mode
        self._create_builder(app_type, app_id, os_id, dev_id)

    def direct_hello(self):
        body = {'oid': 'clientHello'}
        message = {'header': self._builder._header, 'msg': body}
        ws = self._get_curr_connection()
        ws.send(json.dumps(message))
