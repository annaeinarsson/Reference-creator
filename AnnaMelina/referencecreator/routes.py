import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from referencecreator import app, db, bcrypt
from referencecreator.forms import RegistrationForm, LoginForm, UpdateAccountForm, ProjectForm, ReferenceForm
from referencecreator.models import User, Project, Reference
from flask_login import login_user, current_user, logout_user, login_required
# Why can't it find forms and models?


@app.route("/")
@app.route("/home")
def home():  # this is before login
    return render_template('home.html')


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:  # does this mean if the user is logged in?
        return redirect(url_for('home'))  # then home should change to my_projects
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
            # next_page = request.args.get('next')
            # return redirect(next_page) if next_page else redirect(url_for('home'))
            return redirect(url_for('my_projects'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
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


"""@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content_type=form.content_type.data, content=form.content.data, user=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('create_project.html', title='New Post',
                           form=form, legend='New Post')"""


@app.route("/project/new", methods=['GET', 'POST'])
@login_required
def new_project():
    form = ProjectForm()
    if form .validate_on_submit():
        project = Project(title=form.title.data, user=current_user)
        db.session.add(project)
        db.session.commit()
        flash('Your project has been created!', 'success')
        return redirect(url_for('my_projects'))
    return render_template('create_project.html', title='Create New Project',
                           form=form, legend='Create New Project')


"""@app.route("/post/<int:post_id>", methods=['GET', 'POST'])
def post(post_id):
    post = Post.query.get_or_404(post_id)
    form = CommentForm()
    if form.validate_on_submit():
        if current_user.is_authenticated:  # you can only comment if you're logged in
            comment = Reference(content=form.content.data, user=current_user, post=post)
            db.session.add(comment)
            db.session.commit()
            flash('Your post has been created!', 'success')
            return redirect(f"/post/{post.id}")
        else:
            flash('You are not logged in. You need to be logged in to be able to comment!', 'danger')
    # loading comments in the reverse order of insertion
    comments = Comment.query.filter(Post.id == post.id).order_by(Comment.date_posted.desc()).all()
    return render_template('project.html', title=post.title, post=post, form=form, comments=comments)"""


@app.route("/project/<int:project_id>", methods=['GET', 'POST'])
def project(project_id):
    project = Project.query.get_or_404(project_id)
    form = ReferenceForm()
    if form.validate_on_submit():
        if current_user.is_authenticated:  # you can only create a reference if you're logged in
            reference = Reference(title=form.title.data,
                                  publish_date=form.publish_date.data,
                                  subtitle=form.subtitle.data,
                                  author=form.author.data,
                                  journal_title=form.journal_title.data,
                                  volume=form.volume.data,
                                  number=form.number.data,
                                  pages=form.pages.data,
                                  doi=form.doi.data,
                                  isbn=form.doi.data,
                                  chapter=form.chapter.data,
                                  editor=form.editor.data,
                                  publish_place=form.publish_place.data,
                                  publisher=form.publisher.data,
                                  url=form.url.data,
                                  organisation=form.organisation.data,
                                  user=current_user, project=project)
            db.session.add(reference)
            db.session.commit()
            flash('Your reference has been created!', 'success')
            return redirect(f"/project/{project.id}")
        else:
            flash('You are not logged in. You need to be logged in to be able to add references!', 'danger')
    # want to insert references in alphabetical order
    references = Reference.query.filter(Project.id == project.id).all()
    return render_template('project.html', title=project.title, project=project, form=form, references=references)


@app.route("/project/<int:project_id>/add_reference", methods=['POST'])
@login_required
def add_reference(reference_id):  # is it right to use the reference id here?
    form = ReferenceForm()
    if form.validate_on_submit():
        if current_user.is_authenticated:  # you can only create a reference if you're logged in
            reference = Reference(content=form.content.data, user=current_user,
                                  project=project)  # It needs to coupled
            db.session.add(reference)
            db.session.commit()
            flash('Your reference has been created!', 'success')
            return redirect(f"/project/{project.id}")
        else:
            flash('You are not logged in. You need to be logged in to be able to add references!', 'danger')


"""@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        post.content_type = form.content_type.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
        form.content_type.data = post.content_type
    return render_template('create_project.html', title='Update Post',
                           form=form, legend='Update Post')"""


@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_reference(reference_id):
    reference = Reference.query.get_or_404(reference_id)
    if project.author != current_user:
        abort(403)
    form = ReferenceForm()
    if form.validate_on_submit():
        reference.title = form.title.data
        reference.publish_date = form.publish_date.data
        reference.subtitle = form.subtitle.data
        reference.author = form.author.data
        reference.journal_title = form.journal_title.data
        reference.volume = form.volume.data
        reference.number = form.number.data
        reference.pages = form.pages.data
        reference.doi = form.doi.data
        reference.isbn = form.isbn.data
        reference.chapter = form.chapter.data
        reference.editor = form.editor.data
        reference.publish_place = form.publish_place.data
        reference.publisher = form.publisher.data
        reference.url = form.url.data
        reference.organisation = form.organisation.data
        db.session.commit()
        flash('Your reference has been updated!', 'success')
        return redirect(url_for('project', project_id=project.id))
    elif request.method == 'GET':
        form.title.data = reference.title
        form.publish_date.data = reference.publish_date
        form.subtitle.data = reference.subtitle
        form.author.data = reference.author
        form.journal_title.data = reference.journal_title
        form.volume.data = reference.volume
        form.number.data = reference.number
        form.pages.data = reference.pages
        form.doi.data = reference.doi
        form.isbn.data = reference.isbn
        form.chapter.data = reference.chapter
        form.editor.data = reference.editor
        form.publish_place.data = reference.publish_place
        form.publisher.data = reference.publisher
        form.url.data = reference.url
        form.organisation.data = reference.organisation
    return render_template('add_reference.html', title='Update Reference',
                           form=form, legend='Update Reference')


@app.route("/my_projects", methods=['GET'])
@login_required
def my_projects():
    projects = Project.query.order_by(Project.date_created).all()
    return render_template('my_projects.html', title='My Projects', projects=projects)


@app.route("/project/<int:project_id>/delete", methods=['POST'])
@login_required
def delete_project(project_id):
    project = Project.query.get_or_404(project_id)
    if project.author != current_user:
        abort(403)
    db.session.delete(project)
    db.session.commit()
    flash('Your project has been deleted!', 'success')
    return redirect(url_for('my_projects'))


@app.route("/project/reference/<int:reference_id>/delete", methods=['POST'])
@login_required
def delete_reference(reference_id):
    reference = Reference.query.get_or_404(reference_id)
    if Project.author != current_user:
        abort(403)
    db.session.delete(reference)
    db.session.commit()
    flash('Your reference has been deleted!', 'success')  # possibly remove this and just update the page
    return redirect(url_for('project'))  # Just want to update the page, is this the best way?

