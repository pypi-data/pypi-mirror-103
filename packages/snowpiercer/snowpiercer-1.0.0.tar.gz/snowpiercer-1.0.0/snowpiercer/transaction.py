import json
from base64 import b64decode

from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5


class Transaction:
    def __init__(self, sender, receiver, content, signature=None):

        self.sender = sender
        self.receiver = receiver
        self.content = content
        self.signature = signature

    def hash(self):

        tx = json.dumps({
            'sender': self.sender.hex(),
            'receiver': self.receiver,
            'content': self.content
        })
        return SHA256.new(str.encode(tx))

    def sign(self, private_key):

        signature = PKCS1_v1_5.new(private_key).sign(msg_hash=self.hash())
        if not signature:
            print('Signing transaction failed')
            return False

        self.signature = signature
        return True

    @staticmethod
    def validate(tx):

        public_key = RSA.importKey(b64decode(tx.sender))
        validator = PKCS1_v1_5.new(public_key)

        is_valid = validator.verify(tx.hash(), tx.signature)
        if not is_valid:
            print('Verifying failed')
            return False

        return True
