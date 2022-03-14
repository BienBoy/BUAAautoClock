from BUAAClock import BUAAClock
from error import *
import logging
import json

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')


if __name__ == '__main__':
    data = json.load(open('data.json', 'rb'))
    clock = BUAAClock(data['username'], data['password'], data['payload'],
                      data['sendkey'], data['channel'])
    try:
        clock.submit_form()
        logging.info('打卡成功！')
    except NoneUsernameException:
        logging.error('未填写学号')
    except NonePasswordException:
        logging.error('未填写密码')
    except NonePayloadException:
        logging.error('未填写payload')
    except UsernameOrPasswordException:
        logging.error('账号或密码错误')
    except AlreadySubmitException:
        logging.error('今日已填报')
    except EarlyException:
        logging.error('未到打卡时间')
    except SendkeyException:
        logging.error('sendkey有误')
    except Exception:
        logging.error('未知错误')
