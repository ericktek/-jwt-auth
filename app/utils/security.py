from passlib.context import CryptContext

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    """Hashes the password using bcrypt."""
    return pwd_context.hash(password)

def verify_password(hashed_password: str, password: str) -> bool:
    """Verifies that the provided password matches the hashed password."""
    return pwd_context.verify(password, hashed_password)
