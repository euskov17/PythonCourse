import string


def caesar_encrypt(message: str, n: int) -> str:
    """Encrypt message using caesar cipher

    :param message: message to encrypt
    :param n: shift
    :return: encrypted message
    """
    str_lower = string.ascii_lowercase
    str_upper = string.ascii_uppercase
    lower_letters_trans = str_lower[n % len(str_lower):] + str_lower[:n % len(str_lower)]
    upper_letters_trans = str_upper[n % len(str_upper):] + str_upper[:n % len(str_upper)]
    letters_trans = lower_letters_trans + upper_letters_trans
    transtab = message.maketrans(string.ascii_letters, letters_trans)
    new_str = message
    return new_str.translate(transtab)
