from coreapi.test_messaging_api import TestMessagingAPI
from biomio_client import BiomioClient


class TestClient(BiomioClient):
    def __init__(self, host, port, private_key, app_type, app_id, os_id='', dev_id=''):
        BiomioClient.__init__(self, host, port, private_key, app_type, app_id, os_id, dev_id)
        self._messaging_api = TestMessagingAPI(host=host, port=port, app_type=app_type, app_id=app_id,
                                               os_id=os_id, dev_id=dev_id)

    def join(self, callback=None):
        response = self._messaging_api.direct_hello()
        # self._is_connected = response.msg.oid == 'serverHello'
        # res = {'connected': self._is_connected}
        # if callback is not None:
        #     callback(res)
        # self._call_callback(CONNECT, **res)

    def run(self):
        # if not self._is_connected:
        #     self.connect()
        while True: #self._is_connected:
            request = self._messaging_api.select(3)
            self._handle_request(request)
            if self._is_connected and request is None:
                self._messaging_api.nop()
