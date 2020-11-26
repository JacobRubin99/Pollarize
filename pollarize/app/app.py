import logging
import os

import flask
import flask_login
import models
from flask import redirect, render_template, request, url_for, flash
from flask_login import current_user
from forms import LoginForm, RegistrationForm, CreatePollForm, PollFormFactory, BioUpdateForm, PollSearchForm, AddTagFormFactory
from models import Profile, db, migrate, Poll
from werkzeug.urls import url_parse
from datetime import datetime

logging.basicConfig(level=logging.DEBUG)

app = flask.Flask(__name__)
app.config.from_object('config')
db.init_app(app)
migrate.init_app(app, db)

# TODO: Move into config.py
app.config['SECRET_KEY'] = 'secretkey'
app.config['WTF_CSRF_SECRET_KEY'] = 'secretkey'

login_manager = flask_login.LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def user_loader(id):
    return Profile.query.get(int(id))


@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect('/login?next=' + request.path)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        profile = Profile.query.filter_by(username=form.username.data).first()
        if profile is None or not profile.check_password(form.password.data):
            flask.flash('Invalid username or password')
            return redirect(flask.url_for('login'))

        flask_login.login_user(profile, remember=form.remember_me.data)
        next_page = request.args.get('next')

        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('me')
        return redirect(next_page)

    return flask.render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        profile = Profile(username=form.username.data, email=form.email.data)
        profile.set_password(form.password.data)
        db.session.add(profile)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/logout')
def logout():
    flask_login.logout_user()
    return redirect(url_for('login'))


@app.route('/me')
@flask_login.login_required
def me():
    return redirect(url_for('user', profile_id=current_user.id))


@app.route('/', methods=['GET', 'POST'])
def home():
    search = PollSearchForm(request.form)
    if request.method == 'POST':
        return search_results(search)
    polls = db.session.query(models.Poll).all()
    polls.reverse()
    return render_template('home.html', polls=polls, form=search)

@app.route('/search-results')
def search_results(search):
    results = []
    search_string = search.data['search']
    if search.data['search'] == '':
        results = db.session.query(models.Poll).all()
    else:
        select = search.data['select']
        if select == 'Keyword':
            results = db.session.query(models.Poll).filter(
                models.Poll.title.ilike('%'+ search_string + '%'))
        elif select == 'Author':
            if not search_string.isdigit():
                flash('Authors must be integers')
                return redirect('/')
            results = db.session.query(models.Poll).filter(
                models.Poll.creator_user_id == search_string)

    if not results:
        flash('No results found!')
        return redirect('/')
    else:
        return render_template('results.html', polls=results)

@app.route('/create-poll', methods=['GET', 'POST'])
@flask_login.login_required
def create_poll():
    form = CreatePollForm()
    if form.validate_on_submit():
        poll = Poll(title=form.title.data, date_added=datetime.now(),
                    creator_user_id=current_user.id)
        db.session.add(poll)
        db.session.commit()
        return redirect('/poll/' + str(poll.poll_id))
    return render_template('create-poll.html', title='Create Poll', form=form)


@app.route('/poll/<id>', methods=['GET','POST'])
def poll(id):
    poll = db.session.query(models.Poll).filter(
        models.Poll.poll_id == id).one()
    choices = db.session.query(models.Choice).filter(
        models.Choice.poll_id == id).all()
    choices = sorted(choices, key=(lambda x: x.rating), reverse=True)
    tags = db.session.query(models.PollTag).filter(
        models.PollTag.poll_id == id).all()
    existing_tags = db.session.query(models.Tag).all()
    votes = db.session.query(models.Vote).filter(
        models.Vote.user_id == current_user.id)\
        .filter(models.Vote.choice_id.in_([choice.id for choice in choices]))\
        .all()
    
    choice_votes_dict = {}
    for choice in choices:
        choice_votes_dict[choice.id] = 0
        for vote in votes:
            if choice.id == vote.choice_id:
                choice_votes_dict[choice.id] = vote.value

    print(choice_votes_dict)

    form = AddTagFormFactory.form(existing_tags)
    if form.validate_on_submit():
        if form.new_tag.data:
            tag = models.Tag(
                title=form.new_tag.data,
                date_added=datetime.now(),
                creator_user_id=current_user.id)
            db.session.add(tag)
            db.session.commit()
            polltag = models.PollTag(poll_id=id, tag_title=form.new_tag.data)
            db.session.add(polltag)
        else:
            for tag in form.tags.data:
                polltag = models.PollTag(poll_id=id, tag_title=tag)
                db.session.add(polltag)
        db.session.commit()
        return redirect('/poll/' + id)
    return render_template('poll.html', title=poll.title, poll=poll, choices=choices, votes_dict=choice_votes_dict, tags=tags, form=form)

@app.route('/api/newchoice/<poll_id>', methods=['POST'])
def newchoice(poll_id):
    if len(request.json['title']) < 1:
        return ('Empty choice', 400)

    choice = models.Choice(
        poll_id=poll_id,
        title=request.json['title'],
        date_added=datetime.now(),
        creator_user_id=current_user.id,
        rating=0
    )
    db.session.add(choice)
    db.session.commit()
    return ('', 201)

@app.route('/api/vote/<choice_id>', methods=['POST'])
def votechoice(choice_id):
    vote = models.Vote(
        choice_id=choice_id,
        user_id=current_user.id,
        value=request.json['value']
    )
    db.session.add(vote)
    db.session.commit()
    return ('', 201)

@app.route('/user/<profile_id>', methods=['GET'])
def user(profile_id):
    other_user_profile = Profile.query.filter_by(id=profile_id).first()
    return render_template('profile.html', profile=other_user_profile)
    # return 'Viewing user.id={}, user.email={}'.format(
    #    other_user_profile.id,
    #    other_user_profile.email
    # )


@app.route('/updatebio', methods=['GET', 'POST'])
@flask_login.login_required
def update_bio():
    user_id = current_user.id
    form = BioUpdateForm()
    if form.validate_on_submit():
        # if the user cancelled, just redirect them to home
        if form.cancel.data:
            # pressed cancel button
            return redirect(url_for("me"))
        # pressed submit button
        profile = Profile.query.filter_by(id=user_id).first()
        profile.bio = form.bio.data
        db.session.add(profile)
        db.session.commit()
        return redirect(url_for('me'))
    return render_template('update-bio.html', title='update bio', form=form)


@app.route('/test', methods=['GET'])
def test():
    result = db.engine.execute('SELECT now();')
    return dict(result.fetchone())


app.run(host='0.0.0.0', port=5000, debug=True)
