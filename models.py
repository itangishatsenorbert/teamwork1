from app import mysql
from werkzeug.security import check_password_hash

class User:
    @staticmethod
    def create_user(username, email, password):
        cursor = mysql.connection.cursor()
        cursor.execute(''' INSERT INTO users(username, email, password) VALUES(%s, %s, %s) ''', (username, email, password))
        mysql.connection.commit()
        cursor.close()

    @staticmethod
    def authenticate(email, password):
        cursor = mysql.connection.cursor()
        cursor.execute(''' SELECT * FROM users WHERE email = %s ''', (email,))
        user = cursor.fetchone()
        cursor.close()
        if user and check_password_hash(user['password'], password):
            return user
        return None

class Article:
    @staticmethod
    def create_article(title, content, author_id):
        cursor = mysql.connection.cursor()
        cursor.execute(''' INSERT INTO articles(title, content, author_id) VALUES(%s, %s, %s) ''', (title, content, author_id))
        mysql.connection.commit()
        cursor.close()

    @staticmethod
    def get_all_articles():
        cursor = mysql.connection.cursor()
        cursor.execute(''' SELECT articles.id, title, content, username FROM articles JOIN users ON articles.author_id = users.id ''')
        articles = cursor.fetchall()
        cursor.close()
        return articles

    @staticmethod
    def get_article_by_id(article_id):
        cursor = mysql.connection.cursor()
        cursor.execute(''' SELECT articles.id, title, content, username FROM articles JOIN users ON articles.author_id = users.id WHERE articles.id = %s ''', (article_id,))
        article = cursor.fetchone()
        cursor.close()
        return article

    @staticmethod
    def update_article(article_id, title, content):
        cursor = mysql.connection.cursor()
        cursor.execute(''' UPDATE articles SET title = %s, content = %s WHERE id = %s ''', (title, content, article_id))
        mysql.connection.commit()
        cursor.close()

    @staticmethod
    def delete_article(article_id):
        cursor = mysql.connection.cursor()
        cursor.execute(''' DELETE FROM articles WHERE id = %s ''', (article_id,))
        mysql.connection.commit()
        cursor.close()

class Comment:
    @staticmethod
    def add_comment(article_id, user_id, content):
        cursor = mysql.connection.cursor()
        cursor.execute(''' INSERT INTO comments(article_id, user_id, content) VALUES(%s, %s, %s) ''', (article_id, user_id, content))
        mysql.connection.commit()
        cursor.close()

    @staticmethod
    def get_comments_by_article(article_id):
        cursor = mysql.connection.cursor()
        cursor.execute(''' SELECT comments.id, content, username FROM comments JOIN users ON comments.user_id = users.id WHERE article_id = %s ''', (article_id,))
        comments = cursor.fetchall()
        cursor.close()
        return comments

    @staticmethod
    def delete_comment(comment_id):
        cursor = mysql.connection.cursor()
        cursor.execute(''' DELETE FROM comments WHERE id = %s ''', (comment_id,))
        mysql.connection.commit()
        cursor.close()
