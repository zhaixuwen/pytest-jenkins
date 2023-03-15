import json
import pytest
from jsonpath import jsonpath
from deepdiff import DeepDiff


class DoAssert:
    @classmethod
    def total_assert(cls, log, resp, excepted_code, excepted_key, excepted_value, compared_resp, exclude_paths, env, server):
        result = {}
        # 记录token失效状态
        if resp.status_code in [401, 403]:
            result['invalidToken'] = True

        if excepted_code is not None:
            log.info('校验status.')
            if resp.status_code != excepted_code:
                result['status'] = f'响应状态码校验失败: 期望 {excepted_code} 实际 {resp.status_code}'
            DoAssert.assert_status(resp.status_code, excepted_code)

        if compared_resp is not None:
            log.info('校验json.')
            if exclude_paths is None:
                json_result = DoAssert.assert_json(resp.json(), compared_resp, {}, log, env, server)
            else:
                json_result = DoAssert.assert_json(resp.json(), compared_resp, set(exclude_paths.split('\n')), log, env, server)
            if json_result != {} and json_result is not None:
                result['json'] = f'响应json校验失败: 结果 {json_result}'
                pytest.assume(json_result == {})

        if excepted_key is not None:
            log.info('校验key.')
            r = DoAssert.assert_key(resp.json(), excepted_key)
            log.info(f'校验key结果：{r}')
            assert r
            log.info('校验key完成')

        if excepted_value is not None:
            log.info('校验value.')
            DoAssert.assert_resp(resp.json(), excepted_value)
            log.info('校验value完成')

        log.warning(f"错误结果 -> {result}")
        return result

    @classmethod
    def assert_resp(cls, response, assert_resp):
        if assert_resp is None:
            return
        assert_list = assert_resp.split('\n')
        for assert_obj in assert_list:
            obj_list = assert_obj.split(',')
            # ------------get the first value of obj_list-------------
            obj_1 = obj_list[0]
            if obj_list[0] == '${all}':
                obj_1 = response
            else:
                obj_1 = jsonpath(response, obj_list[0])[0]
            # ----------------assert information type-----------------
            if obj_list[1] == '${type}':
                assert type(obj_1) == eval(obj_list[2])
            # ----------------assert information value----------------
            elif obj_list[1] == 'contains':
                assert (str(obj_1)).find(str(obj_list[3])) > 0
            elif obj_list[1] == '==':
                if obj_list[2] == 'str':
                    assert obj_1 == str(obj_list[3])
                elif obj_list[2] == 'int':
                    assert obj_1 == int(obj_list[3])
                elif obj_list[2] == 'float':
                    assert obj_1 == float(obj_list[3])
            elif obj_list[1] == '>=':
                if obj_list[2] == 'int':
                    assert obj_1 >= int(obj_list[3])
                elif obj_list[2] == 'float':
                    assert obj_1 >= float(obj_list[3])
            elif obj_list[1] == '>':
                if obj_list[2] == 'int':
                    assert obj_1 > int(obj_list[3])
                elif obj_list[2] == 'float':
                    assert obj_1 > float(obj_list[3])
            elif obj_list[1] == '<=':
                if obj_list[2] == 'int':
                    assert obj_1 <= int(obj_list[3])
                elif obj_list[2] == 'float':
                    assert obj_1 <= float(obj_list[3])
            elif obj_list[1] == '<':
                if obj_list[2] == 'int':
                    assert obj_1 < int(obj_list[3])
                elif obj_list[2] == 'float':
                    assert obj_1 < float(obj_list[3])

    @staticmethod
    def assert_status(real_status, excepted_status):
        pytest.assume(real_status == excepted_status)

    @staticmethod
    def assert_key(response, assert_keys):
        # 比较响应json的key和预设的key
        keys = assert_keys.split(',')
        # assert set(keys) == Tester.get_keys_from_json(response)
        return set(keys).issubset(DoAssert.get_keys_from_json(response))

    @staticmethod
    def get_keys_from_json(content):
        # 从json中提取所有的key,并去重返回set类型
        result_keys = set()

        def check(content):
            if type(content) == dict and content != {}:
                for i in content.keys():
                    result_keys.add(i)
                    check(content[i])
            elif type(content) == list and content != []:
                for c in content:
                    check(c)

        check(content)
        return result_keys

    @staticmethod
    def assert_json(actual_json, expected_json, exclude_paths, log, env, server):
        # 比较两个json的不同
        if expected_json.endswith('.json'):
            with open(f'resources/{env}/{server}/{expected_json}') as f:
                expected_value = json.load(f)
        else:
            expected_value = json.loads(expected_json)
        result = DeepDiff(expected_value, actual_json, exclude_paths=exclude_paths, ignore_order=True)
        log.warning('assert_json结果 -> '+str(result))
        return result
