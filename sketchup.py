
import random
from umbral import umbral, keys, config


def encrypt_financial_record(pub_key, record_content):
    """
    encrypt financial record XBRL content

    :param pub_key: public key of the orignial financial Record Originator, to be used for encrypting
    :param record_content: XBRL content of the financial record
    :return: a tuple holding the cipher text and capsul info
    """
    ciphertext, umbral_capsule = umbral.encrypt(pub_key, record_content)

    return ciphertext, umbral_capsule
