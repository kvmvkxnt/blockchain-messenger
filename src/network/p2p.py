import json5 as json
from utils.logger import Logger
from .sockets import P2PSocket
from .sync import SyncManager

log = Logger("p2p")


class P2PNetwork:
    def __init__(self, blockchain, host='0.0.0.0', port=5000):
        self.peers = set()
        self.blockchain = blockchain
        self.sync_manager = SyncManager(blockchain)
        self.socket = P2PSocket(host, port)

    def start_network(self):
        """Start the P2P network server."""
        self.socket.start_server(self.handle_client)

    def handle_client(self, conn):
        """Handle communication with a connected client."""
        try:
            while True:
                message = self.socket.receive_message(conn)
                if not message:
                    break
                log.info(f"Received: {message}")
                self.process_message(conn, message)
        except Exception as e:
            log.error(f"Error handling client: {e}")
        finally:
            conn.close()

    def process_message(self, conn, message):
        """Process incoming messages."""
        try:
            data = json.loads(message)
            msg_type = data.get('type')
            if msg_type == 'request_blockchain':
                self.send_blockchain(conn)
            elif msg_type == 'new_block':
                self.handle_new_block(data)
            elif msg_type == 'new_transaction':
                self.handle_new_transaction(data)
        except Exception as e:
            log.error(f"Error processing message: {e}")

    def send_blockchain(self, conn):
        """Send the current blockchain to a peer."""
        response = {'type': 'blockchain_response', 'blockchain': self.blockchain}
        self.socket.send_message(conn, json.dumps(response))
        log.info("Sent blockchain data")

    def handle_new_block(self, data):
        """Handle a new block received from a peer."""
        block = data.get('block')
        if block:
            self.blockchain.append(block)
            log.info("Added new block to the blockchain")
        else:
            log.error("Invalid block data received")

    def handle_new_transaction(self, data):
        """Handle a new transaction received from a peer."""
        transaction = data.get('transaction')
        if transaction:
            log.info(f"Received transaction: {transaction}")
            # You can add transaction verification here
        else:
            log.error("Invalid transaction data received")
