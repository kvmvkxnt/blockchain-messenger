'''This module represents basic Diffie Hellman algorythm usage'''

from cryptography.hazmat.primitives.asymmetric import dh
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.serialization import (
    load_pem_public_key,
    Encoding,
    PublicFormat
)
from cryptography.hazmat.backends import default_backend


class DiffieHellmanKeyExchange:
    '''
    Class manages all DH keys

    :ivar parameters: DH parameter group
    :type parameters: dh.DHParameters
    :ivar private_key: DH private key
    :type private_key: dh.DHPrivateKey
    :ivar public_key: DH public key
    :type public_key: dh.DHPublicKey
    '''

    def __init__(self) -> None:
        '''Initializes DH key manager'''

        # Using pre-installed DH parameters
        self.parameters = dh.DHParameterNumbers(0xFFFFFFFFFFFFFFFFC90FDAA22168C234C4C6628B80DC1CD129024E088A67CC74020BBEA63B139B22514A08798E3404DDEF9519B3CD3A431B302B0A6DF25F14374FE1356D6D51C245E485B576625E7EC6F44C42E9A637ED6B0BFF5CB6F406B7EDEE386BFB5A899FA5AE9F24117C4B1FE649286651ECE45B3DC2007CB8A163BF0598DA48361C55D39A69163FA8FD24CF5F83655D23DCA3AD961C62F356208552BB9ED529077096966D670C354E4ABC9804F1746C08CA18217C32905E462E36CE3BE39E772C180E86039B2783A2EC07A28FB5C55DF06F4C52C9DE2BCBF6955817183995497CEA956AE515D2261898FA051015728E5A8AACAA68FFFFFFFFFFFFFFFF, 2) \
                            .parameters(default_backend())
        self.private_key = self.parameters.generate_private_key()
        self.public_key = self.private_key.public_key()

    def get_public_key(self) -> dh.DHPublicKeyWithSerialization:
        '''
        Returns public key in serialized form

        :return: Public key in serialized form
        :rtype: dh.DHPublicKeyWithSerialization
        '''
        return self.public_key.public_bytes(
            Encoding.PEM, PublicFormat.SubjectPublicKeyInfo
        )

    def generate_shared_key(self, peer_public_key_bytes:
                            dh.DHPublicKeyWithSerialization) -> bytes:
        '''
        Creates shared key based on other peers public key

        :param peer_public_key_bytes: Other peer's public key
        :type peer_public_key_bytes: dh.DHPublicKeyWithSerialization
        :return: The derived shared key
        :rtype: bytes
        '''
        peer_public_key = load_pem_public_key(peer_public_key_bytes)
        shared_key = self.private_key.exchange(peer_public_key)

        # Применяем KDF для усиления ключа
        derived_key = HKDF(
            algorithm=hashes.SHA256(),
            length=32,
            salt=None,
            info=b'dh key exchange'
        ).derive(shared_key)

        return derived_key
