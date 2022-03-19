from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired
from flask_bootstrap import Bootstrap
import os
from datetime import datetime

app = Flask(__name__)

SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bikes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)

SINGLE_BIKE_COST = 4
DOUBLE_BIKE_COST = 3
GROUP_BIKE_COST = 2.5
EXCLUSIVE = 10


# Database
class Bike(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(100), nullable=False)
    tier = db.Column(db.String(100), nullable=False)
    hours = db.Column(db.Integer, nullable=False)
    date_and_time = db.Column(db.DateTime, default=datetime.today(), nullable=False)


# db.create_all()


# Form to appear on rent.html
class RentBikeForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()],
                           render_kw={"placeholder": "Your Name"})
    tiername = StringField("Tiername",
                           validators=[DataRequired()],
                           render_kw={"placeholder": "Example: Single/Double/Group/Exclusive"})
    hours = IntegerField("Hours", validators=[DataRequired()],
                         render_kw={"placeholder": "Example: Single/Double/Group/Exclusive"})
    submit = SubmitField("Submit")


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/rent', methods=['GET', 'POST'])
def rent_bike():
    rent_bike_form = RentBikeForm()
    if rent_bike_form.validate_on_submit():
        tier_name = rent_bike_form.tiername.data
        hours = rent_bike_form.hours.data
        print(tier_name)
        print(hours)
        # add to database
        new_hire = Bike(
            user_name=rent_bike_form.username.data,
            tier=rent_bike_form.tiername.data,
            hours=rent_bike_form.hours.data,
            # date_and_time=datetime.date.today().strftime("%B %d, %Y"),
        )
        db.session.add(new_hire)
        db.session.commit()

        if tier_name.lower() == "single":
            total_cost = SINGLE_BIKE_COST * hours
            print(total_cost)
            return render_template("index.html")
        elif tier_name.lower() == "double":
            total_cost = DOUBLE_BIKE_COST * hours
            print(total_cost)
            return render_template("index.html")
        elif tier_name.lower() == "group":
            total_cost = GROUP_BIKE_COST * hours
            print(total_cost)
            return render_template("index.html")
        elif tier_name.lower() == "exclusive":
            total_cost = EXCLUSIVE * hours
            print(total_cost)
            return render_template("index.html")
    else:
        return render_template('rent.html', form=rent_bike_form)


@app.route('/about')
def about():
    return render_template('about.html')


if __name__ == '__main__':
    app.run(debug=True)
