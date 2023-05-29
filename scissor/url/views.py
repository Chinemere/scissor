from ..utils import db
from flask_restx import Namespace, fields, Resource
from ..models.url import Url
from ..models.users import User
from flask import request, redirect
from random import randint
from http import HTTPStatus
from urllib.parse import urlparse
import requests 
from ..utils import caches
from flask_jwt_extended import  jwt_required, get_jwt_identity



url_namespace= Namespace('url', description='Namespace for URLs')

url_model = url_namespace.model(
    "Url", {
        "url_source":fields.String()

    }
)

url_history= url_namespace.model(
    "Link History",{
        "username": fields.String(),
        "url_source": fields.String(),
        "scissored_url" : fields.String(),
        "clicks": fields.Integer(),
        "user" : fields.Integer(),
        "created_at": fields.DateTime()

    }
)



@caches.cached(timeout=60)
@url_namespace.route('/')
class Links(Resource):
    # from scissor import cache

    @url_namespace.expect(url_model)
    @jwt_required()
    def post(self):
        data = request.get_json()
        url_source = data.get('url_source')
        if not url_source.startswith('http://') and not url_source.startswith('https://'):
            url_source =  "http://" + url_source
        # Check if the url is valid
        try:
            response = requests.head(url_source)
            if response.status_code==200:
                username = get_jwt_identity()
                current_user= User.query.filter_by(username=username).first()
                url_record = Url.query.filter_by(url_source=url_source).first()
                #Check if the url is already in the database
                if url_record:
                    return {"short_url": url_record.scissored_url}  
                short_url = Url.create_short_url(randint(4, 6))
                
                #add http:// or https// to the generated url
                # if url_source.startswith('http://'):
                #     short_url_http = " http://scissor.ly/"+ short_url
                # if url_source.startswith('https://'):
                #     short_url_http = " https://scissor.ly/"+ short_url
                new_url = Url(url_source=url_source, scissored_url=short_url, user=current_user .id)
                new_url.save()
                return  {"short_url": short_url}
                
            else:
                return url_source + " is not reachable "
        except requests.exceptions.RequestException:
            return " Url is not reachable"

        

@caches.cached(timeout=60)
@url_namespace.route('/custom_links/<custom_name>')
class CustomLinks(Resource):
    @url_namespace.expect(url_model)
    @jwt_required()
    def post(self, custom_name):
        data = request.get_json()
        username = get_jwt_identity()
        current_user= User.query.filter_by(username=username).first()
        url_source = data.get('url_source')
        if not url_source.startswith('http://') and not url_source.startswith('https://'):
            url_source =  "http://" + url_source
            #Check if the url is already in the database
        url_record = Url.query.filter_by(url_source=url_source).first()
        if url_record:
            return {"short_url": url_record.scissored_url}  
        short_url = Url.create_custom_url(custom_name)
        
        #add http:// or https// to the generated url
        # if url_source.startswith('http://'):
        #     short_url_http = "http://scissor.ly/"+ short_url
        # if url_source.startswith('https://'):
        #     short_url_http = "https://scissor.ly/"+ short_url
        new_url = Url(url_source=url_source, scissored_url=short_url, user=current_user.id)
        new_url.save()
        return  {"short_url":short_url}


@caches.cached(timeout=60)
@url_namespace.route('/redirect/<scissored_url>')
@jwt_required()
class Redirect_url(Resource):
    def get(self, scissored_url):
        url_record = Url.query.filter_by(scissored_url=scissored_url).first()
        if url_record:
            url_record.clicks +=1
            url_record.save()
            return redirect(url_record.url_source, HTTPStatus.FOUND)
        else:
            return {"error": "url not found"}
                

@caches.cached(timeout=60)           
@url_namespace.route('/analysis/<short_url>')
@jwt_required()
class Analytics(Resource):
    def get(self, short_url):
        url_record =Url.query.filter_by(scissored_url=short_url).first()
        if url_record:
            created_time = url_record.created_at
            formatted_time = Url.getTime(created_time)
            history= {
            "url_source ":url_record.url_source,
            "short_url" : url_record.scissored_url,
            "create Time" : formatted_time,
            "Number of Clicks": url_record.clicks
            }
            return history
        return {"error": "no such url"}

                                                                    
@url_namespace.route('/linkhistory')
class LinkHistory(Resource):
    @url_namespace.marshal_list_with(url_history)
    @jwt_required()
    def get(self):
        # url_record = Url.get_url_id(user_id)
        username = get_jwt_identity()
        current_user = User.query.filter_by(username=username).first()
        current_user_links= current_user.url
        return current_user_links
        





        