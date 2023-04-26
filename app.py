import os

os.environ["FLASK_APP"] = "app"
os.environ["FLASK_ENV"] = "development"
os.environ["FLASK_DEBUG"] = "0"

from flask import Flask
from flask_restful import Api, Resource, reqparse
from flasgger import Swagger, swag_from

app = Flask(__name__)
api = Api(app)

# initialize Swagger
swagger = Swagger(app)

# create a list of tasks
tasks = {}

# create a class for the resource
class TodoSimple(Resource):
    @swag_from('todo_get.yml')
    def get(self, todo_id):
        """
        This is the GET method for TodoSimple resource
        """
        return {todo_id: tasks[todo_id]}

    @swag_from('todo_post.yml')
    def post(self, todo_id):
        """
        This is the POST method for TodoSimple resource
        """
        parser = reqparse.RequestParser()
        parser.add_argument('data', type=str, help='data for TODO task')
        args = parser.parse_args()

        tasks[todo_id] = args['data']
        return {todo_id: tasks[todo_id]}

    @swag_from('todo_put.yml')
    def put(self, todo_id):
        """
        This is the PUT method for TodoSimple resource
        """
        parser = reqparse.RequestParser()
        parser.add_argument('data', type=str, help='data for TODO task')
        args = parser.parse_args()

        tasks[todo_id] = args['data']
        return {todo_id: tasks[todo_id]}

    @swag_from('todo_delete.yml')
    def delete(self, todo_id):
        """
        This is the DELETE method for TodoSimple resource
        """
        del tasks[todo_id]
        return {'message': 'Task deleted'}

class TodoList(Resource):
    @swag_from('todo_list.yml')
    def get(self):
        """
        This is the GET method for TodoList resource
        """
        return tasks

    @swag_from('todo_post.yml')
    def post(self):
        """
        This is the POST method for TodoList resource
        """
        parser = reqparse.RequestParser()
        parser.add_argument('task', type=str, help='task to add')
        args = parser.parse_args()

        todo_id = len(tasks) + 1
        tasks[todo_id] = args['task']
        return {todo_id: tasks[todo_id]}

# add the resources to the api
api.add_resource(TodoSimple, '/tasks/<string:todo_id>')
api.add_resource(TodoList, '/tasks')

@app.route('/')
def index():
    return 'Flask application is running!'

if __name__ == '__main__':
    app.run(debug=True)
