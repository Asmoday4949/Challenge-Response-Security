# Project
#   Small CHAP logic example
#
# Date
#   09.03.2019
#
# Author
# - Malik Fleury
# - Bastien Wermeille

# Quel hachage cryptographique utilisez-vous et pourquoi ?
#
# Quelles précautions pour le générateur aléatoire ?
#
# Quelles précautions pour la construction garantissant l'unicité du nonce ?
#
# Quelles précautions pour la durée de validité du nonce ?
#

import secrets
import hashlib

def hash_function(password):
    # Use hexdigest to facilitate display
    return hashlib.shake_256(bytes(password)).hexdigest()

class Client:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def connect(self, server):
        print(self.username + " connect to " + server.username)
        nonce = server.get_nonce(self.username)

        # Hash password
        hashed_pass = hash_function(str(nonce) + self.username)
        server.auth(self.username, hashed_pass)

        server.send_message()

class Server:
    def __init__(self, username, password_database):
        self.username = username
        self.password_database = password_database
        self.nonce_database = {}
        self.rng = secrets.SystemRandom();

    def get_nonce(self, username):
        nonce = self.rng.random()
        self.nonce_database[username] = {
            'validity':12,
            'value': nonce
        }
        return nonce

    def auth(self, username, hashed_pass):
        try:
            # Check validity
            self.nonce_database[username]['validity']
            nonce = self.nonce_database[username]['value']
            hashed_pass_server = hash_function(nonce+username)
            return hashed_pass_server == hashed_pass
        except Exception:
            return False

    def send_message(self):
        pass

if __name__ == '__main__':
    #TODO

    password_database = {
        'Alice': 'a9d9gV!@P8L)<=a?[kMGV]\>AGe-~dFbuTE]u<qv/`F5Tcf7m/',
        'Jon': '9-a/3s\~UQ@R-tq3=qJDAy)MFbAg68Psf\f59g,F*hQ`*R6#+c',
        'Emilia': '9-a/3s\~UQ@R-tq3=qJDAy)MFbAg68Psf\f59g,F*hQ`*R6#+c'
    }

    alice = Client('Alice', password_database['Alice'])
    bob = Server('Bob', password_database)

    alice.connect(bob)
