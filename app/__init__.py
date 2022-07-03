#added tests
from crypt import methods
import os
from flask import Flask, render_template, request
from flask_googlemaps import GoogleMaps, Map
from dotenv import load_dotenv
from peewee import *
from datetime import datetime
from playhouse.shortcuts import model_to_dict

app = Flask(__name__)
if os.getenv('TESTING') == 'true':
    print('testing app')
    mydb = SqliteDatabase('file:memory?mode=memory&cache=shared',uri=True)
else:
    mydb = MySQLDatabase(os.getenv("MYSQL_DATABASE"), 
        user=os.getenv("MYSQL_USER"), 
        password = os.getenv("MYSQL_PASSWORD"),
        host = os.getenv("MYSQL_HOST"),
        port = 3306 )
load_dotenv()




GoogleMaps(app, key=os.getenv("MAPS_API_KEY"))


@app.route("/")
def index():

    # **Shape of Data**
    #
    # experiences = [{
    #    "name": string,
    #    "role": string,
    #    "date": string
    # }, ...]
    #
    # hobbies = [{
    #    "name": string,
    #    "img": string
    # }, ...]
    #
    # education = [{
    #    "name": string,
    #    "location": string
    # }, ...]

    return render_template("main.jinja",
                           title="Bobo the Baboon",
                           name="Bobo",
                           hobbies="Working out and Gaming",
                           url=os.getenv("URL"),
                           experiences=[
                               {
                                   "name": "Meta",
                                   "role": "Production Engineer",
                                   "date": "XX 2021 - XX 2022"
                               },
                               {
                                   "name": "Google",
                                   "role": "Software Engineer",
                                   "date": "XX 2020 - XX 2021"
                               },
                               {
                                   "name": "Amazon",
                                   "role": "Systems Development Engineer",
                                   "date": "XX 2019 - XX 2020"
                               },
                           ],
                           educations=[{
                               "name": "Yale University",
                               "location": "New Haven, CT"
                           }, {
                               "name": "Harvard University",
                               "location": "Cambridge, MA"
                           }, {
                               "name": "Stanford University",
                               "location": "Stanford, CA"
                           }])


@app.route("/hobbies")
def hobbies_and_map():
    # creating a map in the view
    title = "Bobo's Hobbies"

    bobomap = Map(
        identifier="bobomap",
        lat=9.1304,
        lng=41.2809,
        markers=[{
            'icon':
            'http://maps.google.com/mapfiles/ms/icons/blue-dot.png',
            'lat':
            9.1304,
            'lng':
            41.2809,
            'infobox':
            '<img src="https://cdn3.iconfinder.com/data/icons/142-mini-country-flags-16x16px/32/flag-denmark2x.png" width=32px height=32px/>',
        }, {
            'icon':
            'http://maps.google.com/mapfiles/ms/icons/yellow-dot.png',
            'lat':
            23.6345,
            'lng':
            -102.5528,
            'infobox':
            '<img src="https://cdn3.iconfinder.com/data/icons/142-mini-country-flags-16x16px/32/flag-mexico2x.png" width=32px height=32px/>'
        }, {
            'icon':
            'http://maps.google.com/mapfiles/ms/icons/green-dot.png',
            'lat':
            15.8700,
            'lng':
            100.9925,
            'infobox':
            '<img src= "../static/img/bobo.jpg" width=32px height=32px/>'
        }, {
            'icon':
            'http://maps.google.com/mapfiles/ms/icons/red-dot.png',
            'lat':
            64.9631,
            'lng':
            -19.0208,
            'infobox':
            '<img src= "https://cdn3.iconfinder.com/data/icons/142-mini-country-flags-16x16px/32/flag-iceland2x.png" width=32px height=32px/>'
        }],
        style="height:600px;width:1200px;margin:auto",
        zoom=2)

    hobbies = [
        {
            "name": "Gaming",
            "img": "./img/game.jpg"
        },
        {
            "name": "Working Out",
            "img": "./img/gym.jpg"
        },
    ]

    return render_template('hobbies_and_map.jinja',
                           title=title,
                           trdmap=bobomap,
                           hobbies=hobbies,
                           url=os.getenv("URL"))

@app.route('/timeline')
def timeline():
    return render_template('timeline.html',title="timeline")




class TimelinePost(Model):
    name = CharField()
    email = CharField()
    content = TextField()
    created_at = DateTimeField(default=datetime.now)
    
    class Meta:
        database = mydb
mydb.connect()
mydb.create_tables([TimelinePost])

@app.route('/api/timeline_post', methods=['POST'])
def post_time_line_post():
    try:
        name = request.form['name']
    except KeyError:
        return "Invalid Name", 400
    try:
        email = request.form['email']
        if not '@' in email:
            return "Invalid Email", 400
    except KeyError:
        return "Invalid Email", 400
    try:
        content = request.form['content']
        if len(content)<2:
            return "Invalid Content", 400
    except KeyError:
        return "Invalid Content", 400
    timeline_post= TimelinePost.create(name=name, email=email, content=content)

    return model_to_dict(timeline_post) 

@app.route('/api/timeline_post', methods=['GET'])
def get_time_line_post():
    return {
        'timeline_posts':[
            model_to_dict(p)
            for p in TimelinePost.select().order_by(TimelinePost.created_at.desc())            
        ]
    }    