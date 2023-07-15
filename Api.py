from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

# Initialize Flask app
app = Flask(__name__)
CORS(app)

@app.route('/generate_heat_map', methods=['POST'])
def generate_heat_map():

    # Database connection setup
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Create the customers table
    cursor.execute('''CREATE TABLE IF NOT EXISTS customers (
                    customer_id INTEGER PRIMARY KEY,
                    customer_name TEXT,
                    account_number TEXT
                )''')

    # Create the conversations table
    cursor.execute('''CREATE TABLE IF NOT EXISTS conversations (
                    conversation_id INTEGER PRIMARY KEY,
                    customer_id INTEGER,
                    conversation_text TEXT,
                    timestamp TIMESTAMP,
                    FOREIGN KEY (customer_id) REFERENCES customers (customer_id)
                )''')

    # Insert dummy data into the customers table
    cursor.execute("INSERT INTO customers (customer_id, customer_name, account_number) VALUES (1, 'A', '1234567890')")
    cursor.execute("INSERT INTO customers (customer_id, customer_name, account_number) VALUES (2, 'B', '9876543210')")
    cursor.execute("INSERT INTO customers (customer_id, customer_name, account_number) VALUES (3, 'C', '9876543290')")

    # Insert dummy data into the conversations table
    cursor.execute("INSERT INTO conversations (conversation_id, customer_id, conversation_text, timestamp) VALUES (1, 1, 'Hello, I have a question.', '2023-05-25 10:30:00')")
    cursor.execute("INSERT INTO conversations (conversation_id, customer_id, conversation_text, timestamp) VALUES (2, 1, 'I need assistance with my account.', '2023-05-25 11:45:00')")
    cursor.execute("INSERT INTO conversations (conversation_id, customer_id, conversation_text, timestamp) VALUES (3, 2, 'Hi, I want to inquire about a new product.', '2023-05-25 14:20:00')")
    cursor.execute("INSERT INTO conversations (conversation_id, customer_id, conversation_text, timestamp) VALUES (4, 2, 'Can you provide information on your services?', '2023-05-25 16:10:00')")
    customer_id = request.json.get('customer_id')

    # Check if the customer is new to the bank (no historical data)
    if is_new_customer(customer_id, cursor):
        return jsonify({'message': 'Customer is new to the bank and has no historical data.'}), 404

    # Check if the customer is an existing customer but has not made any calls
    if not has_call_history(customer_id, cursor):
        return jsonify({'message': 'Customer is an existing customer but has not made any calls.'}), 404

    # Retrieve conversation data for the customer from the database
    conversation_data = retrieve_conversation_data(customer_id, cursor)

    # Generate the heat map
    heat_map = generate_heat_map(customer_id)

    return jsonify({'heat_map': heat_map}), 200

    # Close the database connection
    conn.close()

def is_new_customer(customer_id, cursor):
    # Query the customer data from the database based on the customer_id
    query = "SELECT * FROM customers WHERE customer_id = ?"
    cursor.execute(query, (customer_id,))
    customer_data = cursor.fetchone()

    # Check if customer data is present
    if customer_data is None:
        return True
    else:
        return False

def has_call_history(customer_id, cursor):
    # Query the conversation data for the customer from the database based on the customer_id
    query = "SELECT * FROM conversations WHERE customer_id = ?"
    cursor.execute(query, (customer_id,))
    conversation_data = cursor.fetchall()

    # Check if any conversation data is present
    if len(conversation_data) > 0:
        return True
    else:
        return False

def retrieve_conversation_data(customer_id, cursor):
    # Query the conversation data for the customer from the database based on the customer_id
    query = "SELECT * FROM conversations WHERE customer_id = ?"
    cursor.execute(query, (customer_id,))
    conversation_data = cursor.fetchall()

    return conversation_data

def generate_heat_map(customer_id):
    # Generate the heat map 

    #heat_map = ... put the code here

    # returning dummy heat map data
    heat_map = {
        'customer_id': customer_id,
    }

    return heat_map

# Run the Flask app
if __name__ == '__main__':
    app.run()
