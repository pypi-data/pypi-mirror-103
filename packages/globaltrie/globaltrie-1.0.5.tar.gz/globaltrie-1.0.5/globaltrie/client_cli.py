# Only change things below if you know what you are doing.
import socket, argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-ip', '--ip', type=str, help="Put the IP of the Trie Server")
    parser.add_argument('-p', '--port', type=int, help="Put the Port of the Trie Server")
    args = parser.parse_args()
    if args.ip is None or args.port is None:
        # Make sure IP and PORT is filled out.

        print("You need to add values for the IP and PORT of the Trie Server.")
        exit()
    IP = args.ip  # IP of Trie Server
    PORT = args.port  # Port of Trie Server

    ADDRESS = (IP, PORT)
    disconnect_message = 'disconnect'

    try:
        client = socket.socket()
        client.connect(ADDRESS)
    except:
        print("The Trie Server is either not online or the IP and PORT combination you put is wrong")
        exit()

    while True:
        msg = input("[Server] enter your message...")
        if msg.lower() == 'help':
            print("""[Client] Available Commands:
        - add 'input_word'              # Adds a word to the Trie
        - remove 'input_word'           # Removes a word from the Trie
        - exists 'input_word'           # Checks if word is in the Trie
        - autocomplete 'input_word'     # Returns words in the Trie that start with a prefix
        - print                         # Prints out the Trie
        - save                          # Saves the data in the Trie for future use
        - disconnect                    # Disconnects the client from the server""")
            continue
        msg_length_in_bytes = str(len(msg)).encode('utf-8')
        # Send MSG length first, then MSG itself.
        client.send(b' '*(64-len(msg_length_in_bytes)) + msg_length_in_bytes)
        client.send(msg.encode('utf-8'))
        # Receive MSG length first, then MSG itself.
        msg_length = int(client.recv(64).decode('utf-8'))
        msg = client.recv(msg_length).decode('utf-8')
        # Print MSG to screen.
        print(f"[Client] received message: {msg}")
        if msg == disconnect_message:
            break
    client.close()
