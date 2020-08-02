from passlib.context import CryptContext
import os


algo = os.environ.get("HASH_ALGO", "des_crypt")
hasher = CryptContext(schemes=[algo])
