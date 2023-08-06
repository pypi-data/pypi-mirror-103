import requests

def api(path=''):
    return ('https://mccrapi.alejandrogorrze.repl.co/api/v1/items?' + path)

def get(num_id=-1,name=7):
    if num_id == -1 and name == 7:
        return requests.get(api())
    elif num_id == -1:
        return requests.get(api(path='name='+name))
    elif name == 7:
        return requests.get(api(path='id='+num_id))
    