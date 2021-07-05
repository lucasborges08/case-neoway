from bottle import Bottle, HTTPResponse, request

file_resource = Bottle()


@file_resource.route('/file', 'POST')
def store_file():
    if len(request.files) < 1 or not request.files.get('file'):
        return HTTPResponse({'msg': 'Arquivo não encontrado'}, status=400)

    return HTTPResponse({'msg': 'Ok'}, status=200)
