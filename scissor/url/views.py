from ..utils import db
from flask_restx import Namespace, fields, Resource
from ..models.url import Url
from flask import request, redirect
from random import randint
from http import HTTPStatus



url_namespace= Namespace('url', description='Namespace for URLs')

url_model = url_namespace.model(
    "Url", {
        "url_source":fields.String()

    }
)

# url_short_model = url_namespace.model(
#     "Url", {
#         "short":fields.String()

#     }
# )






@url_namespace.route('/')
class Links(Resource):
    @url_namespace.expect(url_model)
    def post(self):
        data = request.get_json()
        url_source = data.get('url_source')
        if not url_source.startswith('http://') and not url_source.startswith('https://'):
            url_source =  "http://" + url_source
            #Check if the url is already in the database
        url_record = Url.query.filter_by(url_source=url_source).first()
        if url_record:
            return {"short_url": url_record.url_source}  
        short_url = Url.create_short_url(randint(4, 6))
        new_url = Url(url_source=url_source, scissored_url=short_url)
        new_url.save()
        return  {"short_url": short_url}

@url_namespace.route('/custom_links/<custom_name>')
class CustomLinks(Resource):
    @url_namespace.expect(url_model)
    def post(self, custom_name):
        data = request.get_json()
        url_source = data.get('url_source')
        if not url_source.startswith('http://') and not url_source.startswith('https://'):
            url_source =  "http://" + url_source
            #Check if the url is already in the database
        url_record = Url.query.filter_by(url_source=url_source).first()
        if url_record:
            return {"short_url": url_record.scissored_url}  
        short_url = Url.create_custom_url(custom_name)
        new_url = Url(url_source=url_source, scissored_url=short_url)
        new_url.save()
        return  {"short_url": short_url}


@url_namespace.route('/redirect/<scissored_url>')
class Redirect_url(Resource):
    def get(self, scissored_url):
        url_record = Url.query.filter_by(scissored_url=scissored_url).first()
        if url_record:
            url_record.clicks +=1
            url_record.save()
            return redirect(url_record.url_source, HTTPStatus.FOUND)
        else:
            return {"error": "url not found"}
                

            







        