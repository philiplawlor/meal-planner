from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# MongoDB connection
client = MongoClient(os.getenv('MONGODB_URI'))
db = client['Recipes']

# Source and destination collections
source_collection = db['Foods']
dest_collection = db['recipes']

# Clear destination collection first
print("Clearing destination collection...")
dest_collection.delete_many({})

# Copy data
print("Copying meals from Foods to recipes...")
for meal in source_collection.find({}, {'_id': 0}):
    try:
        # Convert any datetime fields to strings
        if 'created_at' in meal:
            meal['created_at'] = meal['created_at'].isoformat()
        if 'updated_at' in meal:
            meal['updated_at'] = meal['updated_at'].isoformat()
        
        # Insert into destination collection
        dest_collection.insert_one(meal)
        print(f"Copied meal: {meal['name']}")
    except Exception as e:
        print(f"Error copying meal {meal.get('name', 'unknown')}: {str(e)}")

print("\nCopy complete!")
print(f"Total meals copied: {dest_collection.count_documents({})}")
