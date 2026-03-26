import json
import os
from flask import Flask, jsonify, request

app = Flask(__name__)

# Load data from JSON file
DATA_FILE = os.path.join(os.path.dirname(__file__), 'data', 'customers.json')

def load_data():
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200

@app.route('/api/customers', methods=['GET'])
def get_customers():
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 10))
    
    customers = load_data()
    total = len(customers)
    
    start_idx = (page - 1) * limit
    end_idx = start_idx + limit
    
    paginated_data = customers[start_idx:end_idx]
    
    return jsonify({
        "data": paginated_data,
        "total": total,
        "page": page,
        "limit": limit
    })

@app.route('/api/customers/<id>', methods=['GET'])
def get_customer(id):
    customers = load_data()
    customer = next((c for c in customers if c['customer_id'] == id), None)
    
    if customer:
        return jsonify(customer)
    else:
        return jsonify({"error": "Customer not found"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
