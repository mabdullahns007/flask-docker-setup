import re

EMAIL_REGEX = re.compile(r"^[\w\.-]+@[\w\.-]+\.\w+$")
PASSWORD_REGEX = re.compile(
    r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
)
PASSWORD_REQUIREMENTS_MESSAGE = (
    "Password must be at least 8 characters long, contain uppercase and "
    "lowercase letters, a number, and a special character."
)

