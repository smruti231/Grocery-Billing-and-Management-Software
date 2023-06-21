import sqlite3
def create_db():
    con=sqlite3.connect(database=r'BSW.db')                
    cur=con.cursor()                            

    cur.execute("CREATE TABLE IF NOT EXISTS user(uid INTEGER PRIMARY KEY AUTOINCREMENT,name text,email text,gender text,contact text,dob text,doj text,utype text,address text,salary text, password text)")  
    con.commit()

    cur.execute("CREATE TABLE IF NOT EXISTS category(CID INTEGER PRIMARY KEY AUTOINCREMENT,name text)")
    con.commit()

    cur.execute("CREATE TABLE IF NOT EXISTS supplier(SupplierID INTEGER PRIMARY KEY AUTOINCREMENT,name text,contact text,desc text)")  
    con.commit()

    cur.execute("CREATE TABLE IF NOT EXISTS product(pid INTEGER PRIMARY KEY AUTOINCREMENT,Category text,Supplier text,name text,price text,qty text,status text)")  
    con.commit()

create_db()
