#!/usr/bin/env python3
"""
Basic Flask app.
"""
from flask import Flask, jsonify, request, abort, redirect
from auth import Auth

app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    """Return a welcome message."""
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'])
def users():
    """Register a user."""
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
