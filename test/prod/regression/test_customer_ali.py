import sys

sys.path.append('..')
import pytest
from base.do_case import DoCase
from base.do_token import DoToken
from base.send_apis import SendRequest
from test.conftest import variables


@pytest.mark.prod
@pytest.mark.regression
@pytest.mark.customer_ali
class TestProdRegression:
    FILE_PATH = 'testcase/prod/regression/customer_ali.xlsx'

    config, apis, accounts = DoCase.get_case_info(FILE_PATH)
    server = config[0]['server']
    env = config[0]['env']
    prefix = config[0]['prefix']

    @pytest.mark.parametrize('api', apis)
    @pytest.mark.parametrize('account', accounts)
    def test_api(self, account, api, log):
        company = account['company']
        user_id = account['username']
        project_id = account['password']
        username = account['description']
        token = DoToken.sso_login(log, project_id, user_id, company, username, cloud='ali')
        if token:
            variables['tokens'][username] = token
            api['company'] = company
            api['account'] = username
            SendRequest.single_request(self.env, self.server, self.prefix, api, variables, log)
        else:
            log.error("sso获取token异常,请检查!!!")
            assert False
