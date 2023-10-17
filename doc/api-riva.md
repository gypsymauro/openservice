### Create 
`POST https://www.comune.rivadelgarda.tn.it/api/opendata/v2/content/create`

restituisce:
```
{
	"result": {
		"message": "success",
		"method": "create",
		"content": {
			"metadata": {
				"id": 273891,
				"remoteId": "test-api",
				"classIdentifier": "infobox",
				[...]
			}
		}
	}
}
```	

### Read
`GET https://www.comune.rivadelgarda.tn.it/api/opendata/v2/content/read/{id|remoteId}`

restituisce:
```
{
	"metadata": {
		"id": 273891,
		"remoteId": "test-api",
		"classIdentifier": "infobox",
		[...]
	},
	"data": {
		"identificatore-campo": "valore-campo",
		"identificatore-campo-2": "valore-campo-2",
		[...]
	}
}
```

### Update
`POST https://www.comune.rivadelgarda.tn.it/api/opendata/v2/content/update`

restituisce:
```
{
	"result": {
		"message": "success",
		"method": "update",
		"content": {
			"metadata": {
				"id": 273891,
				"remoteId": "test-api",
				"classIdentifier": "infobox",
				[...]
			}
		}
	}
}
```	

### Delete
`DELETE https://www.comune.rivadelgarda.tn.it/api/opendata/v2/content/delete/{id|remoteId}`

restituisce:
```
{
	"result": {
		"message": "success",
		"method": "delete",
		"content": 273891
	}
}
```

### Search
`GET https://www.comune.rivadelgarda.tn.it/api/opendata/v2/content/search/{query}`

Esempio: `https://www.comune.rivadelgarda.tn.it/api/opendata/v2/content/search/classes [deliberazione] sort [published=>desc]`
Vedi https://github.com/Opencontent/openservices/blob/master/doc/06-search-query.md
