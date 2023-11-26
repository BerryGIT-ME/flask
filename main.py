from dotenv import load_dotenv
load_dotenv()
from flask import Flask, jsonify, request
from llm.llm_agent import ai_chat
from flask_cors import CORS
from validate import valid_data
from db.vector_store.set_up_vector_store import vectorize_database
import sys



app = Flask(__name__)
CORS(app)

chat_error_message = "Hmmm I am currently having some difficulties communicating with our service please refresh the page and try again 🙏🏻"

@app.route('/update', methods=['POST'])
def update_db():
    data = request.get_json()
    try:
        passkey = data['key']
        if passkey == 'update-database':
            new_db = vectorize_database()
            new_db.save_local('./new_index')
            return jsonify({"message": "Ok"})
    except Exception as e:
        print(e, file=sys.stderr)
        return jsonify({"message": "Invalid request"}) 


@app.route('/check', methods=['GET', 'POST', 'PUT', 'PATCH'])
def healthcheck():
    return jsonify({"message": "Ok"})

@app.route('/api', methods=['GET'])
def hello_world():
    return jsonify({'message': 'The api is live!!!'})

@app.route('/api', methods=['POST'])
def chat_handler():
    try:
        data = request.get_json()
        if not valid_data(data): 
            return jsonify(
                {"chat": {"role": "assistant", "content": "It seems your request was not properly formatted"}, "suggestions": []}
            )
        
        

        messages = list(map(lambda x: x['chat'], data))
        response_text, suggestions = ai_chat(messages)
        
        
        return jsonify({"chat": {"role": "assistant", "content": response_text}, "suggestions": suggestions})
    except:
        return jsonify({"chat": {"role": "assistant", "content": chat_error_message}, "suggestions": []})

if __name__ == '__main__':
  app.run(port=5000)
