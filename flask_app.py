import logging
from flask import Flask, request, render_template
import passwordgen
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
import os 
from werkzeug.security import generate_password_hash


app = Flask(__name__)


load_dotenv()
app.config['SECRET_KEY'] = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///passwordgen.db"
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
    #https://dev.to/goke/securing-your-flask-application-hashing-passwords-tutorial-2f0p
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)


with app.app_context():
    db.create_all()

    


@app.route('/')
def hello():
    app.logger.info("Received request")
    if request.scheme == 'http':
        app.logger.warning("INSECURE CONNECTION: Request made over HTTP")

    return render_template("home.html")

@app.route('/generate_password', methods=['GET'])
def generate_password():
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

    #TODO - Save password hashes and check to make sure the password wasn't generated before
    #Needs to match STIG compliance checks

    app.logger.info(f"Password generated: {password}")

    return render_template('passgen.html', passw=password)

if __name__ == "__main__":
    app.run(host='0.0.0.0')
    
#passgen PEM PASSPHRASE: n13e563"!:14$kdsa31;SAD


# https://gist.github.com/dahlsailrunner/679e6dec5fd769f30bce90447ae80081 

# sudo openssl req -x509 -nodes -days 365 -newkey rsa:3072 -keyout passgen.key -out passgn.crt -config passgen.conf

# sudo openssl req -x509 -nodes -days 365 -newkey rsa:3072 -keyout passgen.key -out passgen.crt -config passgen.conf -passin pass:n13e563!

# sudo openssl pkcs12 -export -out passgen.pfx -inkey passgen.key -in passgen.crt

# sudo openssl pkcs12 -in passgen.pfx -clcerts -out passgen.pem

# firefox - your certificates then import 

# sudo cp passgen.pem  /usr/local/share/ca-certificates/

# sudo update-ca-certificates
# trust list | grep -i "localhost"