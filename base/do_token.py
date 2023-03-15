import requests


class DoToken:
    # 不同业务或服务的token获取方式
    @classmethod
    def get_token(cls, server, prefix, username, password, log):
        log.info(f'服务【{server}】用户名【{username}】密码【{password}】')
        log.info(f'token请求前缀【{prefix}】')
        token = None
        if server in ['xxx', 'yyy']:
            if prefix is not None:
                for i in range(3):
                    r = requests.request(
                        'get', prefix +
                        f'/xxx/token/get?client={username}&secret={password}'
                    )
                    log.info('login resp -> ' + r.text)
                    if r.json(
                    )['resMsg'] == 'success' and r.status_code == 200:
                        token = r.json()['data']['access_token']
                        break
        elif server in ['zzz']:
            if prefix is not None:
                for i in range(3):
                    url = prefix + '/xxx/oauth'
                    body = {
                        "username": username,
                        "password": password
                    }
                    r = requests.post(url=url, data=body)
                    log.info('login resp -> ' + r.text)
                    if r.json(
                    )['token_type'] == 'bearer' and r.status_code == 200:
                        token = r.json()['access_token']
                        break

        if token is not None:
            return token
        else:
            return f'获取{server}环境{prefix}服务token失败.'

    @classmethod
    def sso_login(cls,
                  log,
                  project_id,
                  user_id,
                  company,
                  usrename,
                  cloud='aws'):
        log.info(
            f'开始获取sso登录token -> 【公司】{company}【用户名】{usrename}【projectId】{project_id}【userId】{user_id}'
        )
        log.info(f'对应云平台是{cloud}')
        url = 'https://xxx/token/ssoLogin'
        body = {"projectId": project_id, "userId": user_id}
        header = {"content-type": "application/json"}
        r = requests.post(url=url, json=body, headers=header)
        log.info(f'sso获取token结果 -> {r.text}')
        if r.status_code == 200 and r.json()['token']:
            return r.json()['token']
        else:
            return False
