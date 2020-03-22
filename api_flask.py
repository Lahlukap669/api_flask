from flask import Flask, jsonify, request
import json
import hashlib
app = Flask(__name__)

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app.config['SQLALCHEMY_DATABASE_URI'] = "postgres://teecnvbl:ySNvS-XgSa_ql6SKZk87vdKyxwVKp3Ki@kandula.db.elephantsql.com:5432/teecnvbl"
db = SQLAlchemy(app)
migrate = Migrate(app, db)

#Users
##class Users(db.Model):
##    __tablename__ = 'users'
##
##    id = db.Column(db.Integer, primary_key=True)
##    ime = db.Column(db.String())
##    priimek = db.Column(db.String())
##    email = db.Column(db.String())
##    geslo = db.Column(db.String())
##
##    def __init__(self, ime, priimek, email, geslo):
##        self.ime = ime
##        self.priimek = priimek
##        self.email = email
##        self.geslo = geslo


@app.route("/", methods=['GET','POST'])
def index():
    if(request.method == 'POST'):
        podatki_json = request.get_json()
        print(podatki_json["ime"])
        return jsonify({'ime': podatki_json["ime"]}), 201
    else:
        return jsonify({'u sent':"nothing"})


##REGISTER
@app.route("/register/", methods=['GET','POST'])
def register():
    if(request.method == 'POST'):
        ##example of input data:
##        {
##          "ime": "Luka1",
##          "priimek": "Lah1",
##          "email": "luka1.lah@gmail.com",
##          "geslo": "Luka123"
##        }
        podatki_json = request.get_json()
        ##Deviding sent data
        ime = podatki_json["ime"]
        priimek = podatki_json["priimek"]
        email = podatki_json["email"]
        geslo = podatki_json["geslo"]
        ##converting from string to byte
        geslo = bytes(geslo, 'utf-8')
        ##Hashing
        geslo_h = hashlib.sha256(geslo).hexdigest()

##interaction db
        try:
            ##Called function
            db.session.execute("""SELECT register('%s', '%s', '%s', '%s');"""%(ime, priimek, email, geslo_h))
            db.session.commit()
            ##Returned data to program
            return True, 201                
        except Exception as e:
            print(e)
            return False, 404       
    else:
        return "u sent cant use GET"





##LOGIN
@app.route("/login/", methods=['GET','POST'])
def login():
    if(request.method == 'POST'):
        ##example of input data:
##        {
##          "email": "luka1.lah@gmail.com",
##          "geslo": "Luka123"
##        }
        podatki_json = request.get_json()
        ##Deviding sent data
        email = podatki_json["email"]
        geslo = podatki_json["geslo"]
        ##converting from string to byte
        geslo = bytes(geslo, 'utf-8')
        ##Hashing
        geslo_h = hashlib.sha256(geslo).hexdigest()
##interaction db
        try:
            ##Called function
            r = db.session.execute("""SELECT login('%s', '%s');"""%(email, geslo_h)).scalar()
            db.session.commit()
            if(r==True):
                return True, 201
            ##Returned data to program
            else:
                return False                
        except Exception as e:
            print(e)
            return "error", 404       
    else:
        return "u sent nothing"



##new_user = Users(ime=ime, priimek=priimek, email=email, geslo=geslo_h)
##db.session.add(new_user)
##db.session.add("SELECT register(%s, %s, %s, %s)"%(ime, priimek, email, geslo))#new_user)
##db.session.query("SELECT register(%s, %s, %s, %s)"%(ime, priimek, email, geslo))
##db.session.commit()

##@app.route("/multi/<int:num>", methods=['GET'])
##def multiply(num):
##    return jsonify({'u sent': num*10})

if __name__ == '__main__':
    app.run(debug=True)
