import hashlib

def hash_password(password):
    # FALLO: MD5 es débil (CWE-327)
    return hashlib.md5(password.encode()).hexdigest()