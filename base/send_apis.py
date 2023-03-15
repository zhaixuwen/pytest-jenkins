import json
import time
import pytest
from base.do_assert import DoAssert
from base.do_extract import DoExtract
from base.do_header import DoHeader
from base.do_request import DoRequest
from base.do_url import DoUrl


class SendRequest:
    @classmethod
    def single_request(cls, env, server, prefix, param, variables, log):
        """
        单用户请求接口
        """
        if param['run'] == 'no':
            return
        if param['delay'] is not None:
            time.sleep(int(param['delay']))
            log.warning(f'delay {param["delay"]} 秒钟')

        log.info('Request module and desc -> ' + param['module'] + '/' +
                 param['description'])
        try:
            # 拼接请求url
            url = DoUrl.assemble_url(prefix, param['url'])
            # 填充token信息和header信息
            # 如果是monitor监控服务，并且没有指定account，则header中不需要传递token
            if server == 'monitor' and param['account'] is None:
                param['account'] = 'robot'
            header = DoHeader.assemble_header(
                server, variables['tokens'][param['account']],
                param['content_type'])
            # 替换url中的变量
            url = DoExtract.format_string(url, variables)
            # 替换请求体param中的变量
            data = DoExtract.format_string(param['param'], variables)
            # 替换jsonpath表达式中的变量
            param_jsonpath = DoExtract.format_string(param['jsonpath'],
                                                     variables)
            # 处理文件并发送请求
            file = None
            if param['file_name'] is not None:
                file = '_'.join([param['content_type'], param['file_name']])

            r = DoRequest.do_request(env, server, log, param['method'], url,
                                     header, json.loads(data), file)
            # 断言响应的key,value和json
            result = DoAssert.total_assert(log, r, int(param['response_code']),
                                           param['assert_key'],
                                           param['assert_value'],
                                           param['compared_resp'],
                                           param['exclude_paths'], env, server)
        except Exception as e:
            result = '请求或校验出现异常！'
            log.error(e)

        # 持久化断言失败的信息
        if result != {}:
            result_info = {
                "id": param["id"],
                "module": param["module"],
                "description": param["description"],
                "url": param["url"],
                "results": result
            }
            variables['errors'].append(result_info)

            pytest.fail('-Failed-')

        # 提取响应中的变量
        DoExtract.extract_variable(param_jsonpath, param['regex'], r,
                                   variables, log)
