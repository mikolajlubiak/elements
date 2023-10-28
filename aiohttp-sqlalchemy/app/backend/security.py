from passlib.hash import argon2

def generate_password_hash(password):
    return argon2.hash(password)

def check_password_hash(hashed, password):
    return argon2.verify(password, hashed)

