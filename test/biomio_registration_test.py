from ..biomio_registration import BiomioRegistration


WEBSOCKET_HOST = "gate-dev.biom.io"
WEBSOCKET_PORT = "8080"


class TestBiomioRegistration(object):
    def __init__(self):
        self._registrator = BiomioRegistration(WEBSOCKET_HOST, WEBSOCKET_PORT)

    def register_test(self):
        app_type = "probe"
        dev_id = "c1d277535c7fbc2"
        os_id = "Android_6.0.1"
        secret = "66236380"
        reg_data = self._registrator.register(secret, app_type, os_id, dev_id)
        print reg_data
