# ============================================================
# Security utilities — password hashing and JWT
# ============================================================
from passlib.context import CryptContext
from jose            import JWTError, jwt
from datetime        import datetime, timedelta

# bcrypt is preferred over MD5/SHA-256 for passwords because:
# - It is intentionally slow (work factor), making brute-force attacks very expensive
# - MD5 and SHA-256 are designed to be FAST — bad for passwords
# - bcrypt automatically handles salting — no replay attacks
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY  = "super-secret-key-change-this-in-production-use-env-var"
ALGORITHM   = "HS256"
TOKEN_EXPIRY_MINUTES = 30


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire    = datetime.utcnow() + timedelta(minutes=TOKEN_EXPIRY_MINUTES)
    to_encode.update({"exp": expire})
    # JWT payloads are base64-encoded, NOT encrypted
    # Never put sensitive data (passwords, credit cards) in JWT payload
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str) -> dict:
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])