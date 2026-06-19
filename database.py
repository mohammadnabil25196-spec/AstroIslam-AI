import sqlite3

def get_db_connection():
    conn = sqlite3.connect('astroislam.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    
    # Users Table banana
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            otp TEXT,
            is_verified INTEGER DEFAULT 0,
            status TEXT DEFAULT 'user'
        )
    ''')
    
    # Knowledge Base Table banana (Aapka custom data)
    conn.execute('''
        CREATE TABLE IF NOT EXISTS knowledge_base (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT NOT NULL,
            answer TEXT NOT NULL,

            hawala TEXT NOT NULL
        )
    ''')
    
    # Master Admin Account create karna (Agar pehle se na ho)
    try:
        conn.execute('''
            INSERT INTO users (email, password, is_verified, status) 
            VALUES ('astroislam0@gmail.com', 'AstroNabil@786', 1, 'admin')
        ''')
        print("👑 Master Admin Account created successfully!")
    except sqlite3.IntegrityError:
        # Email pehle se exist karti hai toh error ignore karein
        pass
        
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
    print("📋 Database system initialized perfect!")
