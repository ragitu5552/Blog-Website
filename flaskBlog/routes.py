import os
import secrets
from flask import render_template, url_for, flash, redirect, request, abort
from flaskBlog import app, db, bcrypt
from flaskBlog.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm
from flaskBlog.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required


@app.route("/")
@app.route("/home")
def home():
    with app.app_context():
        posts = Post.query.all()
        users = {user.id:user for user in User.query.all()}
    return render_template('home.html', title='Home', posts=posts, users=users)


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))



@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form)

@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        with app.app_context():
            posts = Post(title=form.title.data, content=form.content.data, user_id=current_user.id)
            db.session.add(posts)
            db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('home'))
    return render_template("create_post.html", title="Create Post", form=form, legend="Create New Post")

@app.route("/post/<int:post_id>")
def post(post_id):
    with app.app_context():
        post = Post.query.get_or_404(post_id)
        user = User.query.filter_by(id=post_id).first()
        return render_template('post.html', title=post.title, post = post, post_id=post_id, user=user)

@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    with app.app_context():
        post = Post.query.get_or_404(post_id)
        user = User.query.filter_by(id=post.user_id).first()
        if user != current_user:
            abort(403)
        form = PostForm()
        if form.validate_on_submit():
            with app.app_context():
                post = Post.query.filter_by(id=post_id).first()
                post.title = form.title.data
                post.content = form.content.data
                db.session.commit()
                flash('Post updated successfully!', 'success')
                return redirect(url_for('post', post_id=post.id))
        elif request.method == "GET":
            form.title.data = post.title
            form.content.data = post.content
        return render_template("create_post.html", title="Update Post", form=form, legend="Update Post")

@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    with app.app_context():
        post = Post.query.get_or_404(post_id)
        user = post.author
        if user != current_user:
            abort(403)
        db.session.delete(post)
        db.session.commit()
        flash('Post Deleted', 'success')
        return redirect(url_for('home'))