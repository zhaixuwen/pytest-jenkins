import requests


class DoRequest:
    @classmethod
    def do_request(cls, env, server, logg, method, url, headers, data, file=None,):
        logg.info(f'Request url --> {url}')
        logg.info(f'Request header --> {headers}')
        logg.info(f'Request data --> {data}')
        logg.info(f'Request file --> {file}')

        if data is None:
            data = {}
        
        resp = None
        if file is not None:
            file_type = None
            file_model = file.split('_')[0]
            file_name = file.split('_')[1]
            if file.split('.')[-1] == 'xlsx':
                file_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            elif file.split('.')[-1] == 'pdf':
                file_type = 'application/pdf'
                
            files = [(file_model, (file_name, open(f'resources/{env}/{server}/{file_name}', 'rb'), file_type))]
            logg.info(f'Request file --> {files}')
            resp = requests.request(method=method, url=url, headers=headers, data=data, files=files)
        else:
            if headers['Content-Type'] == 'application/x-www-form-urlencoded':
                resp = requests.request(method=method, url=url, headers=headers, data=data)
            if headers['Content-Type'] == 'application/json':
                resp = requests.request(method=method, url=url, headers=headers, json=data)
        logg.info(f'Request response code --> {resp.status_code}')
        logg.info(f'Request response --> {resp.text}')
        return resp
