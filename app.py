from flask import Flask,render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import  datetime
from medichain_model import predictDisease

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
res = None
with app.app_context():
    db = SQLAlchemy(app)
class Todo(db.Model):
    
    sno = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(200), nullable = False)
    desc = db.Column(db.String(200), nullable = False)
    date_created = db.Column(db.DateTime, default = datetime.utcnow)
    
    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"
@app.route('/')
def hello_world():  
    return render_template('index.html')

@app.route('/symp', methods=['GET', 'POST'])
def products():
    if(request.method=="POST"):
        multiselect = request.form.getlist('symptoms')
        listToStr = ','.join(map(str, multiselect))
        res = predictDisease(listToStr)
        return render_template('symptom.html', res=res)
    return render_template('symptom.html')

@app.route('/login')    
def login():
    return render_template('signup-login.html')

if __name__ == "__main__":
    app.run(debug = True,port = 5000) 