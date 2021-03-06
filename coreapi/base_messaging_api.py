from websocket import WebSocket
from settings import DEFAULT_SOCKET_TIMEOUT, SSL_OPTIONS
from crypt import Crypto
import select
import sys


WEBSOCKET_URL = "wss://{host}:{port}/websocket"


OPCODE_CONT = 0x0
OPCODE_TEXT = 0x1
OPCODE_BINARY = 0x2
OPCODE_CLOSE = 0x8
OPCODE_PING = 0x9
OPCODE_PONG = 0xa


class BaseMessagingAPI(object):
    def __init__(self, host, port):
        self._websocket_url = WEBSOCKET_URL.format(host=host, port=port)
        self._last_read_message = None
        self._last_sent_message = None
        self._session_token = None
        self._refresh_token = None
        self._session_ttl = None
        self._connection_ttl = None
        self._builder = None
        self._ws = None

    def receive(self):
        request = self._read_message(self._ws)
        if request:
            return request
        return None

    def select(self, ping_timeout=0):
        r, w, e = select.select((self._ws.sock, ), (), (), ping_timeout)
        if r:
            op_code, frame = self._ws.recv_data_frame(True)
            data = frame.data
            if op_code == OPCODE_CLOSE:
                pass
            elif op_code == OPCODE_CONT:
                pass
            elif op_code == OPCODE_TEXT:
                pass
            elif op_code == OPCODE_BINARY:
                pass
            elif op_code == OPCODE_PING:
                pass
            elif op_code == OPCODE_PONG:
                pass
            response = self._create_message_from_json(data)
            self._last_read_message = response
            return response
        return None

    def _get_digest_for_next_message(self, private_key):
        """
        Creates digest for next message.
        """
        header_str = self._builder.header_string()
        return Crypto.create_digest(data=header_str, key=private_key)

    def _create_message_from_json(self, json_string):
        return self._builder.create_message_from_json(json_string)

    def _new_connection(self, socket_timeout=DEFAULT_SOCKET_TIMEOUT):
        """
        Creates connection and returns socket that could be used for further
        communication with server.
        :param: socket_timeout Timeout for socket operations.
        :return: WebSocket connected to server.
        """
        socket = WebSocket()#sslopt=SSL_OPTIONS)
        socket.connect(self._websocket_url)
        socket.settimeout(socket_timeout)
        return socket

    def _get_curr_connection(self):
        """
        Helper method to get current connected websocket object.
        Could be used to get current websocket after some setup methods
        (e.g. setup_test_with_handshake) that creates connection with server
        and send messages to prepare test case.
        """
        if not self._ws or not self._ws.connected:
            self._ws = self._new_connection()
        return self._ws

    def _read_message(self, websocket):
        """
        Reads message from given websocket and memorizes session and refresh tokens
        as well as the last received message. Memorized tokens will be used in further
        communication with server.
        :param: Websocket connected to server to listen.
        :return: BIOMIO message responce object.
        """
        try:
            response_str = websocket.recv()
            response = self._create_message_from_json(response_str)
            self._last_read_message = response
            return response
        except:
            print sys.exc_info()[0]
            return None

    def _send_message(self, message, websocket=None, wait_for_response=True, close_connection=False):
        """
        Sends given message to server using given connected to server websocket. This method also could be used
        to listen to server responce.
        :param: message BIOMIO message object.
        :param: websocket Connected to server WebSocket object. If not specified - new connection will be established.
        :param: wait_for_response If True method will wait for responce and return BIOMIO message response object.
        :param: close_connection Closes connection after method execution if True; leaves connection open otherwise.
        :return: WebSocket connected to server.
        """
        if websocket is None:
            websocket = self._new_connection()
        self._last_sent_message = message
        websocket.send(message.serialize())
        response = None
        if wait_for_response:
            response = self._read_message(websocket=websocket)
        if close_connection:
            websocket.close()
        return response

    def _check_tokens(self, response, oid):
        if response:
            if not str(response.header.token) == self._session_token:
                self._set_session_token(str(response.header.token))
            if response.msg.oid == oid:
                self._refresh_token = str(response.msg.refreshToken)
                self._session_ttl = int(response.msg.sessionttl)
                self._connection_ttl = int(response.msg.connectionttl)

    def _set_session_token(self, token):
        """
        Sets session token for BiomioTest object. Token will be used in further
        communication with server. Method raises exception if appropriate setup method
        was not called before.
        :param token: Session token.
        """
        self._builder.set_header(token=token)
        self._session_token = token
