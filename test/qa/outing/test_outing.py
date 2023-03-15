import sys

sys.path.append('..')
import pytest
from base.do_case import DoCase
from base.do_token import DoToken
from base.send_apis import SendRequest
from test.conftest import variables
from utils.timer import Timer


@pytest.mark.qa
@pytest.mark.outing
@pytest.mark.test
class TestQaOuting:
    FILE_PATH = 'testcase/qa/outing/outing_test.xlsx'

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
        variables['timestamp'] = Timer.get_timestamp()
        SendRequest.single_request(self.env, self.server, self.prefix, api,
                                   variables, log)
