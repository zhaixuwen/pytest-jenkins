import os
import smtplib
import time

_user = "qwer@163.com"
_pwd = "qwer"
now_time = time.strftime('%Y-%m-%d-%H-%M-%S')


# 发送邮件
class SendEmail:
    def send_mail(
            self,
            email_to,
            text='Mail service to trigger, please go xxx view'):
        text = text
        SUBJECT = "Mail service verification"
        BODY = '\r\n'.join(("From: %s" % _user, "TO: %s" % email_to,
                            "subject: %s" % SUBJECT, "", text))

        email = smtplib.SMTP_SSL("smtp.163.com")
        email.login(_user, _pwd)
        try:
            email.sendmail(_user, email_to, BODY)
            email.close()
            print('Email Send Successful.')
        except Exception as e:
            print(e, "Email Send Failed.")


# 向企业微信机器人推送消息
class WechatMessage:
    # 测试环境机器人
    QA_PATH = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=1234'
    # 生产环境机器人
    PRD_PATH = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send\?key\=2234'

    @classmethod
    def send_message(cls, env, message, mentioned_mobile_list=[]):
        path = None
        if env == 'qa':
            path = cls.QA_PATH
        elif env == 'prd':
            path = cls.PRD_PATH

        if mentioned_mobile_list:
            # 如果需要@人
            mentioned_mobile_str = '['
            for mobile in mentioned_mobile_list:
                mentioned_mobile_str += '\"{}\",'.format(mobile)
            mentioned_mobile_str = mentioned_mobile_str[0:-1] + ']'
            term = "curl \'%s\' -H 'Content-Type: application/json' -d '{\"msgtype\": \"text\", \"text\": {\"content\": " \
               "\"%s\", \"mentioned_mobile_list\": %s}}'" % (path, message, mentioned_mobile_str)
        else:
            # 不需要@人走原来的逻辑
            term = "curl %s -H 'Content-Type: application/json' -d '{\"msgtype\": \"text\", \"text\": {\"content\": " \
            "\"%s\"}}'" % (path, message)
        os.system(term)
