from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# Replace <password> with your actual password
uri = "mongodb+srv://kumarkushagra777@cluster0.oakeu.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(f"Error: {e}")
