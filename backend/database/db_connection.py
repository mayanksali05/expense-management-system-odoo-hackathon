from pymongo import MongoClient, ASCENDING
import gridfs

def init_db(app):
    """
    Initialize MongoDB connection, create GridFS for file storage,
    and create necessary indexes for collections.
    """
    # Connect to MongoDB
    client = MongoClient(app.config['MONGO_URI'])
    
    # Get the default database from the URI
    db = client.get_default_database()
    
    # Attach db and GridFS to Flask app
    app.db = db
    app.fs = gridfs.GridFS(db)  # for storing files if needed

    # ----------- Create Indexes -----------
    try:
        # Ensure email is unique for users
        db.users.create_index("email", unique=True)

        # For faster querying expenses by user and date
        db.expenses.create_index([("user_id", ASCENDING), ("created_at", ASCENDING)])

        # Index on status for quick filtering
        db.expenses.create_index("status")

        # Index on expense_id in approvals for quick lookup
        db.approvals.create_index("expense_id")

        print("✅ MongoDB indexes created successfully.")
    except Exception as e:
        print(f"⚠️ Error creating indexes: {e}")

    return db
