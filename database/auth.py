import hashlib
import hmac
import secrets
import sqlite3

from database.db import get_connection


def hash_password(password):
    """Hash a password securely using PBKDF2."""

    salt = secrets.token_bytes(16)

    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        100_000
    )

    return f"{salt.hex()}${password_hash.hex()}"


def verify_password(password, stored_hash):
    """Verify a password against the stored hash."""

    try:
        salt_hex, hash_hex = stored_hash.split("$")

        salt = bytes.fromhex(salt_hex)
        stored_password_hash = bytes.fromhex(hash_hex)

        password_hash = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            salt,
            100_000
        )

        return hmac.compare_digest(
            password_hash,
            stored_password_hash
        )

    except (ValueError, TypeError):
        return False


def create_user(username, email, password):
    """Create a new user."""

    conn = get_connection()
    cursor = conn.cursor()

    password_hash = hash_password(password)

    try:
        cursor.execute(
            """
            INSERT INTO users (username, email, password_hash)
            VALUES (?, ?, ?)
            """,
            (username, email, password_hash)
        )

        conn.commit()

        return True, "Account created successfully!"

    except sqlite3.IntegrityError:
        return False, "Username or email already exists."

    finally:
        conn.close()


def authenticate_user(username, password):
    """Authenticate a user."""

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id, username, email, password_hash
        FROM users
        WHERE username = ?
        """,
        (username,)
    )

    user = cursor.fetchone()

    conn.close()

    if user and verify_password(password, user["password_hash"]):

        return {
            "id": user["id"],
            "username": user["username"],
            "email": user["email"]
        }

    return None