class DoUrl:
    @classmethod
    def assemble_url(cls, prefix, url):
        full_url = prefix + url
        # 如果请求url以http开头，则不拼装前缀
        if url.startswith('http'):
            full_url = url
        return full_url
