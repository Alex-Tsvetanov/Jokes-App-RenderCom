import grpc
from concurrent import futures
import time
import sys
import os
from flask import Flask, jsonify
from flask_cors import CORS
import threading

# Add generated proto files to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'proto'))

import jokes_pb2
import jokes_pb2_grpc
from db import Database

# Create Flask app for HTTP API
app = Flask(__name__)
CORS(app)  # Enable CORS for frontend

db = Database()

@app.route('/api/jokes', methods=['GET'])
def get_jokes():
    """HTTP endpoint to get all jokes"""
    try:
        jokes = db.get_all_jokes()
        return jsonify({'jokes': jokes})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy'})

class JokeServiceServicer(jokes_pb2_grpc.JokeServiceServicer):
    def __init__(self):
        self.db = Database()
    
    def StreamJokes(self, request, context):
        """Stream all jokes from database, one per second"""
        print("📡 Client connected, streaming jokes...")
        
        try:
            jokes = self.db.get_all_jokes()
            
            for joke_data in jokes:
                # Create a Joke message
                joke = jokes_pb2.Joke(
                    id=joke_data['id'],
                    setup=joke_data['setup'],
                    punchline=joke_data['punchline']
                )
                
                print(f"  → Sending joke #{joke_data['id']}: {joke_data['setup']}")
                yield joke
                
                # Wait 1 second before sending next joke
                time.sleep(1)
            
            print("✅ Finished streaming all jokes")
        except Exception as e:
            print(f"❌ Error streaming jokes: {e}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f'Error: {str(e)}')

def start_grpc_server():
    """Start gRPC server in a separate thread"""
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    jokes_pb2_grpc.add_JokeServiceServicer_to_server(JokeServiceServicer(), server)
    
    grpc_port = os.getenv('GRPC_PORT', '50051')
    server.add_insecure_port(f'0.0.0.0:{grpc_port}')
    
    print(f"🚀 Starting gRPC server on port {grpc_port}...")
    server.start()
    print(f"✅ gRPC server is running!")
    
    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        print("\n🛑 Shutting down gRPC server...")
        server.stop(0)

def serve():
    # Initialize database
    print("🔧 Initializing database...")
    db.init_db()
    
    # Start gRPC server in background thread
    grpc_thread = threading.Thread(target=start_grpc_server, daemon=True)
    grpc_thread.start()
    
    # Start Flask HTTP server on main thread
    port = int(os.getenv('PORT', '8000'))
    print(f"🚀 Starting HTTP server on port {port}...")
    print(f"✅ Server is running and ready to accept connections!")
    app.run(host='0.0.0.0', port=port, debug=False)

if __name__ == '__main__':
    serve()
