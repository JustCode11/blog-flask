from app import app, db, login_manager
from flask import render_template, flash, redirect, url_for, request
from app.models import Entry, Tag, User, Comment
from flask_login import current_user, login_user, logout_user, login_required
from app.forms import LoginForm, RegistrationForm, AddEntryForm, AddCommentForm, EditEntryForm


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    form = AddCommentForm()
    entries = Entry.query.all()
    if form.validate_on_submit():
        comment = Comment(content=form.content.data,
                          user_id=current_user.id, entry_id=form.entry_id.data)
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for('index'))
    print(form.errors)
    return render_template('index.html', title='Startseite', entries=entries, form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            return redirect(url_for('login'))
        login_user(user, remember=False)
        return redirect(url_for('index'))
    return render_template('login.html', title="Login", form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, firstname=form.firstname.data,
                    lastname=form.lastname.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('signup.html', title="Registrierung", form=form)


@app.route('/addEntry', methods=['GET', 'POST'])
@login_required
def addEntry():
    form = AddEntryForm()
    if form.validate_on_submit():
        entry = Entry(title=form.title.data, content=form.content.data,
                      user_id=current_user.id)
        for tagId in form.tags.data:
            tag = Tag.query.get(tagId)
            entry.tags.append(tag)
        db.session.add(entry)
        db.session.commit()
        return redirect(url_for('index'))
    print(form.errors)
    return render_template('addEntry.html', title="Neuen Blogeintrag", form=form)


@app.route('/editEntry/<entryId>', methods=['GET', 'POST'])
@login_required
def editEntry(entryId):
    entry = Entry.query.filter_by(id=int(entryId)).first()
    form = EditEntryForm()
    if form.validate_on_submit():
        print('content: ', form.content.data)
        Entry.query.filter_by(id=int(entryId)).update({'title': form.title.data,
                                                       'content': form.content.data})
        entry.tags = []
        for tagId in form.tags.data:
            tag = Tag.query.get(tagId)
            entry.tags.append(tag)
        db.session.add(entry)
        db.session.commit()
        return redirect(url_for('profile'))
    form.content.data = entry.content
    print(form.errors)
    return render_template('editEntry.html', title="Eintrag bearbeiten", entry=entry, form=form)


@app.route('/deleteEntry/<int:entryId>')
@login_required
def deleteEntry(entryId):
    entry_to_delete = Entry.query.get_or_404(entryId)
    try:
        db.session.delete(entry_to_delete)
        db.session.commit()
        return redirect(url_for('profile'))
    except:
        return redirect(url_for('profile'))


@app.route('/deleteComment/<int:commentId>')
@login_required
def deleteComment(commentId):
    comment_to_delete = Comment.query.get_or_404(commentId)
    try:
        db.session.delete(comment_to_delete)
        db.session.commit()
        return redirect(url_for('profile'))
    except:
        return redirect(url_for('profile'))


@app.route('/profile')
@login_required
def profile():
    entries = Entry.query.filter_by(user_id=current_user.id).all()
    comments = Comment.query.filter_by(user_id=current_user.id).all()
    return render_template('profile.html', title="Profil", entries=entries, comments=comments)
