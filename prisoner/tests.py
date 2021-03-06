# -*- coding: utf-8 -*-
from __future__ import division

import random

from otree.common import Currency as c, currency_range

from ._builtin import Bot
from .models import Constants
from . import views


class PlayerBot(Bot):
    def play_round(self):
        yield (views.Introduction)
        yield (views.Decision, {"decision": 'Cooperate'})
        assert 'Both of you chose to cooperate' in self.html
        assert self.player.payoff == Constants.both_cooperate_payoff
        yield (views.Results)
