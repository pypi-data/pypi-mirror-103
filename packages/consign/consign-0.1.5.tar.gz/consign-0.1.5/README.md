# Consign

Consign is a simple library to validate and store data in different sources.

```
>>> import consign
>>> import requests
>>> r = requests.get('https://api.github.com/user', auth=('user', 'pass'))
>>> r.status_code
200
>>> consign.text(r.text, './local_file.txt')
>>> consign.json(r.json(), './local_file.json')
>>> consign.blob(r.json(), './cloud_file.json', provider='azure', connection_string=private_keys, container=container_name)
```

Consign allows you to validate and store data extremely easily, whether in a 
local file or in a cloud storage.
