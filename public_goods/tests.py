# -*- coding: utf-8 -*-
from __future__ import division

import random

from otree.common import Currency as c, currency_range

from ._builtin import Bot
from .models import Constants
from . import views
from otree.api import SubmissionMustFail, Submission


class PlayerBot(Bot):

    cases = ['basic', 'min', 'max']

    def play_round(self):
        case = self.case
        yield (views.Introduction)

        if case == 'basic':
            assert self.player.payoff == None
            if self.player.id_in_group == 1:
                for invalid_contribution in [-1, 101]:
                    yield SubmissionMustFail(views.Contribute, {
                        'contribution': invalid_contribution})

        contribution = {
            'min': 0,
            'max': 100,
            'basic': 50,
        }[case]

        yield (views.Contribute, {"contribution": contribution})

        yield (views.Results)

        if self.player.id_in_group == 1:

            if case == 'min':
                expected_payoff = 100
            elif case == 'max':
                expected_payoff = 200
            else:
                expected_payoff = 150
            assert self.player.payoff == expected_payoff
