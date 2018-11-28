
from flask import Flask
from flask_restful import Resource, Api 


app = Flask(__name__)
api = Api(app)

proverbs_list = [{'locale': 'English', 'proverb': 'A bird in hand is worth two in the bush'}]

class Proverbs(Resource):

    def __init__(self):
        self.proverbs = proverbs_list

    def get(self):
        return self.proverbs


@app.route('/', methods=['get'])
def hello():
        return "hello vincent"


api.add_resource(Proverbs, '/proverbs')

if __name__=='__main__':
    app.run(debug=True)
