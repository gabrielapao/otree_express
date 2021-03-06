# -*- coding: utf-8 -*-
from __future__ import division

import random

from otree.common import Currency as c, currency_range

from . import views
from ._builtin import Bot
from .models import Constants
from otree.api import SubmissionMustFail


class PlayerBot(Bot):

    cases = ['basic', 'p1_wins', 'all_0', 'all_max']

    def play_round(self):
        case = self.case

        # Introduction
        yield (views.Introduction)

        if case == 'basic':
            for invalid_bid in [-1, 11]:
                yield SubmissionMustFail(views.Bid, {"bid_amount": invalid_bid})
        if case == 'p1_wins':
            if self.player.id_in_group == 1:
                bid_amount = 2
            else:
                bid_amount = 1
        elif case == 'all_0':
            bid_amount = 0
        else: # case == 'all_max':
            bid_amount = Constants.max_allowable_bid
        yield (views.Bid, {"bid_amount": bid_amount})

        if case == 'p1_wins':
            if self.player.id_in_group == 1:
                assert 'You won the auction' in self.html
            else:
                assert 'You did not win' in self.html

        if self.player.id_in_group == 1:
            num_winners = sum([1 for p in self.group.get_players() if p.is_winner])
            assert num_winners == 1

        for field in [
            self.player.bid_amount,
            self.player.payoff,
            self.player.item_value_estimate,
            self.player.is_winner
        ]:
            assert field is not None

        yield (views.Results)
