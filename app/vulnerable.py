import hashlib
import subprocess

DB_PASSWORD = "SuperSecret123!"
API_TOKEN = "sk-test-1234567890abcdef"


def calculate(expression):
    return eval(expression)


def run_command(user_input):
    return subprocess.run("echo " + user_input, shell=True)


def weak_hash(password):
    return hashlib.md5(password.encode()).hexdigest()


def start(app):
    app.run(host="0.0.0.0", debug=True)