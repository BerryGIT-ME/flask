from dotenv import load_dotenv
load_dotenv()
from flask import Flask, jsonify, request
from db.vector_store.set_up_vector_store import get_image_vector_from_file, get_similarity
import pandas as pd
from llm.llm_agent import ai_chat
from flask_cors import CORS
from validate import valid_data
from db.vector_store.set_up_vector_store import vectorize_database
from werkzeug.utils import secure_filename
import sys
import os


app = Flask(__name__)
CORS(app)

chat_error_message = "Hmmm I am currently having some difficulties communicating with our service please refresh the page and try again 🙏🏻"
wrong_file_upload_message = "The only file formats we support at this time are .jpg and .jpeg. Please make sure the image you uploaded is one of those."
ALLOWED_EXTENSIONS = {'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/image-upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "Improper request format", 400

    file = request.files['file']
    file_name = file.filename
    current_script_path = os.path.abspath(__file__)
    current_base_dir = "/".join(current_script_path.split('/')[:-1])
    image_dir = current_base_dir + '/images'

    # print(image_dir, file=sys.stderr)
    if file and allowed_file(file_name):
        file_name = secure_filename(file_name)
        file_path = os.path.join(image_dir, file_name)
        file.save(file_path)

        # make inference from file
        merged_products = pd.read_pickle('./images_index/product_map.pkl')
        embeddings = pd.read_pickle('./images_index/image_embeddings.pkl').T

        test_image_embeddings = get_image_vector_from_file(file_path)
        ids = get_similarity(embeddings, test_image_embeddings, 3)

        results = merged_products[merged_products['product_id'].isin(ids)]
        suggestions = [v for k,v in results.T.to_dict().items()]
        os.remove(file_path)
        return jsonify({"chat": {"role": "assistant", "content": "Here are some of the closest matches for that image"}, "suggestions": suggestions})
    else: 
        return jsonify({"chat": {"role": "assistant", "content": wrong_file_upload_message}, "suggestions": []})
    

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
