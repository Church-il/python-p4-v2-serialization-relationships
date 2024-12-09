# server/app.py
from flask import Flask, make_response
from flask_migrate import Migrate
from models import db, Zookeeper, Enclosure, Animal

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

@app.route('/')
def index():
    return '<h1>Zoo app</h1>'

@app.route('/animal/<int:id>')
def animal_by_id(id):
    animal = Animal.query.get(id)
    if animal:
        response_body = f'''
        <ul>ID: {animal.id}</ul>
        <ul>Name: {animal.name}</ul>
        <ul>Species: {animal.species}</ul>
        <ul>Zookeeper: {animal.zookeeper.name if animal.zookeeper else "None"}</ul>
        <ul>Enclosure: {animal.enclosure.environment if animal.enclosure else "None"}</ul>
        '''
        return make_response(response_body)
    return make_response('<h1>Animal not found</h1>', 404)

@app.route('/zookeeper/<int:id>')
def zookeeper_by_id(id):
    zookeeper = Zookeeper.query.get(id)
    if zookeeper:
        response_body = f'''
        <ul>ID: {zookeeper.id}</ul>
        <ul>Name: {zookeeper.name}</ul>
        <ul>Birthday: {zookeeper.birthday}</ul>
        '''
        response_body += ''.join([f'<ul>Animal: {animal.name}</ul>' for animal in zookeeper.animals])
        return make_response(response_body)
    return make_response('<h1>Zookeeper not found</h1>', 404)

@app.route('/enclosure/<int:id>')
def enclosure_by_id(id):
    enclosure = Enclosure.query.get(id)
    if enclosure:
        response_body = f'''
        <ul>ID: {enclosure.id}</ul>
        <ul>Environment: {enclosure.environment}</ul>
        <ul>Open to Visitors: {enclosure.open_to_visitors}</ul>
        '''
        response_body += ''.join([f'<ul>Animal: {animal.name}</ul>' for animal in enclosure.animals])
        return make_response(response_body)
    return make_response('<h1>Enclosure not found</h1>', 404)

if __name__ == '__main__':
    app.run(port=5555, debug=True)
