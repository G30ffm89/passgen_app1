import logging
from flask import Flask, redirect, render_template, url_for
import passwordgen
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
import os 
from werkzeug.security import generate_password_hash


app = Flask(__name__)


load_dotenv()
app.config['SECRET_KEY'] = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('database')
#TODO - Need to check what the logging requirements for the STIG are TLS_AES_256_GCM_SHA384 tls 1.3 more secure than 1.2
#add back slashes
db = SQLAlchemy(app)


logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s',
                    handlers=[
                        logging.FileHandler("logs/flask_app.log"),
                        logging.StreamHandler()
                    ])

class Password(db.Model): #very hard to have duplicate passwords 
    id = db.Column(db.Integer, primary_key=True)
    password_hash = db.Column(db.String(128), unique=True, nullable=False)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)


with app.app_context():
    db.create_all()

#disable http2 


@app.route('/')
def home():
    # this checkes encase for whatever reason the hashed and salted password is already in the db, very unlikly but a precaution 
    app.logger.info("Received request")

    password = passwordgen.getpassword()

    new_password_entry = Password()
    new_password_entry.set_password(password)

    while True:
        password = passwordgen.getpassword()
        new_password_entry = Password()
        new_password_entry.set_password(password)

        try:
            db.session.add(new_password_entry)
            db.session.commit() 
            break  
        except SQLAlchemy.exc.IntegrityError:
            db.session.rollback()  
            app.logger.warning("Error rolling back ")

    #TODO - Save password hashes and check to make sure the password wasn't generated before the not possible due to the chance of two numbers matching 
    #Needs to match STIG compliance checks

    app.logger.info(f"Password generated: {password}")

    return render_template('passgen.html', passw=password)

@app.errorhandler(404) #404 redirects
def page_not_found(error):
    return redirect(url_for('home'))         

if __name__ == "__main__":
    app.run(host='0.0.0.0')
    
