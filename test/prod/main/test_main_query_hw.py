import sys

sys.path.append('..')
import pytest
from base.do_case import DoCase
from base.do_token import DoToken
from base.send_apis import SendRequest
from test.conftest import variables


@pytest.mark.prod
@pytest.mark.main_query
@pytest.mark.hw
class TestProdMainQueryHw:
    FILE_PATH = 'testcase/prod/main/main_query_hw.xlsx'

    config, apis, account = DoCase.get_case_info(FILE_PATH)
    server = config[0]['server']
    env = config[0]['env']
    prefix = config[0]['prefix']

    @pytest.mark.parametrize('user', account)
    def test_login(self, user, log):
        token = DoToken.get_token(self.server, self.prefix, user['username'],
                                  user['password'], log)
        log.info(f'Token -> {token}')
        assert '失败' not in token
        variables['tokens'][user['description']] = token

    @pytest.mark.parametrize('api', apis)
    def test_apis(self, api, log):
        SendRequest.single_request(self.env, self.server, self.prefix, api,
                                   variables, log)
