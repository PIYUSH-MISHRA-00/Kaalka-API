from kaalka.kaalka import Kaalka

kaalka_instance = Kaalka()

def encrypt(message: str, timestamp: str) -> str:
    """
    Encrypt the message using Kaalka.encrypt with the given timestamp.
    """
    return kaalka_instance.encrypt(message, timestamp)

def decrypt(encrypted: str, timestamp: str) -> str:
    """
    Decrypt the encrypted message using Kaalka.decrypt with the given timestamp.
    """
    return kaalka_instance.decrypt(encrypted, timestamp)
