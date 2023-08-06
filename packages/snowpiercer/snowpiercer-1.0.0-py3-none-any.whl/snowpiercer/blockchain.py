from .block import Block


class Blockchain:
    def __init__(self):

        self.validated_transactions = []
        self.chain = []

        self.__generate_block(previous_hash='0')

    @property
    def last_block(self):
        return self.chain[-1]

    @property
    def size(self):
        return len(self.chain)

    def generate_block(self):
        previous_hash = self.last_block.hash()

        return self.__generate_block(previous_hash)

    def add_transaction(self, transaction):

        return self.__add_transaction(transaction)

    def __generate_block(self, previous_hash):

        block = Block(index=self.size + 1,
                      transactions=self.validated_transactions,
                      previous_hash=previous_hash)

        self.validated_transactions = []
        self.chain.append(block)

        return block

    def __add_transaction(self, transaction):

        self.validated_transactions.append(transaction)
