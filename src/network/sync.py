import json5 as json
from utils.logger import Logger

log = Logger("sync")


class SyncManager:
    def __init__(self, blockchain):
        self.blockchain = blockchain

    def request_blockchain(self, connection):
        """Request blockchain data from another node."""
        request = {'type': 'request_blockchain'}
        connection.send(json.dumps(request).encode('utf-8'))
        log.info("Requested blockchain data")

    def handle_blockchain_response(self, response):
        """Handle received blockchain data."""
        try:
            data = json.loads(response)
            if 'blockchain' in data:
                log.info("Received blockchain data")
                # Update local blockchain if needed
                self.compare_and_update(data['blockchain'])
        except Exception as e:
            log.error(f"Failed to process blockchain response: {e}")

    def compare_and_update(self, received_blockchain):
        """Compare and update local blockchain with received data."""
        if len(received_blockchain) > len(self.blockchain):
            self.blockchain = received_blockchain
            log.info("Blockchain updated with received data")
        else:
            log.info("Received blockchain is not longer. Ignoring.")
