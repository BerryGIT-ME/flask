from flask import Flask, render_template, jsonify

app = Flask(__name__)

@app.route('/')
def index():
  return jsonify({'message': "hello world"})

if __name__ == '__main__':
  app.run(port=5000)
