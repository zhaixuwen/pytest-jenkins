import sys

sys.path.append('../')
from utils.exceler import DoExcel


class DoCase:
    @classmethod
    def get_case_info(cls, file_path):
        # 从测试用例文件中获取配置信息和接口信息
        case_xlsx = DoExcel(file_path)
        config = case_xlsx.get_all_data('config')
        api = case_xlsx.get_all_data('api')
        account = case_xlsx.get_all_data('account')
        return config, api, account
