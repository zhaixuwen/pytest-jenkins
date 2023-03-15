import re

from jsonpath import jsonpath


class DoExtract:
    @classmethod
    def extract_variable(cls, json_path, regex, data, save_dict, logg):
        # 提取响应中的变量
        if json_path is not None:
            data = data.json()
            extract_list = json_path.split('\n')
            for extract in extract_list:
                json_path = extract.split(',')[0]
                variable_name = extract.split(',')[1]
                save_dict[variable_name] = DoExtract.extract_json(data, json_path)
        if regex is not None:
            data = data.text
            extract_list = regex.split('\n')
            for extract in extract_list:
                regex_path = extract.split(',')[0]
                regex_index = extract.split(',')[1]
                variable_name = extract.split(',')[2]
                save_dict[variable_name] = DoExtract.extract_regex(data, regex_path, regex_index)
        logg.info(f'global variables --> {save_dict}')

    @staticmethod
    def extract_regex(data, regex_path, regex_index):
        # 通过正则表达式提取数据
        results = re.findall(regex_path, str(data))
        return results[int(regex_index)]

    @staticmethod
    def extract_json(data, json_path):
        # 通过jsonpath表达式提取数据
        return jsonpath(data, json_path)[0]

    @staticmethod
    def find_variable(string):
        # 查找字符串中的变量
        # 如果从'abc${d}ef'中查找，返回${d}
        return re.findall(r'\$\{[^}]+\}', string)

    @staticmethod
    def format_string(text, variable_pool):
        if text is not None:
            # 使用上面find_variable方法，提取字符串中的变量
            # 如传入'abc${d}ef'，返回${d}, d
            variables = DoExtract.find_variable(text)
            if not variables:
                return text
            for variable in variables:
                if variable not in ['${all}', '${type}']:
                    text = text.replace(variable, str(variable_pool[variable[2:-1]]))
        return text
