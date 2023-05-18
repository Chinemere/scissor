from flask_restx import Namespace, fields, Resource
from flask import request 
from ..models.users import User
from werkzeug.exceptions import Conflict, BadRequest
from werkzeug.security import generate_password_hash
from http import HTTPStatus



auth_namespace= Namespace('auth', description='A namespace for authentication')

# serializer
signup_model=auth_namespace.model(
    'signUP',{
        'id': fields.Integer(),
        'username': fields.String(required=True, description='Type in your username'),
        'email': fields.String(required=True, description='type in An email'),
        'password': fields.String(required=True, description='Type in a Password')

    }
)

user__model=auth_namespace.model(
    'User',{
        'id': fields.Integer(),
        'username': fields.String(required=True, description= "A username"),
        'passwordhash': fields.String(required=True, description= "A username"),
    }
)

login__model=auth_namespace.model(
    'Login',{
        'username': fields.String(required=True, description= "A username"),
        'password': fields.String(required=True, description= "A username"),
    }
)


@auth_namespace.route('/signup')
class  SignUp(Resource):
    @auth_namespace.expect(signup_model)
    @auth_namespace.marshal_with(user__model)
    def post(self):
        ''' Create A new Account '''
        data = request.get_json()
        try:
            new_user= User(
                username = data.get('username'),
                email = data.get('email'),
                password_hash = generate_password_hash(data.get('password'))
            )
            new_user.save(), HTTPStatus.CREATED
            return new_user, 
        except Exception as e:
            raise Conflict(f'A User with  the email {data.get("email")} already exist')

