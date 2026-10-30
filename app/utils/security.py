import functools
from flask import session
from werkzeug.security import generate_password_hash, check_password_hash
from app.utils.errors import unauthorized

def hash_password(password: str) -> str:
    """Hashes a password securely using PBKDF2/SHA256 via Werkzeug."""
    return generate_password_hash(password, method='scrypt')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies a plain password against the stored secure hash."""
    return check_password_hash(hashed_password, plain_password)

def login_required(view_func):
    """Decorator to enforce active session authentication on API routes."""
    @functools.wraps(view_func)
    def wrapped_view(*args, **kwargs):
        if 'user_id' not in session:
            return unauthorized("Please log in to access this feature.")
        return view_func(*args, **kwargs)
    return wrapped_view

