from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import  asc

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    rank = db.Column(db.Integer,nullable=False)
   
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Article %r>' % self.id


@app.route('/')
@app.route('/home')
def index():
    return render_template("index.html")


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/posts')
def posts():
    articles = Article.query.order_by(asc(Article.rank)).all()
    #articles = Article.query.order_by(desc(Article.rank.asc())).all()
    return render_template("posts.html", articles=articles)


@app.route('/posts/<int:id>')
def post_detail(id):
    article = Article.query.get(id)
    return render_template("post_detail.html", article=article)


@app.route('/posts/<int:id>/del')
def post_delete(id):
    article = Article.query.get_or_404(id)

    try:
        db.session.delete(article)
        db.session.commit()
        return redirect('/posts')
    except:
        return 'An error occurred while deleting the article'


@app.route('/posts/<int:id>/update', methods=['POST', 'GET'])
def create_update(id):
    article = Article.query.get(id)
    if request.method == 'POST':
        article.title = request.form['title']
        article.rank = request.form['rank']
        article.text = request.form['text']

        try:
            db.session.commit()
            return redirect('/posts')
        except:
            return "An error occurred while editing the article"
    else:

        return render_template("post_update.html", article=article)


@app.route('/create-article', methods=['POST', 'GET'])
def create_article():
    if request.method == 'POST':
        title = request.form['title']
        rank = request.form['rank']
        text = request.form['text']

        article = Article(title=title, rank=rank, text=text)

        try:
            db.session.add(article)
            db.session.commit()
            return redirect('/posts')
        except:
            return "An error occurred while adding the article"
    else:
        return render_template("create_article.html")


if __name__ == '__main__':
    app.run(debug=True)