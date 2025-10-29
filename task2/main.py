import os
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from pymongo.errors import PyMongoError
from dotenv import load_dotenv

load_dotenv()

# Get credentials from environment variables
username = os.getenv("MONGO_USERNAME")
password = os.getenv("MONGO_PASSWORD")

if not username or not password:
    raise ValueError("Missing credentials")

# Construct connection URI
uri = f"mongodb+srv://{username}:{password}@cluster0.gqzrq1f.mongodb.net/?appName=Cluster0"

# Connect to MongoDB
client = MongoClient(uri, server_api=ServerApi('1'))
db = client["task2"]
collection = db["cats"]

# Drop collection if it exists
if "cats" in db.list_collection_names():
    collection.drop()
    print("Dropped existing 'cats' collection.")

# Insert sample documents
try:
    result_many = collection.insert_many([
        {"name": "Barsik", "age": 3, "features": ["ходить в капці", "дає себе гладити", "рудий"]},
        {"name": "Lama", "age": 2, "features": ["ходить в лоток", "не дає себе гладити", "сірий"]},
        {"name": "Liza", "age": 4, "features": ["ходить в лоток", "дає себе гладити", "білий"]},
    ])
    print("Inserted IDs:", result_many.inserted_ids)
except PyMongoError as e:
    print("Error inserting documents:", e)

# === CRUD FUNCTIONS ===
def read_all_cats():
    """Print all cat documents."""
    try:
        found = False
        for cat in collection.find():
            print(cat)
            found = True
        if not found:
            print("Collection is empty.")
    except PyMongoError as e:
        print("Error reading cats:", e)

def read_cat_by_name(name):
    """Print a cat document by name."""
    try:
        cat = collection.find_one({"name": name})
        if cat:
            print(cat)
        else:
            print(f"No cat found with name '{name}'.")
    except PyMongoError as e:
        print("Error reading cat:", e)

def update_cat_age(name, new_age):
    """Update the age of a cat by name."""
    try:
        result = collection.update_one({"name": name}, {"$set": {"age": new_age}})
        if result.matched_count:
            print(f"Updated age of '{name}' to {new_age}.")
        else:
            print(f"No cat found with name '{name}'.")
    except PyMongoError as e:
        print("Error updating age:", e)

def add_cat_feature(name, feature):
    """Add a new feature to a cat's features array."""
    try:
        result = collection.update_one({"name": name}, {"$addToSet": {"features": feature}})
        if result.matched_count:
            print(f"Added feature '{feature}' to '{name}'.")
        else:
            print(f"No cat found with name '{name}'.")
    except PyMongoError as e:
        print("Error adding feature:", e)

def delete_cat_by_name(name):
    """Delete a cat document by name."""
    try:
        result = collection.delete_one({"name": name})
        if result.deleted_count:
            print(f"Deleted cat '{name}'.")
        else:
            print(f"No cat found with name '{name}'.")
    except PyMongoError as e:
        print("Error deleting cat:", e)

def delete_all_cats():
    """Delete all cat documents."""
    try:
        result = collection.delete_many({})
        print(f"Deleted {result.deleted_count} cats from the collection.")
    except PyMongoError as e:
        print("Error deleting all cats:", e)

# === Example usage ===
if __name__ == "__main__":
    print("\n--- READ ALL CATS ---")
    read_all_cats()

    print("\n--- READ BY NAME ---")
    read_cat_by_name("Barsik")

    print("\n--- UPDATE AGE ---")
    update_cat_age("Lama", 5)
    read_cat_by_name("Lama")

    print("\n--- ADD FEATURE ---")
    add_cat_feature("Liza", "любить спати")
    read_cat_by_name("Liza")

    print("\n--- DELETE CAT ---")
    delete_cat_by_name("Liza")
    read_all_cats()

    print("\n--- DELETE ALL CATS ---")
    delete_all_cats()
    read_all_cats()   # Collection is empty.