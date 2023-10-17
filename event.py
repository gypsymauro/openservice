from worker import Worker
from time import gmtime, strftime
from datetime import datetime


class eventWorker(Worker):
    def __init__(self):
        super().__init__()
        self.remoteid = self.__class__.__name__ + '-'
        
    def do(self):
        dataset = self.getDataset("select * from portale.www_consiglio_comunale order by id_anag LIMIT 3")

        for record in dataset:
            remoteid=self.remoteid + str(record['id_anag'])
            data = {"metadata":
                    {
                        "remoteId": remoteid,
		        "classIdentifier": "event",
		        "parentNodes": [
		            266780
		        ],
		        "sectionIdentifier": "standard"
	            },
	            "data": {
                        "titolo": record['nominativo'],
                        "from_time": strftime("%Y-%m-%d %H:%M:%S", gmtime()) ,
                        "to_time": strftime("%Y-%m-%d %H:%M:%S", gmtime()),
                        "tipo_evento":[{"id":499,}],
                        "luogo_svolgimento":"Sedi diverse",
                        "informazioni":"<p>Organizzatore: Comune Di Riva Del Garda</p>",
                        "orario_svolgimento":"Dalle 20:30 alle 23:30"
                    }
                    }


            #self.createOrUpdateItem(data,datetime.now())
            self.delete(remoteid)
                
            


if __name__ == "__main__":        
    eW = eventWorker()

    eW.do()
    
    
     

        

        
