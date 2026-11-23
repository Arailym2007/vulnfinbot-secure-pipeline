import ast
import hashlib
import os
import subprocess


def get_db_password():
    return os.environ.get("DB_PASSWORD", "")


def calculate(expression):
    # Safe evaluation of literals only
    return ast.literal_eval(expression)


def run_command(user_input):
    # No shell, arguments passed as a list
    return subprocess.run(["echo", user_input], check=False)


def strong_hash(password):
    return hashlib.sha256(password.encode()).hexdigest()


def start(app):
    app.run(host="127.0.0.1", debug=False)