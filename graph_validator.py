from neo4j import GraphDatabase
import requests
import hashlib
import json

# python "C:\Users\aryan\OneDrive\Documents\VSCodeProjects\GraphValidation\.venv\Scripts\graph_validator.py"

class GraphValidator:
    def __init__(self):
        self.memgraph_uri = "bolt://localhost:7687"
        self.cloudapi_url = "http://localhost:5000/api/graph"
        self.driver = GraphDatabase.driver(self.memgraph_uri)

    def get_memgraph_data(self):
        try:
            with self.driver.session() as session:
                query = """
                MATCH (n)
                OPTIONAL MATCH (n)-[r]->(m)
                WITH collect(distinct {
                    id: id(n),
                    type: labels(n)[0],
                    properties: properties(n)
                }) as nodes,
                collect(distinct {
                    source: id(startNode(r)),
                    target: id(endNode(r)),
                    type: type(r)
                }) as relationships
                RETURN {nodes: nodes, relationships: relationships} as result
                """
                result = session.run(query)
                data = result.single()['result']               
                return data
        except Exception as e:
            print(f"Memgraph error: {str(e)}")
            return None

    def get_cloudapi_data(self):
        try:
            response = requests.get(self.cloudapi_url)
            if response.status_code == 200:
                data = response.json()
                return data
            raise Exception(f"API returned status code: {response.status_code}")
        except Exception as e:
            print(f"CloudAPI error: {str(e)}")
            return None

    def compute_checksum(self, data):
        if data is None:
            return None
        normalized = json.dumps(data, sort_keys=True)
        return hashlib.sha256(normalized.encode('utf-8')).hexdigest()

    def validate(self):
        try:
            memgraph_data = self.get_memgraph_data()
            cloudapi_data = self.get_cloudapi_data()

            if memgraph_data is None or cloudapi_data is None:
                return False

            memgraph_checksum = self.compute_checksum(memgraph_data)
            cloudapi_checksum = self.compute_checksum(cloudapi_data)

            print(f"\nMemgraph checksum: {memgraph_checksum}")
            print(f"CloudAPI checksum: {cloudapi_checksum}")

            return memgraph_checksum == cloudapi_checksum

        except Exception as e:
            print(f"Validation error: {str(e)}")
            return False

    def close(self):
        self.driver.close()

def main():
    validator = GraphValidator()
    try:
        print("\nStarting validation...")
        result = validator.validate()
        print(f"\nValidation {'successful' if result else 'failed'}")
    finally:
        validator.close()

if __name__ == "__main__":
    main()
