from bottle import Bottle, HTTPResponse, request
from app.services.files import Files

file_resource = Bottle()


@file_resource.route('/files', 'POST')
def store_file():
    if len(request.files) < 1 or not request.files.get('file'):
        return HTTPResponse({'msg': 'Arquivo não encontrado na requisição'}, status=400)

    file = request.files['file']
    Files().store(file.raw_filename, file.file, file.content_type)
    return HTTPResponse({'msg': 'Ok'}, status=200)

