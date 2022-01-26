#from crypt import methods
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import null
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db = SQLAlchemy(app)

class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(20), nullable=False, default='N/A')
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return 'Blog Post: '+ str(self.id)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/posts', methods=['GET'])
def posts():
    all_posts = BlogPost.query.order_by(BlogPost.date_posted.desc()).all()
    return render_template('posts.html', posts = all_posts)

@app.route('/posts/delete/<int:id>')
def delete(id):
    post = BlogPost.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    return redirect('/posts')

@app.route('/posts/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    post = BlogPost.query.get_or_404(id)
    
    if request.method == 'POST':
        #receive all the items from the form
        post.title = request.form['title']
        post.content = request.form['content']
        post.author = request.form['author']

        #update enrties to the database
        db.session.commit()

        #after successful entry to the database redirect the user to post page
        return redirect('/posts')
    else:
        return render_template('update.html', post=post)

@app.route('/posts/create', methods=['GET','POST'])
def create():
    if request.method == 'POST':
        #receive all the items from the form
        title = request.form['title']
        content = request.form['content']
        author = request.form['author']
        
        #create new BlogPost object with all the new form entries
        new_post = BlogPost(title=title, content=content, author=author)

        #add new enrties to the database
        db.session.add(new_post)
        db.session.commit()

        #after successful entry to the database redirect the user to post page
        return redirect('/posts')
    else:
        return render_template('create.html')


if __name__ == '__main__':
    app.run(debug=True) 