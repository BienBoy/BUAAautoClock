class NoneUsernameException(Exception):
    def __init__(self, err='未填写学号'):
        Exception.__init__(self, err)


class NonePasswordException(Exception):
    def __init__(self, err='未填写密码'):
        Exception.__init__(self, err)


class NonePayloadException(Exception):
    def __init__(self, err='未填写payload'):
        Exception.__init__(self, err)


class UsernameOrPasswordException(Exception):
    def __init__(self, err='学号或密码错误'):
        Exception.__init__(self, err)


class AlreadySubmitException(Exception):
    def __init__(self, err='今日已上报'):
        Exception.__init__(self, err)


class EarlyException(Exception):
    def __init__(self, err='今日已上报'):
        Exception.__init__(self, err)


class SendkeyException(Exception):
    def __init__(self, err='sendkey填写错误'):
        Exception.__init__(self, err)
