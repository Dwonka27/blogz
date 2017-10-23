from flask import Flask, request, redirect, render_template, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:blogz@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(1200))
    owner_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def __init__(self, title, body, owner):
        self.title = title
        self.body = body
        self.owner = owner

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    blogs = db.relationship('Blog', backref='owner')

    def __init__(self, username, password):
        self.username = username
        self.password = password

@app.route("/signup", methods=["POST", "GET"])
def signup():

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        verify = request.form["verify"]

        existing_user = User.query.filter_by(username=username).first()
        if not existing_user:
            new_user = User(username, password)
            db.session.add(new_user)
            db.session.commit()
            session["username"] = username     
        else:
            return "<h1>User Already Exist.</h1>"

    return render_template("signup.html")


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            session["username"] = username
            flash("Logged in")
            return redirect("/")
        else:
            flash("User Password incorrect or User does not exist", "error")
    
    return render_template("login.html")



@app.route("/blog", methods=["POST", "GET"])
def index():

    if request.method == "POST":
        title = request.form["title"]
        body = request.form["body"]

    blogs = Blog.query.all()   

    return render_template("blog.html", blogs = blogs )


@app.route("/newpost", methods=["POST", "GET"])
def newpost():

    if request.method == "POST":
        body = request.form["body"]
        title = request.form["title"]
        if len(title) == 0:
            return render_template("newpost.html", error="Please fill in this body")

        if len(body) == 0:
            return render_template("newpost.html", error="Please fill in this body")
        
        
        new_post = Blog(title, body)
        db.session.add(new_post)
        db.session.commit()
        return redirect("/blog") 
    


    return render_template("newpost.html" )

@app.route("/post")
def post():
    
    single = request.args.get("p")

    solo = Blog.query.get(single)
    
    return render_template("post.html", solo=solo )
    


if __name__ == '__main__':
    app.run()