
class WithdrawLink():
    def __init__(self, url, title, min_withdrawable, max_withdrawable, uses, wait_time, webhook_url):
        self.__url=url
        self.__title=title
        self.__min_withdrawable=min_withdrawable
        self.__max_withdrawable=max_withdrawable
        self.__uses=uses
        self.__wait_time=wait_time
        self.__webhook_url=webhook_url

    def get_url(self):
        return self.__url

    def get_title(self):
        return self.__title

    def get_min_withdrawable(self):
        return int(self.__min_withdrawable)

    def get_max_withdrawable(self):
        return int(self.__max_withdrawable)

    def get_uses(self):
        return int(self.__uses)

    def get_wait_time(self):
        return int(self.__wait_time)

    def get_webhook_url(self):
        return self.__webhook_url