from ..models.users import User
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required
from http import HTTPStatus



user_namespace = Namespace('users', description="Namespace for users")

user_model = user_namespace.model(
    "Users", {
        "id":fields.Integer(),
        "username": fields.String(description= "your username"),
        "email" : fields.String(description= "your username")
    }

)

@user_namespace.route('/allusers')
class GetAllUsers(Resource):
    @user_namespace.marshal_with(user_model)
    @jwt_required()
    def get(self):
        ''' Get all Users '''
        all_users = User.query.all()
        return all_users, HTTPStatus.OK



