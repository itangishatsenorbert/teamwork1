from flask import Flask, render_template, redirect, url_for, request, flash, session 
import sqlite3
from flask import flask_mysqldb
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlite3 import Error

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a unique and secure key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Optional, to disable modification 
# Sample Data
articles = [
    {"id": 1, "title": "Introduction to Flask", "date_created": "2024-08-01"},
    {"id": 2, "title": "Building REST APIs", "date_created": "2024-08-05"},
    {"id": 3, "title": "Understanding Jinja2", "date_created": "2024-08-10"},
]

notifications = [
    {"message": "Welcome to your dashboard!", "date": "2024-08-12"},
    {"message": "New comment on your article.", "date": "2024-08-13"},
    {"message": "Your profile was updated.", "date": "2024-08-14"},
]
@app.route('/')
def indx():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        # Here you would typically save the data to a database
        # For this example, we'll just print it to the console
        print(f"Username: {username}, Email: {email}, Password: {password}")
        
        # Redirect to the login page after processing
        return redirect(url_for('login'))
    
    return render_template('signup.html')
def get_db_connection():
    try:
        # Replace 'database.db' with your database file name
        conn = sqlite3.connect('database.db')
        return conn
    except Error as e:
        print(e)
        return None

# Example usage of get_db_connection
conn = get_db_connection()
if conn:
    print("Connection successful")
else:
    print("Connection failed")

@app.route('/dashboard')
def dashboard():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('dashboard.html')
  # Pass recent articles and notifications to the template
    recent_articles = articles[-3:]  # Last 3 articles
    return render_template('dashboard.html', recent_articles=recent_articles, notifications=notifications)
   # Fetch recent articles and notifications from your database
    recent_articles = fetch_recent_articles()
    notifications = fetch_user_notifications()
    return render_template('dashboard.html', recent_articles=recent_articles, notifications=notifications)


@app.route('/about')
def aboutus():
    return render_template('about.html')
@app.route('/articles')
def article_list():
    articles = articles.query.all()
    return render_template('article_list.html', articles=articles)

@app.route('/article/<int:article_id>', methods=['GET', 'POST'])
def article_detail(article_id):
    article = article.query.get_or_404(article_id)
    comments = comment.query.filter_by(article_id=article_id).all()
    if request.method == 'POST':
        content = request.form['content']
        comment = comment(content=content, article_id=article_id, user_id=1)  # Assuming user_id=1 for now
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for('article_detail', article_id=article_id))
    return render_template('article_detail.html', article=article, comments=comments)

@app.route('/create_article', methods=['GET', 'POST'])
def create_article():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        article = article(title=title, content=content, user_id=1)  # Assuming user_id=1 for now
        db.session.add(article)
        db.session.commit()
        return redirect(url_for('article_list'))
    return render_template('create_article.html')
@app.route('/delete_article/<int:article_id>', methods=['POST'])
def delete_article(article_id):
    article = article.query.get_or_404(article_id)
    db.session.delete(article)
    db.session.commit()
    return redirect(url_for('article_list'))
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Check if credentials match the default values
        if username == 'admin' and password == '123':
            session['logged_in'] = True
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password. Please try again.', 'error')
            return render_template('login.html')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    # Clear the session data
    session.pop('logged_in', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))
@app.route('/articles/<int:id>')
def view_article(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM articles WHERE id = %s', (id,))
    article = cursor.fetchone()
    cursor.execute('SELECT comments.*, users.username FROM comments JOIN users ON comments.author_id = users.id WHERE article_id = %s ORDER BY created_at DESC', (id,))
    comments = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('view_article.html', article=article, comments=comments)

@app.route('/articles/edit/<int:id>', methods=['GET', 'POST'])
def edit_article(id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM articles WHERE id = %s AND author_id = %s', (id, session['user_id']))
    article = cursor.fetchone()
    
    if not article:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        
        cursor.execute('UPDATE articles SET title = %s, content = %s WHERE id = %s', (title, content, id))
        conn.commit()
        cursor.close()
        conn.close()
        
        return redirect(url_for('dashboard'))
    
    cursor.close()
    conn.close()
    return render_template('edit_article.html', article=article)


if __name__ == '__main__':
    app.run(debug=True)
