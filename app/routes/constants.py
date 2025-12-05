# Authentication route constants
import re

EMAIL_REGEX = re.compile(r"^[\w\.-]+@[\w\.-]+\.\w+$")
PASSWORD_REGEX = re.compile(
    r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
)
PASSWORD_REQUIREMENTS_MESSAGE = (
    "Password must be at least 8 characters long, contain uppercase and "
    "lowercase letters, a number, and a special character."
)

# Error messages
EMAIL_PASSWORD_REQUIRED_ERROR = "Email and password are required."
INVALID_EMAIL_FORMAT_ERROR = "Invalid email format."
EMAIL_ALREADY_REGISTERED_ERROR = "Email is already registered."
INVALID_EMAIL_OR_PASSWORD_ERROR = "Invalid email or password."
LOGIN_COMPLETION_ERROR = "Unable to complete login at this time."

# JWT configuration
JWT_EXPIRATION_MINUTES_CONFIG_KEY = "JWT_EXPIRATION_MINUTES"
JWT_SECRET_KEY_CONFIG_KEY = "JWT_SECRET_KEY"
JWT_DEFAULT_EXPIRATION_MINUTES = 60
JWT_ALGORITHM = "HS256"

# JWT payload keys
JWT_SUBJECT_KEY = "sub"
JWT_EMAIL_KEY = "email"
JWT_ISSUED_AT_KEY = "iat"
JWT_EXPIRATION_KEY = "exp"

