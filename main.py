from flask import Flask, request
import json
import mysql.connector
from mysql.connector import Error

def connection():
  with open("dbcredentials.json", 'r') as file:
    creds = json.load(file)
  try:
    db = mysql.connector.connect(
      host=creds.get("Hostname"),
      database=creds.get("DatabaseName"),
      user=creds.get("Username"),
      password=creds.get("Password"),
      )
  except Error as e:
    print("Connection failed...")
    print(e)
    return None
  return db

app = Flask(__name__)

# insertion
@app.route("/insert", methods=['POST'])
def insertData():
  db = connection()
  cursor = db.cursor()
  name = request.form['name']
  age = int(request.form['age'])
  try:
    cursor.execute(f"insert into people(name, age) values('{name}', {age})")
    db.commit()
    db.close()
    return "Inserted successfully"
  except Exception as e:
    db.rollback()
    db.close()
    return "Insertion failed"

#updation
@app.route("/update", methods=['POST'])
def updateData():
  db = connection()
  cursor = db.cursor()
  name = request.form['name']
  age = int(request.form['age'])
  try:
    cursor.execute(f"update people set name='{name}', age={age} where name='{name}'")
    db.commit()
    db.close()
    return "Updated successfully"
  except Exception as e:
    db.rollback()
    db.close()
    return "Updation failed"

#deletion
@app.route("/delete", methods=['POST'])
def deleteData():
  db = connection()
  cursor = db.cursor()
  name = request.form['name']
  try:
    cursor.execute(f"delete from people where name='{name}'")
    db.commit()
    db.close()
    return "Deleted successfully"
  except Exception as e:
    db.rollback()
    db.close()
    return "Deletion failed"  

#selection
@app.route("/select")
def selectData():
  db = connection()
  cursor = db.cursor()
  try:
    cursor.execute(f"select * from people")
    result = cursor.fetchall()
    db.close()
    return str(result)
  except Exception as e:
    db.close()
    return "Selection failed" 

if __name__ == '__main__':
  app.run(debug=True)