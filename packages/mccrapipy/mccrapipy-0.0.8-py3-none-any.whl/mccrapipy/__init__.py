import requests

class item():
    def __init__(self,num_id,img_url,name,response):
        self.num_id = num_id
        self.img_url = img_url
        self.name = name
        self.response = response

def api(path=''):
    return ('https://mccrapi.alejandrogorrze.repl.co/api/v1/items?' + path)

def get(num_id=-1,name=7):
    if num_id == -1 and name == 7:
        return requests.get(api())
    elif num_id == -1:
        return requests.get(api(path='name='+name))   
    elif name == 7:
        resp =  requests.get(api(path='id='+str(num_id)))
        return item(num_id=resp.json()[0]['num_id'],img_url=resp.json()[0]['img_url'],name=resp.json()[0]['name'],response=resp)
        
    