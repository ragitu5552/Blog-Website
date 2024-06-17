from flaskBlog import app, db
from flaskBlog import User, Post  # Import your models

def create_tables():
    with app.app_context():
        db.create_all()
        print("Database tables created successfully.")

def add_data():
    with app.app_context():
        user_1 = User(username='tuktuk', email='tuktuk@gmail.com', password='password')
        print('User added successfully!')

def show_data():
    with app.app_context():
        users = User.query.all()
        for user in users:
            print(f"Username: {user.username}, Email: {user.email}, posts: {user.posts}")

if __name__ == '__main__':
    show_data()