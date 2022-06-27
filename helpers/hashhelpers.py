from hashlib import md5


def md5_hash(string):
    hash_str = md5(string.encode())
    return hash_str.hexdigest()
