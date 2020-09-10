import json
from flask import Flask, request, jsonify, render_template, redirect
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_cors import CORS
from config import Development
from models import db, Todo

app = Flask(__name__) #instanciando Flask para crear nuestra aplicación.
app.url_map.strict_slashes = False
app.config.from_object(Development)
db.init_app(app)
Migrate(app, db)
manager = Manager(app)
manager.add_command("db", MigrateCommand)
CORS(app)

@app.route("/") #definimos la ruta principal.
def main():
    return render_template('index.html')

"""
@app.route("/test", methods=['GET'])
def test():
    if request.method == 'GET':
        pass

@app.route("/test/<int:id>", methods=['GET'])
def test(id):
    if request.method == 'GET':
        pass

@app.route("/test", methods=['POST'])
def test(id = None):
    if request.method == 'GET':
        pass

@app.route("/test/<int:id>", methods=['PUT'])
def test(id):
    if request.method == 'GET':
        pass

@app.route("/test/<int:id>", methods=['DELETE'])
def test(id):
    if request.method == 'GET':
        pass
"""   

@app.route("/todos/user/<username>", methods=['GET', 'POST', 'PUT', 'DELETE'])
def todos(username):
    if request.method == 'GET':
        todo = Todo.query.filter_by(username = username).first()
        if todo:
            return jsonify(todo.serialize()), 200
        else:
            return jsonify({"msg": "This user does not exists, first call the POST method to create a username"}), 404

    if request.method == 'POST':
        todos = request.get_json()

        if not type(todos) == list:
            return jsonify({"msg": "The request body must be an empty array"}), 400
        if len(todos) > 0:
            return jsonify({"msg": "The request body must be an empty array"}), 400

        todo = Todo.query.filter_by(username = username).first()
        if todo:  
            return jsonify({"msg": "This user was already created"}), 404

        todo = Todo()
        todo.username = username
        todos.append({"label": "Sample Task", "done": False})
        todo.todos = json.dumps(todos)
        todo.save()

        if todo:
            return jsonify({
                "result": "ok"
            }), 201
        else: 
            return jsonify({"msg": "Error with todos"}), 400 

        return jsonify({
            "result": "ok"
        }),201
        
    if request.method == 'PUT':
        todos = request.get_json()

        if not type(todos) == list:
            return jsonify({"msg": "The request body must be an empty array"}), 400
        if len(todos) == 0:
            return jsonify({"msg": "The request body is empty but it must be an array of todo's"}), 400

        todo = Todo.query.filter_by(username = username).first()
        if not todo:  
            return jsonify({"msg": "This user does not exists, first call the POST method to create a username"}), 404

        todo.todos = json.dumps(todos)
        todo.update()

        return jsonify({"result": "A list with {0} todo's was successfully saved".format(len(todos))}), 200

    if request.method == 'DELETE': 
        todo = Todo.query.filter_by(username = username).first()

        if not todo:
            return jsonify({"msg": "This user does not exists, first call the POST method to create a username"}), 404
        else:
            todo.delete()
            return jsonify({
                "result": "ok"
            }), 201  

if __name__ == "__main__": #preguntamos si esta es nuestra app principal.
    manager.run()