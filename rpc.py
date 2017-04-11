import time
import websocket
import json

# docker build -t gate-dev:v1 .
# docker images
# df -Th
# docker run -d -p 743:443 -p 7080:8080 -p 7379:6379 -p 7381:6381 -p 744:444 gate-dev:v1 /usr/bin/supervisord -c /opt/supervisord.conf
#

if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.create_connection("wss://gate-dev.biom.io:8080/websocket")

    seq = 0
    onBehalfOf = 'biomio.vk.test@gmail.com'

    header = {
            "protoVer": "1.0",
            "seq": seq,
            "oid": "clientHeader",
            "appId": "a8574879896db2f989c3a40155399531",
            "appType": "extension",
            "osId": "linux",
            "devId": "node_js_lib",
            # 'token': None
    }

    msg = {
        "msg": {
            "oid": "clientHello",
            # 'secret': None,
            # 'apnsToken': None
        },
        "header": header
    }

    print('- SEND MESSAGE --------------------------------------------------------------------------------------------')
    print("{}".format(msg))
    print('-----------------------------------------------------------------------------------------------------------')

    ws.send(json.dumps(msg))

    token = None
    key = None

    while True:
        result = ws.recv()
        if result:
            print('- RECEIVED MESSAGE ----------------------------------------------------------------------------------------')
            print("{}".format(result))
            print('-----------------------------------------------------------------------------------------------------------')

            result = json.loads(result)
            received_msg = result.get('msg')
            received_header = result.get('header')

            if (not token) or (token == received_header.get('token')):
                seq += 2
                token = received_header.get('token')

                if received_msg['oid'] == 'rpcResp' and received_msg['call'] == 'check_user_exists':
                    msg = {
                        "msg":
                            {
                                "oid": "rpcReq",
                                "onBehalfOf": onBehalfOf,
                                "namespace": "auth_client_plugin",
                                "call": "process_auth",
                                "data": {
                                    "keys": [
                                        "email", "auth_code"
                                    ],
                                    "values": [
                                        onBehalfOf,
                                        "NO_REST"
                                    ]
                                }
                            },

                        "header": {
                            "protoVer": "1.0",
                            "seq": seq,
                            "oid": "clientHeader",
                            "appId": "a8574879896db2f989c3a40155399531",
                            "appType": "extension",
                            "osId": "linux",
                            "devId": "node_js_lib",
                            "token": token
                        }
                    }

                    print(
                    '- SEND MESSAGE --------------------------------------------------------------------------------------------')
                    print("{}".format(msg))
                    print(
                    '-----------------------------------------------------------------------------------------------------------')

                    ws.send(
                        json.dumps(
                            msg
                        )
                    )

                # if received_msg['oid'] == 'rpcResp' and received_msg['call'] == 'process_auth':
                #     msg = {
                #         "msg":
                #             {
                #                 "oid": "rpcReq",
                #                 "onBehalfOf": "testssssss2@gmail.com",
                #                 "namespace": "process_auth",
                #                 "call": "check_user_exists",
                #                 "data": {
                #                     "keys": [
                #                         "email","auth_code"
                #                     ],
                #                     "values": [
                #                         "roman.slyepko@vakoms.com.ua",
                #                         "NO_REST"
                #                     ]
                #                 }
                #             },
                #
                #         "header": {
                #             "protoVer": "1.0",
                #             "seq": seq,
                #             "oid": "clientHeader",
                #             "appId": "a8574879896db2f989c3a40155399531",
                #             "appType": "extension",
                #             "osId": "linux",
                #             "devId": "node_js_lib",
                #             "token": token
                #         }
                #     }
                #
                #     print(
                #     '- SEND MESSAGE --------------------------------------------------------------------------------------------')
                #     print("{}".format(msg))
                #     print(
                #     '-----------------------------------------------------------------------------------------------------------')
                #
                #     ws.send(
                #         json.dumps(
                #             msg
                #         )
                #     )

                if received_msg['oid'] == 'serverHello':
                    msg = {
                        "msg":
                            {
                                "oid": "rpcReq",
                                "onBehalfOf": onBehalfOf,
                                "namespace": "auth_client_plugin",
                                "call": "check_user_exists",
                                "data": {
                                    "keys": [
                                        "client_key"
                                    ],
                                    "values": [
                                        onBehalfOf
                                    ]
                                }
                            },

                        "header": {
                            "protoVer": "1.0",
                            "seq": seq,
                            "oid": "clientHeader",
                            "appId": "a8574879896db2f989c3a40155399531",
                            "appType": "extension",
                            "osId": "linux",
                            "devId": "node_js_lib",
                            "token": token
                        }
                    }

                    print('- SEND MESSAGE --------------------------------------------------------------------------------------------')
                    print("{}".format(msg))
                    print('-----------------------------------------------------------------------------------------------------------')

                    ws.send(
                        json.dumps(
                            msg
                        )
                    )
        else:
            time.sleep(5)
        time.sleep(5)
    ws.close()