from flask_restx import Namespace, Resource, fields
from flask import request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.models import db, User, Todo
import requests

# Create Namespace
ns = Namespace('api', description="User & Todo APIs")

# ---------------- Swagger Models ----------------
user_model = ns.model('User', {
    'username': fields.String(required=True),
    'email': fields.String(required=True),
    'password': fields.String(required=True)
})

login_model = ns.model('Login', {
    'email': fields.String(required=True),
    'password': fields.String(required=True)
})

todo_model = ns.model('Todo', {
    'userId': fields.Integer(required=True),
    'title': fields.String(required=True),
    'completed': fields.Boolean(default=False)
})

@ns.route('/hello')
class HelloWorld(Resource):
    def get(self):
        """Simple test API to check if server is running"""
        return {"message": "Hello, World! API is working!"}

# ---------------- User Resources ----------------
@ns.route('/register')
class Register(Resource):
    @ns.expect(user_model)
    def post(self):
        data = request.json
        if User.query.filter_by(email=data['email']).first():
            return {"message": "Email already exists"}, 400
        user = User(username=data['username'], email=data['email'])
        user.set_password(data['password'])
        db.session.add(user)
        db.session.commit()
        return {"message": "User registered successfully"}, 201


@ns.route('/login')
class Login(Resource):
    @ns.expect(login_model)
    def post(self):
        data = request.json
        user = User.query.filter_by(email=data['email']).first()
        if user and user.check_password(data['password']):
            token = create_access_token(identity=user.id)
            return {"message": "Login successful", "access_token": token}, 200
        return {"message": "Invalid credentials"}, 401


@ns.route('/dashboard')
class Dashboard(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        user_obj = User.query.get(user_id)
        return {"message": f"Welcome {user_obj.username}!"}


@ns.route('/logout')
class Logout(Resource):
    def post(self):
        # JWT logout is handled in frontend by deleting the token
        return {"message": "Logout successful"}


# ---------------- Todo Resources ----------------
@ns.route('/todo/save')
class SaveTodos(Resource):
    def post(self):
        url = "https://jsonplaceholder.typicode.com/todos/"
        response = requests.get(url)
        if response.status_code != 200:
            return {"message": "Failed to fetch data"}, response.status_code
        todos_data = response.json()
        saved_count = 0
        for t in todos_data:
            if not Todo.query.get(t['id']):
                new_todo = Todo(
                    id=t['id'],
                    userId=t['userId'],
                    title=t['title'],
                    completed=t['completed']
                )
                db.session.add(new_todo)
                saved_count += 1
        db.session.commit()
        return {"message": f"{saved_count} todos saved to DB"}


@ns.route('/todo')
class TodoList(Resource):
    @ns.marshal_list_with(todo_model)
    def get(self):
        todos_list = Todo.query.all()
        return todos_list

    @ns.expect(todo_model)
    def post(self):
        data = request.json
        new_todo = Todo(
            userId=data['userId'],
            title=data['title'],
            completed=data.get('completed', False)
        )
        db.session.add(new_todo)
        db.session.commit()
        return {"message": "Todo created", "todo": {
            "id": new_todo.id,
            "userId": new_todo.userId,
            "title": new_todo.title,
            "completed": new_todo.completed
        }}, 201


@ns.route('/todo/<int:todo_id>')
class SingleTodo(Resource):
    @ns.marshal_with(todo_model)
    def get(self, todo_id):
        todo_obj = Todo.query.get(todo_id)
        if not todo_obj:
            ns.abort(404, "Todo not found")
        return todo_obj

    @ns.expect(todo_model)
    def put(self, todo_id):
        todo_obj = Todo.query.get(todo_id)
        if not todo_obj:
            ns.abort(404, "Todo not found")
        data = request.json
        todo_obj.title = data.get('title', todo_obj.title)
        todo_obj.completed = data.get('completed', todo_obj.completed)
        todo_obj.userId = data.get('userId', todo_obj.userId)
        db.session.commit()
        return {"message": "Todo updated", "todo": {
            "id": todo_obj.id,
            "userId": todo_obj.userId,
            "title": todo_obj.title,
            "completed": todo_obj.completed
        }}

    def delete(self, todo_id):
        todo_obj = Todo.query.get(todo_id)
        if not todo_obj:
            ns.abort(404, "Todo not found")
        db.session.delete(todo_obj)
        db.session.commit()
        return {"message": "Todo deleted"}


@ns.route('/todo/search')
class SearchTodo(Resource):
    def get(self):
        title = request.args.get('title')
        completed = request.args.get('completed')
        query = Todo.query
        if title:
            query = query.filter(Todo.title.ilike(f"%{title}%"))
        if completed is not None:
            if completed.lower() == 'true':
                query = query.filter(Todo.completed == True)
            elif completed.lower() == 'false':
                query = query.filter(Todo.completed == False)
        todos_list = query.all()
        return todos_list


@ns.route('/todo/page')
class PaginatedTodos(Resource):
    def get(self):
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))
        pagination = Todo.query.paginate(page=page, per_page=per_page, error_out=False)
        data = [{
            "id": t.id,
            "userId": t.userId,
            "title": t.title,
            "completed": t.completed
        } for t in pagination.items]
        return {"page": page, "per_page": per_page, "total": pagination.total, "todos": data}


@ns.route('/todo/stats')
class TodoStats(Resource):
    def get(self):
        total = Todo.query.count()
        completed = Todo.query.filter_by(completed=True).count()
        pending = total - completed
        return {"total": total, "completed": completed, "pending": pending}
