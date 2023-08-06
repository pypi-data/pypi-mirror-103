import socket


class global_trie():
    def __init__(self, ip, port):
        # Initialize all variables.

        self.PORT = port
        self.IP = ip
        self.ADDRESS = (ip, self.PORT)
        self.disconnect_message = 'disconnect'
        self.client = socket.socket()

    def connect(self):
        # Initiate the connection to the server.

        self.client.connect(self.ADDRESS)

    def _send_msg(self, msg):
        # Function to send messages to server.

        msg_length_in_bytes = str(len(msg)).encode('utf-8')
        self.client.send(b' ' * (64 - len(msg_length_in_bytes)) + msg_length_in_bytes)
        self.client.send(msg.encode('utf-8'))

    def _get_msg(self):
        # Function to receive messages and print them to screen.

        msg_length = int(self.client.recv(64).decode('utf-8'))
        msg = self.client.recv(msg_length).decode('utf-8')
        print(f"[Client] received message: {msg}")
        if msg == self.disconnect_message:
            self.client.close()

    def add_keyword(self, word):
        # Tells server to add word to Trie.

        self._send_msg(f'add {word}')
        self._get_msg()

    def remove_keyword(self, word):
        # Tells server to remove word from Trie.

        self._send_msg(f'remove {word}')
        self._get_msg()

    def keyword_exists(self, word):
        # Asks server if words exists in Trie.

        self._send_msg(f'exists {word}')
        self._get_msg()

    def autocomplete(self, prefix):
        # Asks server for all words in Trie with certain prefix.

        self._send_msg(f'autocomplete {prefix}')
        self._get_msg()

    def print(self):
        # Asks server to return printable value of the Trie.

        self._send_msg(f'print')
        self._get_msg()

    def save(self):
        # Asks server to save the current state of the Trie.

        self._send_msg(f'save')
        self._get_msg()
