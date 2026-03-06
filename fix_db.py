import sqlite3
import os

# Paths to your database files
AUTH_DB = "auth.db"
TODO_DB = "todo.db"

def add_column(db_path, table, column_def):
    if not os.path.exists(db_path):
        print(f"⚠️ {db_path} not found. Skipping...")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        cursor.execute(f"ALTER TABLE {table} ADD COLUMN {column_def}")
        conn.commit()
        print(f"✅ Added column to {table} in {db_path}: {column_def}")
    except sqlite3.OperationalError as e:
        if "duplicate column name" in str(e):
            print(f"ℹ️ Column already exists in {table} ({db_path})")
        else:
            print(f"❌ Error altering {table} in {db_path}: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    print("🔧 Starting Database Migration...")
    
    # Update Users Table
    add_column(AUTH_DB, "users", "updated_at DATETIME")
    
    # Update Todos Table
    add_column(TODO_DB, "todos", "task_date DATE")
    add_column(TODO_DB, "todos", "start_time TIME")
    add_column(TODO_DB, "todos", "end_time TIME")
    add_column(TODO_DB, "todos", "email_sent BOOLEAN DEFAULT 0")
    
    print("\n🎉 Migration Finished! You can now restart your server.")