DEFAULT_SOCKET_TIMEOUT = 5  # seconds
SSL_OPTIONS = {
    "ca_certs": "server.pem"
}
WEBSOCKET_HOST = ""
WEBSOCKET_PORT = 0
WEBSOCKET_URL = "wss://{host}:{port}/websocket".format(host=WEBSOCKET_HOST, port=WEBSOCKET_PORT)
