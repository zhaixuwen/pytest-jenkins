class DoHeader:
    @classmethod
    def assemble_header(cls, server, token, content_type):
        # 设置content-type和token
        headers = {}
        if content_type == 'json':
            headers['Content-Type'] = 'application/json'
            # headers['Accept'] = 'application/json;charset=UTF-8'
        if server == 'outing':
            headers['access_token'] = token
        elif server == 'monitor':
            if token == 'robot_token':
                pass
            else:
                headers['access_token'] = token
        else:
            headers['Authorization'] = f'Bearer {token}'
        return headers
