from test_client import TestClient
from base_client import TRY_REQUEST, RESOURCE_REQUEST, DISCONNECT, CONNECT
from binascii import b2a_base64
from nose.tools import nottest
from test.utils import get_files
import threading
import time
import os

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
FACE_TRAINING_DATA_PATH = os.path.join(APP_ROOT, "data", "face_training")
WEBSOCKET_HOST = "gate-dev.biom.io"
WEBSOCKET_PORT = "8080"


class OpenIdSim:
    def __init__(self):
        self._client = None
        self._private_key = """-----BEGIN RSA PRIVATE KEY-----
        MIICXgIBAAKBgQCoBl9L2XrEH+UJ1oDcSg/U7/h1YlKMsu+NdygI0J2wxRe5HWZE
        YU5VQDGXbpm1yhEe4AyKZwXnQnET/aqA/LxnQNe2VYjYCsY8BUN0zJwIBmv4k28E
        zlh9mV+5BXUSEBe7COcfezPen0llVYJdtMRYRNZP59vHBB2ZpuBaHdKaCQIDAQAB
        AoGBAKYudz4bgLJNIUhToOs/TN074i6m6iJCL29o9G2TdwMIS+hITYc//iuO6/1r
        5BbKHZi922lfb5VEP3aYInSkgui5zCYfa0zDQD2GK2QZvOfuSGEdD/uDI3U+dgKg
        mzprWoQ1kFVLshxs7fb7/WXDwtKLL/aR1dAWaEHGxasjY1kBAkEAx8GxrYch1HcW
        Jo2UtzPxigbuowsnvJb1QIAINfoWLBa/NixGxuaAoKH+sXTfKCvSicJE56z/7377
        SELdOp0lWQJBANdVermVlseZpAYfgA70/gKPBEcR4IxkhRfUAPGc29+fw5bulvfn
        kFjV8ULilnR8UE89FFaSsWOPrko85A1/lDECQBtPX/tZfkaOAXlD4hEqCNvWFsoz
        vDsMaHtpBbZbeqyMb5f4dbS7ztonS6r3T4sucppi9Qi3nkYgFjrK6XQaCAECQQDS
        XAArQpZs4YwaKzW35uAqcbqVD0LVA/H9SC+v2TP27yVs0iILhl0+W6p4U9D1dOgj
        sKCovl+qypdSkM+c3DBRAkEAkmKKpdKfjRs7PFfFv81AwSTZFGxj1q/JfPwN3KIJ
        vVn65Ak0oZ2w54K8upQlnwC7kKWbL6JH1QYpXbvWHuju8Q==
        -----END RSA PRIVATE KEY-----"""
        self._app_type = 'extension'
        self._app_id = 'a8574879896db2f989c3a40155399531'
        self._os_id = 'linux'
        self._dev_id = 'node_js_lib'
        # self._app_type = 'probe'
        # self._app_id = '23baecb6e903c6cc98917247da020b11'
        # self._os_id = 'Android_6.0.1'
        # self._dev_id = 'c1d277535c7fbc2'

    def setup(self):
        self._client = TestClient(WEBSOCKET_HOST, WEBSOCKET_PORT, "", app_type=self._app_type,
                                    app_id=self._app_id, os_id=self._os_id, dev_id=self._dev_id)
        self._client.register(CONNECT, self._connect_callback)
        self._client.register(DISCONNECT, self._disconnect_callback)
        self._client.register(TRY_REQUEST, self._try_callback)
        self._client.register(RESOURCE_REQUEST, self._resource_callback)
        print "!!SETUP!!"

    def teardown(self):
        self._client.disconnect()
        time.sleep(10)
        print "||TEARDOWN||"

    @nottest
    def active_test(self):
        self._client.join(self._connect_callback)
        t = threading.Thread(target=self._client.run)
        t.start()

        session_id = ""
        on_behalf_of = "biomio.vk.test@gmail.com"
        namespace = "auth_client_plugin"
        call_pr = "process_auth"
        data = {
            "keys": ["email", "auth_code"],
            "values": ["biomio.vk.test@gmail.com", "NO_REST"]
        }

        time.sleep(5)
        # self._client.request(session_id, on_behalf_of, namespace, call_pr, data, callback=self._request_callback)
        i = 0
        while True:
            time.sleep(2)
            i += 1
            if i == 400:
                break
        print "wake up"

    @nottest
    def passive_test(self):
        self._client.run()
        # print "passive sleep"
        # time.sleep(20)
        print "passive wake up"

    @nottest
    def _request_callback(self, request):
        print "REQ CALLBACK", dict(request)

    @nottest
    def _enum_ns_callback(self, request):
        print request

    @nottest
    def _enum_calls_callback(self, request):
        print request

    @nottest
    def _restore_callback(self, request):
        print "restore", request

    @nottest
    def _connect_callback(self, request):
        print "connect", request
        session_id = ""
        on_behalf_of = "biomio.vk.test@gmail.com"
        namespace = "auth_client_plugin"
        # call_pr = 'check_user_exists'
        # data = {
        #     "keys": ["client_key"],
        #     "values": ["biomio.vk.test@gmail.com"]
        # }
        call_pr = "process_auth"
        data = {
            "keys": ["email", "auth_code"],
            "values": ["biomio.vk.test@gmail.com", "NO_REST"]
        }

        time.sleep(5)
        self._client.request(session_id, on_behalf_of, namespace, call_pr, data, callback=self._request_callback)

    @nottest
    def _disconnect_callback(self, request):
        print "DISCONNECT CALLBACK", request

    @nottest
    def _try_callback(self, request):
        if request:
            msg = dict(request['msg'])
            tries_list = msg['resource']
            message = {
                "probe_status": "success",
                "try_id": msg['try_id']
            }
            for try_data in tries_list:
                print "================= TRY ================="
                probe_data = None
                if try_data['tType'] == "face":
                    image_samples = [self.image_data(os.path.join(FACE_TRAINING_DATA_PATH, f))
                                     for f in get_files(FACE_TRAINING_DATA_PATH)]
                    used_samples = [image_samples[inx] for inx in range(0, try_data['samples'], 1)]
                    probe_data = {
                        'oid': "imageSamples",
                        'samples': used_samples
                    }
                elif try_data['tType'] == "fp":
                    probe_data = {
                        "oid": "locationSamples",
                        "samples": ["49.811055,24.079584,65.000000"]
                    }
                    if len(tries_list) > 1:
                        continue
                else:
                    if len(tries_list) > 1:
                        continue
                curr_message = message.copy()
                curr_message.update({'probe_data': probe_data, 'try_type': try_data['tType']})
                request['callback'](**curr_message)
                print "================= TRY DEAD ================="

    @staticmethod
    @nottest
    def image_data(image_path):
        data = None
        with open(image_path, "rb") as f:
            data = b2a_base64(f.read())
        return data

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
        request['callback'](**message)


sim = OpenIdSim()
sim.setup()
sim.active_test()
