from flask import Flask,render_template,redirect,request
import chatbot
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/healthcare'
app.secret_key = 'b_5#y2L"F4Q8z\\;n\\xec/'
ChtBtLt = []
UsrLt = []

db = SQLAlchemy(app)

class userdetail(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    mobile = db.Column(db.String(20), nullable=False)

@app.route('/')
def home():
    ChtBtLt.clear()
    UsrLt.clear()
    info = userdetail.query.all()
    usernum = info[-1].id
    return render_template('home.html',usr = usernum)


@app.route('/ChatBt', methods=['GET','POST'])
def ChatBt():
    if(request.method=='POST'):
        msg = request.form.get('mesg')
        UsrLt.append(msg)
        ChtBtLt.append(chatbot.chat(msg=msg))
    return render_template('ChatBotPage.html',n=len(ChtBtLt),ChtBtLt=ChtBtLt,UsrLt=UsrLt)


@app.route('/reg', methods=['POST','GET'])
def reg():
    if(request.method=='POST'):
        name = request.form.get('name')
        add = request.form.get('address')
        mob = request.form.get('phone')
        entry = userdetail(name=name,address=add,mobile=mob)
        db.session.add(entry)
        db.session.commit()
        return render_template('ChatBotPage.html',n=len(ChtBtLt),ChtBtLt=ChtBtLt,UsrLt=UsrLt)
    return render_template('reg.html')

if __name__ == '__main__':
    app.run(debug=True)