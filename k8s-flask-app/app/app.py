import os
from flask import Flask, jsonify
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)

# Database connection parameters from environment variables
DB_HOST = os.environ.get('DB_HOST', 'postgres')
DB_PORT = os.environ.get('DB_PORT', '5432')
DB_NAME = os.environ.get('DB_NAME', 'postgres')
DB_USER = os.environ.get('DB_USER', 'postgres')
DB_PASSWORD = os.environ.get('DB_PASSWORD', 'postgres')

def get_db_connection():
    """Create a database connection"""
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    conn.autocommit = True
    return conn

@app.route('/')
def index():
    return jsonify({
        'message': 'Welcome to Flask-PostgreSQL Kubernetes Demo',
        'status': 'running'
    })

@app.route('/health')
def health():
    return jsonify({'status': 'healthy'})

@app.route('/db-test')
def db_test():
    try:
        # Attempt to connect to the database
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        # Create a test table if it doesn't exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS test_table (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Insert a test record
        cursor.execute("INSERT INTO test_table (name) VALUES ('test-record') RETURNING id, name, created_at")
        record = cursor.fetchone()
        
        # Close the connection
        cursor.close()
        conn.close()
        
        return jsonify({
            'message': 'Database connection successful',
            'record': record
        })
    except Exception as e:
        return jsonify({
            'message': 'Database connection failed',
            'error': str(e)
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    