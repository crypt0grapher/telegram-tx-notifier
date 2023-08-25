import hashlib
import re


def safe_bignumber_to_float(value):
    try:
        return float(value) / 10 ** 18
    except ValueError:
        return 0.0


def is_valid_ethereum_address(address: str) -> bool:
    if len(address) != 42 or not address.startswith("0x"):
        return False
    # Check if it's a hexadecimal string
    if not re.fullmatch("0x[a-fA-F0-9]{40}", address):
        return False

    # Check the checksum if it's a mixed-case address
    # if not re.fullmatch("0x[a-f0-9]{40}", address) and not re.fullmatch("0x[A-F0-9]{40}", address):
    #     return check_checksum(address)

    return True


def check_checksum(address: str) -> bool:
    address = address[2:]  # Remove the '0x' prefix
    address_hash = hashlib.sha3_256(address.lower().encode()).hexdigest()

    for i in range(40):
        address_char = int(address[i], 16)
        hash_char = int(address_hash[i], 16)

        # If the ith digit is a letter and it's capital
        if address_char > 9 and address[i].isupper():
            # Check if the corresponding hash digit is 8 or higher
            if hash_char <= 7:
                return False
        # If the ith digit is a letter and it's lowercase
        elif address_char > 9 and address[i].islower():
            # Check if the corresponding hash digit is 8 or higher
            if hash_char >= 8:
                return False

    return True