import os

import json

from src import Const


class Statistics:
    def __init__(self):
        self.killing = 0
        self.wins = 0
        self.loses = 0

    def load_statistics(self):
        if os.path.exists(Const.PATH + 'data/statistics.json'):
            with open(Const.PATH + 'data/statistics.json', 'r') as file:
                settings_json = json.load(file)
                self.killing = settings_json.get('killing', self.killing)
                self.wins = settings_json.get('wins', self.wins)
                self.loses = settings_json.get('loses', self.loses)

    def save_statistics(self):
        with open(Const.PATH + 'data/statistics.json', 'w') as file:
            json.dump(self.to_json(), file)

    def to_json(self):
        return {
            'killing': self.killing,
            'wins': self.wins,
            'loses': self.loses
        }

    def __add__(self, other):
        if isinstance(other, Statistics):
            result = Statistics()
            result.killing = self.killing + other.killing
            result.wins = self.wins + other.wins
            result.loses = self.loses + other.loses
            return result
        else:
            raise TypeError("Unsupported operand type(s) for +: 'Statistics' and '{}'".format(type(other).__name__))
