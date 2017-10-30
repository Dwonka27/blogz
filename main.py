from flask import Flask, request, redirect, render_template, flash, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:blogz@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = "sajsadiofewojwosdosdjio"


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

@app.before_request
def require_login():
    allowed_routes = ["login", "signup", "blog"]

    if request.endpoint not in allowed_routes and "username" not in session:
        return redirect("/login")



@app.route("/signup", methods=["POST", "GET"])
def signup():

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        verify = request.form["verify"]

        existing_user = User.query.filter_by(username=username).first()
        if not existing_user:
            if password == verify:
                new_user = User(username, password)
                db.session.add(new_user)
                db.session.commit()
                session["username"] = username
                return redirect("/newpost")     
            else:
                flash("Passwords do not match.", "error")
            #successfully rerouted to new post page!
        else:
            flash("User Already Exist.", "error")

    #changed render from signup to home       
    return render_template("signup.html")
    #successfully rerouted to new post page!

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            session["username"] = username
            flash("Logged in")
            #changed redirect to "/newpost" rather than "/"(index)
            return redirect("/newpost")
        else:
            flash("User Password incorrect or User does not exist", "error")
    
    return render_template("login.html")


@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")


@app.route("/blog", methods=["POST", "GET"])
def blog():
    
    userid = request.args.get("id")
    
    if userid:
        
        allofit = User.query.get(userid)
        owner = Blog.query.filter_by(owner=allofit).all()
        return render_template("allofit.html", blogs=owner)

    blogs = Blog.query.all()   

    return render_template("blog.html", blogs = blogs )


@app.route("/newpost", methods=["POST", "GET"])
def newpost():

    if request.method == "POST":
        body = request.form["body"]
        title = request.form["title"]
        # Adding owner variable and not sure about how to query it...
        owner = User.query.filter_by(username=session["username"]).first()
        if len(title) == 0:
            return render_template("newpost.html", error="Please fill in this body")

        if len(body) == 0:
            return render_template("newpost.html", error="Please fill in this body")
        
        
        new_post = Blog(title, body, owner)
        db.session.add(new_post)
        db.session.commit()
        return redirect("/blog") 
    


    return render_template("newpost.html" )

@app.route("/post")
def post():
    
    single = request.args.get("p")

    solo = Blog.query.get(single)
   
    return render_template("post.html", solo=solo )

# Working on adding a home page with all of the Usernames from the database displayed!


@app.route("/", methods=["GET"])
def index():

    users = User.query.all()

    return render_template("home.html", users = users)
    # Definitely almost finished home page


if __name__ == '__main__':
    app.run()