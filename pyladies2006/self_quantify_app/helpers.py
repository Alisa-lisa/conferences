from passlib.context import CryptContext
import os


algo = os.getenv.get("HASH_ALGO", "des_crypt")


hasher = CryptContext(schemes=[algo])
