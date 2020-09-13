from flask import Flask, session, escape, url_for, request, redirect, render_template

from config import Config


app = Flask(__name__)
app.config.from_object(Config)

from models import User, db
from forms import RegistrationForm



@app.route('/', methods=['GET', 'POST'])
def index():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data)
        user.set_token()
        db.session.add(user)
        db.session.commit()
        return render_template('index.html', title='Home')
    if 'token' in session:
        data = session['token']
        return render_template('index.html', title='Home', data=data)
    return render_template('index.html', title='Home', form=form)


@app.route('/<token>')
def authentication(token):
    user = User.query.filter_by(token=token).first()
    if user:
        user.add_visits()
        db.session.add(user)
        db.session.commit()
        session['token'] = token

    return redirect(url_for('index'))


@app.route('/analytics')
def analytics():
    return 'Hello World!'



if __name__ == '__main__':
    app.run(debug=True)
