from flask_restx import Namespace, fields, Resource
from flask import request 
from ..models.users import User
from werkzeug.exceptions import Conflict, BadRequest
from werkzeug.security import generate_password_hash, check_password_hash
from http import HTTPStatus
from flask_jwt_extended import get_jwt_identity,    create_access_token, create_refresh_token, current_user, get_current_user



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

user_model=auth_namespace.model(
    'User',{
        'id': fields.Integer(),
        'email': fields.String(required=True, description= "A username"),
        'username': fields.String(required=True, description= "A username")
    }
)

login_model=auth_namespace.model(
    'Login',{
        'username': fields.String(required=True, description= "A username"),
        'password': fields.String(required=True, description= "A username"),
    }
)


@auth_namespace.route('/signup')
class  SignUp(Resource):
    @auth_namespace.expect(signup_model)
    @auth_namespace.marshal_with(user_model)
    def post(self):
        ''' Create A new Account '''
        data = request.get_json() 
        try:

            new_user= User(
                username = data.get('username'),
                email = data.get('email'),
                passwordHash = generate_password_hash(data.get('password'))
            )
            new_user.save()
            return new_user, HTTPStatus.CREATED
        except Exception as e:
            raise Conflict(f' User creation unsuccessful: {str(e)}'  )


@auth_namespace.route('/login')
class  Login(Resource):
    @auth_namespace.expect(login_model)
    def post(self):
        '''Generate JWT/Login '''
        data = request.get_json()
        username = User.query.filter_by(username=data.get('username')).first()
        password= data.get('password')
        if (username is not None) and check_password_hash(username.passwordHash, password):
            acces_token = create_access_token(identity=username.username)
            refresh_token= create_refresh_token(identity=username.username)
            response = {
                'access_token':acces_token, 
                'refresh_token': refresh_token
            }
            return response, HTTPStatus.OK
        raise BadRequest('Invalid Username or password')



