from worker import Worker
from time import gmtime, strftime
from datetime import datetime


# {"metadata":{"id":172434,"remoteId":"riva_associazione-32293","classIdentifier":"associazione","class":"http:\/\/www.comune.rivadelgarda.tn.it\/api\/opendata\/v2\/classes\/associazione","ownerId":14,"ownerName":{"ita-IT":"Administrator User"},"mainNodeId":166247,"sectionIdentifier":"standard","stateIdentifiers":["ez_lock.not_locked","sensor.pending","privacy.public","moderation.skipped"],"published":"2015-02-02T15:11:25+01:00","modified":"2022-09-16T22:37:26+02:00","languages":["ita-IT"],"name":{"ita-IT":"ASSOCIAZIONE NUSANTARA"},"parentNodes":[502],"link":"http:\/\/www.comune.rivadelgarda.tn.it\/api\/opendata\/v2\/content\/read\/172434"},"data":{"ita-IT":{"titolo":"ASSOCIAZIONE NUSANTARA","abstract":"","indirizzo":"VIALE N.PERNICI, 22","presso":null,"cap":"38066","localita":"RIVA DEL GARDA","telefono":"328 2132262","numero_telefono1":null,"fax":null,"casella_postale":null,"email":"associazione@nusantara.it; mattheo88@gmail.com","url":null,"url_facebook":null,"circoscrizione":[],"categoria":"ASSOCIAZIONI SPORTIVE","argomento":[],"contatti":"","referente_nome":"RAFFAELLI MATTEO","referente_ruolo":null,"referente_indirizzo":"","referente_telefono":null,"referente_fax":null,"scheda":"","image":null,"gps":{"latitude":0,"longitude":0,"address":""},"cod_associazione":"0","data_inizio_validita":"2022-09-02T14:49:13+02:00","data_archiviazione":null}}}


class associazioneWorker(Worker):
    def __init__(self):
        super().__init__()
        self.remoteid = self.__class__.__name__ + '-'



    def do(self):
        dataset = self.getDataset("select *, 'associazione-' || id_anag as codice, extract( epoch from (d_mod)) as datamodifica from portale.www_associazioni limit 3")

        for record in dataset:
            remoteid=self.remoteid + str('test-riva-' + record['codice'])
            data = {"metadata":
                    {
                        "remoteId": remoteid,
		        "classIdentifier": "associazione",
		        "parentNodes": [
		            266780
		        ],
		        "sectionIdentifier": "standard"
	            },
	            "data": {
                        "titolo": record['rag_sociale'],
                        "indirizzo": record['indirizzo'] ,
                        "cap": record['cap'] ,
                        "localita": record['localita'] ,
                        "telefono": record['tel1'],
                        "email": record['e_mail'],
                        "referente_nome": record['referente'],
                        "categoria": record['desc_attivita'],
                        "url": record['home_page'],                        

                    }
                    }


            self.createOrUpdateItem(data,datetime.now())
            self.delete(remoteid)
                
            


if __name__ == "__main__":        
    aW = associazioneWorker()

    #aW.read('riva_associazione-32293')
    aW.do()
    
    
     

        

        
