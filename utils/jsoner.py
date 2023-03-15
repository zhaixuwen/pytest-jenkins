import re
import json


# 读取json文件内容为dict
def read_json(file):
    with open(file, mode='r') as f:
        return json.loads(f.read())


# 将dict内容写入文件
def overwrite_json(file, token):
    with open(file, mode='w', encoding='utf8') as f:
        return json.dump(token, f)


# 查找字符串中用${}括起来的字符
def re_replace(content):
    print(content)
    value = re.findall(r'\$\{[^}]+\}', content)[0]  # 带${}括号的变量:${test}
    return value, value[2:-1]
