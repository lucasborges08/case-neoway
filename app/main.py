from bottle import Bottle
from app.api.v0.file_resource import file_resource

api = Bottle()
api.mount('/v0', file_resource)

if __name__ == "__main__":
    api.run(host='0.0.0.0', port='8090')
