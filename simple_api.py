from http.server import HTTPServer, SimpleHTTPRequestHandler
import urllib.parse
import json
import os
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# MongoDB connection
client = MongoClient(os.getenv('MONGODB_URI'))
db = client['Recipes']
collection = db['recipes']

class SimpleAPIHandler(SimpleHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_GET(self):
        if self.path == '/meals':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type')
            self.end_headers()
            
            # Fetch meals from MongoDB
            meals = []
            for meal in collection.find({}, {'_id': 0}):
                # Convert any datetime fields to strings
                if 'created_at' in meal:
                    meal['created_at'] = meal['created_at'].isoformat()
                if 'updated_at' in meal:
                    meal['updated_at'] = meal['updated_at'].isoformat()
                
                meals.append(meal)

            # Get unique values for filters
            cuisines = list(set(meal.get("cuisine", "") for meal in meals))
            difficulties = list(set(meal.get("difficulty", "") for meal in meals))
            dietary_info = list(set(
                info for meal in meals 
                for info in meal.get("dietary_info", [])
            ))

            response = {
                "meals": meals,
                "filters": {
                    "cuisines": cuisines,
                    "difficulties": difficulties,
                    "dietary_info": dietary_info
                }
            }

            self.wfile.write(json.dumps(response).encode('utf-8'))
        else:
            super().do_GET()

if __name__ == '__main__':
    server = HTTPServer(('localhost', 3001), SimpleAPIHandler)
    print('Starting simple API server on http://localhost:3001')
    server.serve_forever()
