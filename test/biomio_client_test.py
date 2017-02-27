from ..biomio_client import BiomioClient, TRY_REQUEST, RESOURCE_REQUEST
from nose.tools import nottest


class BiomioClientTest:
    def __init__(self):
        self._client = None
        self._private_key = None
        self._app_type = None
        self._app_id = None
        self._os_id = ''
        self._dev_id = ''

    def setup(self):
        pass

    def teardown(self):
        self._client.disconnect()

    def active_test(self):
        self._client = BiomioClient(self._private_key, app_type=self._app_type, app_id=self._app_id,
                                    os_id=self._os_id, dev_id=self._dev_id, auto_receiving=True, timeout=5)
        self._client.connect()

        session_id = ""
        on_behalf_of = ""
        namespace = ""
        call_pr = ""
        data = ""
        self._client.request(session_id, on_behalf_of, namespace, call_pr, data, callback=self._request_callback)

        self._client.enum_ns_request(callback=self._enum_ns_callback)

        ns = ""
        self._client.enum_calls_request(ns=ns, callback=self._enum_calls_callback)

    def passive_test(self):
        self._client = BiomioClient(self._private_key, app_type=self._app_type, app_id=self._app_id,
                                    os_id=self._os_id, dev_id=self._dev_id, auto_receiving=False, timeout=5)
        self._client.register(TRY_REQUEST, self._try_callback)
        self._client.register(RESOURCE_REQUEST, self._resource_callback)
        self._client.connect()
        while True:
            pass

    @nottest
    def _request_callback(self, request):
        print request

    @nottest
    def _enum_ns_callback(self, request):
        print request

    @nottest
    def _enum_calls_callback(self, request):
        print request

    @nottest
    def _try_callback(self, request):
        message = {
            "probeData": {
                "oid": "locationSamples",
                "samples": ["49.811055,24.079584,65.000000"]
            },
            "probeStatus": "success",
            "tType": "location",
            "try_id": 'try_id'
        }
        request['callback'](message)

    @nottest
    def _resource_callback(self, request):
        message = {
            "push_token": "1234567",
            "data": [
                {
                    "rProperties": "1280x960,1280x720,640x480,480x360,192x144",
                    "rType": "front-cam"
                },
                {
                    "rProperties": "3264x2448,1920x1080,1280x720,640x480,480x360,192x144",
                    "rType": "back-cam"
                },
                {
                    "rProperties": "",
                    "rType": "mic"
                },
                {
                    "rProperties": "",
                    "rType": "fp-scanner"
                },
                {
                    "rProperties": "",
                    "rType": "location"
                },
                {
                    "rProperties": "",
                    "rType": "input"
                },
            ]
        }
        request['callback'](message)
