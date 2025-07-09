#!/usr/bin/env python3
"""
Database creation script for Dustbin
Creates all tables with the correct schema including new columns
"""

from app import app, db, User, Paste, IPRateLimit

def create_database():
    """Create all database tables"""
    print("Creating database tables...")
    
    with app.app_context():
        # Drop all tables first (if they exist)
        db.drop_all()
        print("Dropped existing tables")
        
        # Create all tables with new schema
        db.create_all()
        print("Created new tables with updated schema")
        
        # Verify tables were created
        inspector = db.inspect(db.engine)
        tables = inspector.get_table_names()
        print(f"Created tables: {tables}")
        
        # Check columns for paste table
        if 'paste' in tables:
            columns = [col['name'] for col in inspector.get_columns('paste')]
            print(f"Paste table columns: {columns}")
            
            # Verify new columns exist
            required_columns = ['id', 'title', 'content', 'language', 'created_at', 
                              'expires_at', 'is_public', 'user_id', 'views', 'ip_address']
            missing_columns = [col for col in required_columns if col not in columns]
            
            if missing_columns:
                print(f"❌ Missing columns: {missing_columns}")
                return False
            else:
                print("✅ All required columns present")
        
        # Check IPRateLimit table
        if 'ip_rate_limit' in tables:
            columns = [col['name'] for col in inspector.get_columns('ip_rate_limit')]
            print(f"IPRateLimit table columns: {columns}")
        
        print("✅ Database created successfully!")
        return True

if __name__ == "__main__":
    success = create_database()
    if success:
        print("\n🎉 Database is ready!")
        print("You can now run: python app.py")
    else:
        print("\n❌ Database creation failed!")
        exit(1)
