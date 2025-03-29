from flask import Flask, jsonify
app = Flask(__name__)

MOCK_DATA = {
    "nodes": [
        {
            "id": 6,
            "properties": {"age": 28, "name": "Alice"},
            "type": "Person"
        },
        {
            "id": 7,
            "properties": {"age": 32, "name": "Bob"},
            "type": "Person"
        },
        {
            "id": 8,
            "properties": {"age": 25, "name": "Charlie"},
            "type": "Person"
        },
        {
            "id": 9,
            "properties": {"founded": 2010, "name": "TechCorp"},
            "type": "Company"
        },
        {
            "id": 10,
            "properties": {"founded": 2015, "name": "DataInc"},
            "type": "Company"
        }
    ],
    "relationships": [
        {
            "source": 6,
            "target": 9,
            "type": "WORKS_AT"
        },
        {
            "source": 6,
            "target": 7,
            "type": "KNOWS"
        },
        {
            "source": 7,
            "target": 9,
            "type": "WORKS_AT"
        },
        {
            "source": 8,
            "target": 10,
            "type": "WORKS_AT"
        },
        {
            "source": None,
            "target": None,
            "type": None
        },
        {
            "source": None,
            "target": None,
            "type": None
        }
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
