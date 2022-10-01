
class WithdrawLink():
    def __init__(self, url, title, minWithdrawable, maxWithdrawable, uses, waitTime, webhookUrl):
        self.__url=url
        self.__title=title
        self.__minWithdrawable=minWithdrawable
        self.__maxWithdrawable=maxWithdrawable
        self.__uses=uses
        self.__waitTime=waitTime
        self.__webhookUrl=webhookUrl

    def get_url(self):
        return self.__url

    def get_title(self):
        return self.__title

    def get_minWithdrawable(self):
        return int(self.__minWithdrawable)

    def get_maxWithdrawable(self):
        return int(self.__maxWithdrawable)

    def get_uses(self):
        return int(self.__uses)

    def get_waitTime(self):
        return int(self.__waitTime)

    def get_webhookUrl(self):
        return self.__webhookUrl