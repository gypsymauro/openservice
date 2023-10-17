import requests
import json
import re
import base64
import configparser
import logging

log_levels = {'DEBUG': logging.DEBUG, 
              'INFO': logging.INFO,
              'WARNING': logging.WARNING,
              'ERROR': logging.ERROR,
              }


class openService():
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('openservice.ini')
        self.auth_token=config.get('default','auth_token')
        self.url_api = config.get('default','url_api')
        self.debug = config.getboolean('default','debug',fallback=True)
        self.apiread = self.url_api + "/content/read"
        self.apicreate = self.url_api + "/content/create"
        self.apiupdate = self.url_api + "/content/update"
        self.apisearch = self.url_api + "/content/search"
        self.apidelete = self.url_api + "/content/delete"
        self.log = logging.getLogger(__name__)
        logging.basicConfig()
        self.log.setLevel(log_levels[config.get('default','log_level',fallback='DEBUG')])

                
    def prettyPrintRequest(self,req):
        self.log.debug("=================================================")
        
        self.log.debug('{}\n{}\r\n{}\r\n\r\n{}'.format(
            '-----------START-----------',
            req.method + ' ' + req.url,
            '\r\n'.join('{}: {}'.format(k, v) for k, v in req.headers.items()),
            req.body,
        ))
        self.log.debug("=================================================")

    def printResponse(self,response):
        self.log.info('Response status code %s' % response.status_code)
        self.log.debug(response.headers)
        self.log.debug(response.encoding)
        self.log.debug(response.text)
        self.log.debug(response.json())                
       
    def doRequest(self,method,url,querystring={},headers={},json={}):
        _querystring = { }
        _querystring = {**_querystring,**querystring}
        _headers = {"Content-Type":"application/json",
                    "Authorization": "Basic %s" % self.auth_token}

        _headers = {**_headers,**headers}

        request = requests.Request(method, url, headers=_headers, params=_querystring,json=json)
        prepared = request.prepare()


        if self.debug:
            self.prettyPrintRequest(prepared)

        s = requests.Session()
        self.log.info('>>> Calling method %s on %s' % (method, url))
        response = s.send(prepared)

        return response


    def read(self,data):
        # data = id
        response = self.doRequest("GET","%s/%s" % (self.apiread,data))

        self.printResponse(response)
        return response        

    def create(self,data):
        #json_data = json.dumps(data).encode('utf-8')

        response = self.doRequest("POST",self.apicreate,json=data)

        self.printResponse(response)
        return response        

    def update(self,data):
        response = self.doRequest("POST",self.apiupdate,json=data)

        self.printResponse(response)
        return response        
        
    def delete(self,data):

        delete_url = self.apidelete+ ("/%s" % data)
        response = self.doRequest("DELETE",delete_url,json=data)

        self.printResponse(response)
        return response        

    def search(self,data):

        response = self.doRequest("GET",self.apisearch + "/" + data)

        self.printResponse(response)
        return response


if __name__ == "__main__":
    os = openService()        


    test = [
        'create',
        'search',        
        'read',
        'update',
#        'delete'
    ]
    

    if 'create' in test:
        with open("file.pdf", "rb") as file:
            b64_file_content= base64.b64encode(file.read())        
#            data = {"metadata":
#                    {
#                        "remoteId": "test-cartella",
#		        "classIdentifier": "cartella",
#		        "parentNodes": [
#		            177723
#		        ],
#		        "sectionIdentifier": "standard"
#	            },
#	            "data": {
#		        "oggetto": "Test Cartella",
#                    }
                    
#            response=os.create(data)


            data = {"metadata":
                    {
                        "remoteId": "test-deliberazione",
		        "classIdentifier": "deliberazione",
		        "parentNodes": [
		            177723
		        ],
		        "sectionIdentifier": "standard"
	            },
	            "data": {
		        "oggetto": "Test Deliberazione",
		        "organo_competente": [
		            "riva_organopolitico-1"
		        ],
		        "numero": 123,
		        "anno": 2022,
                        "file": {
		            "filename": "test.pdf",
                            "file": b64_file_content.decode("ascii")},
                    }
                }
            
            response=os.create(data)

            if response.status_code == 200:
                print("<<< Id: %s url: %s" % (response.json()['result']['content']['metadata']['id'],
                                          response.json()['result']['content']['metadata']['link']))        
            
            

    if 'read' in test:
        data = "test-deliberazione"
        response=os.read(data)
        print("remoteId: %s" % data)                  

    if 'update' in test:
        with open("file.pdf", "rb") as file:
            b64_file_content= base64.b64encode(file.read())        

            data = {"metadata":{
            "remoteId": "test-deliberazione"
	    },
	    "data": {
		"iter": [],
		"allegati": [
		    {
		    "filename": "allegato.pdf",
                    "file":b64_file_content.decode("ascii")
                    },
                ]
            }
            }
            
        response=os.update(data)
        print("remoteId: %s" %  data['metadata']['remoteId'])                  

    if 'delete' in test:
        data="test-deliberazione"
        response=os.delete(data)
        print("remoteId: %s" %  data)                                


    if 'search' in test:
        response=os.search("classes [deliberazione] sort [published=>desc]")
        if response.status_code == 200:
            print("<<< # Record: %s" % response.json()["totalCount"])



        
        
        
        
        

 
