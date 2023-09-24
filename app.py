from dotenv import load_dotenv
load_dotenv()
import os
from flask import Flask, request, jsonify, abort
from flask_cors import CORS
from services.chat import chatService

app = Flask(__name__)

# Enable CORS for all domains
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Custom error handler for 400 Bad Request
@app.errorhandler(400)
def bad_request_error(error):
    error_message = {
        "code": 400,
        "error": "Bad Request",
        "message": "The request is invalid"
    }

    return jsonify(error_message), 400

# Custom error handler for 500 Internal Server Error
@app.errorhandler(500)
def internal_server_error(error):
    error_message = {
        "code": 500,
        "error": "Internal Server Error",
        "message": "An unexpected error occured"
    }

    return jsonify(error_message), 500

@app.route('/api/v1/chat', methods=['POST'])
def controller():
    try:
        data = request.get_json()
    
        if not data["query_text"]:
            abort(400)

        answer = chatService(data['query_text'])
        result = {"code": 200, "data": answer}
        return jsonify(result), 200
    except:
        abort(500)


host = os.getenv("HOST")
port = os.getenv("PORT")

if __name__ == '__main__':
    app.run(host if host is not None else "0.0.0.0", port if port is not None else 4000)

