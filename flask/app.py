# Copyright (c) 2024 Ali ihsan YILMAZ
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

from flask import Flask, jsonify, request, abort
from functools import wraps
import os
from dotenv import load_dotenv
from pusher import Pusher
from fatals import list_fatals, get_fatal_details, delete_fatal_error
from run import run_function

load_dotenv()

app = Flask(__name__)
app.config['ENV'] = os.getenv('ENV', 'production')

# Pusher Configuration
if os.getenv('PUSHER', 'False').lower() == 'true':
    app.pusher_client = Pusher(
        app_id=os.getenv('PUSHER_APP_ID'),
        key=os.getenv('PUSHER_KEY'),
        secret=os.getenv('PUSHER_SECRET'),
        cluster=os.getenv('PUSHER_CLUSTER')
    )
    print("Pusher configured successfully.")
else:
    app.pusher_client = None
    print("Pusher is disabled.")

# Security Header Value
AUTH_HASH = os.getenv('AUTH_HASH')

def require_auth(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_hash = request.headers.get('X-Auth-Hash')
        if not auth_hash:
            abort(401, description="Authentication hash is missing")
        
        if auth_hash != AUTH_HASH:
            abort(401, description="Invalid authentication hash")
        
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def hello():
    return "Hello, Flask application is running!"

@app.route('/run', methods=['POST'])
@require_auth
def run():
    return run_function()

@app.route('/fatals', methods=['GET'])
@require_auth
def fatals():
    return list_fatals()

@app.route('/fatals/<filename>', methods=['GET'])
@require_auth
def fatal_details(filename):
    return get_fatal_details(filename)

@app.route('/fatals/<filename>', methods=['DELETE'])
@require_auth
def delete_fatal(filename):
    return delete_fatal_error(filename)

if __name__ == '__main__':
    debugMode = app.config['ENV'] == 'development'
    print(f"Debug mode: {debugMode}")
    app.run(host='0.0.0.0', port=5000, debug=debugMode)
