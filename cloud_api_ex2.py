from flask import Flask, jsonify
app = Flask(__name__)

MOCK_DATA = {
    "nodes": [
        {"id": 1, "type": "User", "properties": {"name": "Test User 1", "email": "user1@test.com"}},
        {"id": 2, "type": "User", "properties": {"name": "Test User 2", "email": "user2@test.com"}},
        {"id": 101, "type": "Post", "properties": {"title": "Test Post 1", "content": "Content 1"}},
        {"id": 102, "type": "Post", "properties": {"title": "Test Post 2", "content": "Content 2"}}
    ],
    "relationships": [
        {"source": 1, "target": 101, "type": "CREATED"},
        {"source": 2, "target": 102, "type": "CREATED"}
    ]
}

@app.route('/')
def home():
    return "Mock Cloud API is running!"

@app.route('/api/graph', methods=['GET'])
def get_graph():
    return jsonify(MOCK_DATA)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=False)
