from flask import request


class _Field:
    def __init__(self, data):
        self.data = data


class LoginForm:
    """Minimal form object that mirrors Flask-WTF's login usage pattern."""

    def __init__(self):
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        remember_raw = request.form.get("remember_me", "")
        remember = str(remember_raw).lower() in {"1", "true", "on", "yes"}

        self.email = _Field(email)
        self.password = _Field(password)
        self.remember_me = _Field(remember)

    def validate_on_submit(self):
        if request.method != "POST":
            return False
        return bool(self.email.data and self.password.data)
