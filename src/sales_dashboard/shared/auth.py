from loguru import logger


def authenticate_user(username: str, password: str) -> bool:
    """
    Placeholder authentication function
    TODO: Implement with database
    """
    logger.debug(f"Authenticating user: {username}")
    # Hardcoded untuk development
    is_valid = username == "admin" and password == "admin123"

    if is_valid:
        logger.info(f"Authentication successful for user: {username}")
    else:
        logger.warning(f"Authentication failed for user: {username}")

    return is_valid


def validate_credentials(username: str, password: str) -> dict:
    """Validate user credentials and return user info"""
    if authenticate_user(username, password):
        return {
            "success": True,
            "username": username,
            "role": "admin",  # TODO: Get from database
        }
    return {"success": False, "message": "Invalid credentials"}
