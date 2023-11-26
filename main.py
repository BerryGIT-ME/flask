from dotenv import load_dotenv
load_dotenv()
from flask import Flask, jsonify, request
from llm.llm_agent import ai_chat
from flask_cors import CORS
from validate import valid_data



app = Flask(__name__)
CORS(app)

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
        return jsonify({"chat": {"role": "assistant", "content": "An unexpected error has occurred"}, "suggestions": []})

if __name__ == '__main__':
  app.run(port=5000)
