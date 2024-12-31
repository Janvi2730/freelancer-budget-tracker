from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for cross-origin requests

# Configure database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///budget.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Database model
class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    type = db.Column(db.String(20), nullable=False)  # "Income" or "Expense"

# Create database
with app.app_context():
    db.create_all()

# Routes
@app.route('/api/budget', methods=['POST'])
def add_transaction():
    data = request.get_json()
    if not data or 'description' not in data or 'amount' not in data or 'type' not in data:
        return jsonify({"error": "Invalid request"}), 400

    new_transaction = Transaction(
        description=data['description'],
        amount=data['amount'],
        type=data['type']
    )
    db.session.add(new_transaction)
    db.session.commit()
    return jsonify({"message": "Transaction added successfully"}), 201

@app.route('/api/budget', methods=['GET'])
def get_transactions():
    transactions = Transaction.query.all()
    return jsonify([
        {"id": t.id, "description": t.description, "amount": t.amount, "type": t.type}
        for t in transactions
    ])

if __name__ == '__main__':
    app.run(debug=True)
