from flask import Flask, request, redirect, render_template, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:build-a-blog@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(1200))

    def __init__(self, title, body):
        self.title = title
        self.body = body
        


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