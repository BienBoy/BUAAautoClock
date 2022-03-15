import requests
from urllib import parse
import datetime
from error import *


class BUAAClock(object):

    def __init__(self, username, password, payload, sendkey=None, channel=None):
        if username:
            self.username = username
        else:
            raise NoneUsernameException
        if password:
            self.password = password
        else:
            raise NonePasswordException
        if payload:
            self.payload = payload
        else:
            raise NonePayloadException
        self.sendkey = sendkey
        self.channel = channel
        self.session = requests.Session()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
        AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36 \
        Edg/97.0.1072.76',
            'Referer': 'https://app.buaa.edu.cn/site/buaaStudentNcov/index',
            'X-Requested-With': 'XMLHttpRequest'
        }
        self.data = self.parse_form_data()

    def login(self):
        url = 'https://app.buaa.edu.cn/uc/wap/login/check'
        data = {
            'username': self.username,
            'password': self.password
        }
        response = self.session.post(url, data=data)
        if response.json()['m'] == ' 账号或密码错误':
            raise UsernameOrPasswordException

    def parse_form_data(self):
        payload = parse.unquote(self.payload)
        data = parse.parse_qs(payload, keep_blank_values=True)
        date_of_today = datetime.date.today()
        date_of_yesterday = date_of_today - datetime.timedelta(days=1)
        data['date'] = [str(date_of_yesterday).replace('-', '')]
        return data

    def submit_form(self):
        self.login()
        url = 'https://app.buaa.edu.cn/buaaxsncov/wap/default/save'
        response = self.session.post(url, headers=self.headers, data=self.data)
        if response.status_code == 200 and response.json().get('m') == '操作成功':
            if self.sendkey:
                self.send_message_to_phone('{}体温上报成功'.format(datetime.date.today()),
                                           '{}体温已上报'.format(datetime.date.today()))
        elif response.json().get('m') == '今天已经填报了':
            if self.sendkey:
                self.send_message_to_phone('今日已上报', '{}体温已上报'.format(datetime.date.today()))
            raise AlreadySubmitException
        elif response.json().get('m') == '填报时间为每日17时至24时':
            if self.sendkey:
                self.send_message_to_phone('体温上报失败，请自行打卡',
                                           '体温上报失败：未到填报时间，请自行打卡')
            raise EarlyException
        else:
            if self.sendkey:
                self.send_message_to_phone('体温上报失败', '体温上报失败：{}，请自行上报'.format(response.json().get('m')))
            raise Exception

    def send_message_to_phone(self, title, content):
        url = f'https://sctapi.ftqq.com/{self.sendkey}.send'
        data = {
            'title': title,
            'desp': content,
            'channe': self.channel
        }
        response = requests.post(url, data=data)
        if response.json().get('40001'):
            raise SendkeyException

