# Lucas Yugi Kumagai 21110496
# Gustavo da Nóbrega Silva 21100654

import pandas as pd
from flask import Flask
import flask.scaffold
flask.helpers._endpoint_from_view_func = flask.scaffold._endpoint_from_view_func
from flask_restful import reqparse, abort, Api, Resource
import json

#iniciar flask padrÃ£o
app = Flask(__name__)
api = Api(app)

#leitura csv 
Animes = pd.read_csv('anime.csv')
#transformação para dicionário orientado a index
Animes = Animes.to_dict(orient="index")

#para abortar se não possuir nada 
def abort_if_anime_doesnt_exist(anime_id):
    if anime_id not in Animes:
        abort(404, message=f'Anime {anime_id} doesn\'t exist')

parser = reqparse.RequestParser()
parser.add_argument('MAL_ID', type=int)
parser.add_argument('Name')

#métodos get, delet, put que retornam um json  
class Anime(Resource):
    def get(self, anime_id):
        abort_if_anime_doesnt_exist(anime_id)
        return json.dumps(Animes[anime_id])

    def delete(self, anime_id):
        abort_if_anime_doesnt_exist(anime_id)
        del Animes[anime_id]
        return json.dumps(''), 204

    def put(self, anime_id):
        args = parser.parse_args()
        content = {'MAL_ID': args['MAL_ID'], 'Name': args['Name']}
        Animes[anime_id] = content
        return json.dumps(content), 201

#métodos get e post
class AnimeList(Resource):
    def get(self):
        return json.dumps(Animes)

    def post(self):
        args = parser.parse_args()
        anime_id = max(Animes.keys()) + 1
        Animes[anime_id] = {'MAL_ID': args['MAL_ID'], 'Name': args['Name']}
        return json.dumps(Animes[anime_id]), 201

#para navegar entre paginas do site, sendo a primeira pagina o json
api.add_resource(AnimeList, '/')
api.add_resource(Anime, '/anime/<int:anime_id>')


#rodar a API
if __name__ == "__main__":
    app.run(debug=True)

#hospedagem no server do heroku

# foi completo o desafio 2, assim sendo hospedado a API no server do heroku que pode ser acessado, 
# por este link https://animes2020.herokuapp.com/
