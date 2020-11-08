# -*- coding:utf-8 -*-

class PositionInfo(object):

    def __init__(self, start_up_money):

        self.start_up_money = start_up_money

        self.left_money = 0
        self.lock_money = 0

    def get_info(self):
        result = "start_up_money %s \n left_money %s \n lock_money %s\n"
        return result
