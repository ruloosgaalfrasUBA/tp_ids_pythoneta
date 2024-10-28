from flask import Flask, render_template , request , redirect ,url_for
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, scoped_session



engine = create_engine("mysql://root:root@localhost:(puerto en el que esta la base de datos/nombre ")

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
