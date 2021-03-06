import os
from os import environ

import dj_database_url
from boto.mturk import qualification

import otree.settings


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# the environment variable OTREE_PRODUCTION controls whether Django runs in
# DEBUG mode. If OTREE_PRODUCTION==1, then DEBUG=False
if environ.get('OTREE_PRODUCTION') not in {None, '', '0'}:
    DEBUG = False
else:
    DEBUG = True

ADMIN_USERNAME = 'admin'

# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')


# don't share this with anybody.
SECRET_KEY = '96nwa*zoa$xhkszukze_a33&s7nm6adewc+l%$ag(lg$71x2zh'

# To use a database other than sqlite,
# set the DATABASE_URL environment variable.
# Examples:
# postgres://USER:PASSWORD@HOST:PORT/NAME
# mysql://USER:PASSWORD@HOST:PORT/NAME

DATABASES = {
    'default': dj_database_url.config(
        default='sqlite:///' + os.path.join(BASE_DIR, 'db.sqlite3')
    )
}

# AUTH_LEVEL:
# If you are launching a study and want visitors to only be able to
# play your app if you provided them with a start link, set the
# environment variable OTREE_AUTH_LEVEL to STUDY.
# If you would like to put your site online in public demo mode where
# anybody can play a demo version of your game, set OTREE_AUTH_LEVEL
# to DEMO. This will allow people to play in demo mode, but not access
# the full admin interface.

AUTH_LEVEL = environ.get('OTREE_AUTH_LEVEL')


# setting for integration with AWS Mturk
AWS_ACCESS_KEY_ID = environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = environ.get('AWS_SECRET_ACCESS_KEY')


# e.g. EUR, CAD, GBP, CHF, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = False

# e.g. en, de, fr, it, ja, zh-hans
# see: https://docs.djangoproject.com/en/1.9/topics/i18n/#term-language-code
LANGUAGE_CODE = 'en'

# if an app is included in SESSION_CONFIGS, you don't need to list it here
INSTALLED_APPS = ['otree']

# SENTRY_DSN = ''

DEMO_PAGE_INTRO_TEXT = """
<ul>
    <li>
        <a href="https://github.com/oTree-org/otree" target="_blank">
            oTree on GitHub
        </a>.
    </li>
    <li>
        <a href="http://www.otree.org/" target="_blank">
            oTree homepage
        </a>.
    </li>
</ul>
<p>
    Here are various games implemented with oTree. These games are all open
    source, and you can modify them as you wish.
</p>
"""

ROOMS = [
    {
        'name': 'econ101',
        'display_name': 'Econ 101 class',
        'participant_label_file': '_rooms/econ101.txt',
    },
    {
        'name': 'live_demo',
        'display_name': 'Room for live demo (no participant labels)',
    },
]


# from here on are qualifications requirements for workers
# see description for requirements on Amazon Mechanical Turk website:
# http://docs.aws.amazon.com/AWSMechTurk/latest/AWSMturkAPI/ApiReference_QualificationRequirementDataStructureArticle.html
# and also in docs for boto:
# https://boto.readthedocs.org/en/latest/ref/mturk.html?highlight=mturk#module-boto.mturk.qualification

mturk_hit_settings = {
    'keywords': ['easy', 'bonus', 'choice', 'study'],
    'title': 'Title for your experiment',
    'description': 'Description for your experiment',
    'frame_height': 500,
    'preview_template': 'global/MTurkPreview.html',
    'minutes_allotted_per_assignment': 60,
    'expiration_hours': 7*24, # 7 days
    #'grant_qualification_id': 'YOUR_QUALIFICATION_ID_HERE',# to prevent retakes
    'qualification_requirements': [
        # qualification.LocaleRequirement("EqualTo", "US"),
        # qualification.PercentAssignmentsApprovedRequirement("GreaterThanOrEqualTo", 50),
        # qualification.NumberHitsApprovedRequirement("GreaterThanOrEqualTo", 5),
        # qualification.Requirement('YOUR_QUALIFICATION_ID_HERE', 'DoesNotExist')
    ]
}


# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = {
    'real_world_currency_per_point': 0.01,
    'participation_fee': 1.00,
    'num_bots': 6,
    'doc': "",
    'mturk_hit_settings': mturk_hit_settings,
}

SESSION_CONFIGS = [
    {
        'name': 'PTT_express_FM_n2',
        'display_name': "Free Message, 2 players",
        'real_world_currency_per_point': 1,
        'num_demo_participants': 2,
        'targetIncome': [10.3],
        'num_readers': 0,
        'reader_endowment': [12],  # to be extended to a list for when there is more than one readers
        'Params': [
        {'treat': 'FM', 'val_typ':  None, 'elic_met':  None, 'BDM_typ':   None, 'Met_par':           None, 'end': [3, 4]},
        ],
        'app_sequence': ['zFake_searchTask','PTT_expression', 'payment_info'],
        'debug': True
    },
    {
        'name': 'PTT_express_NM_n2',
        'display_name': "No Message, 2 players",
        'real_world_currency_per_point': 1,
        'num_demo_participants': 2,
        'targetIncome': [10.3],
        'num_readers': 0,
        'reader_endowment': [12],  # to be extended to a list for when there is more than one readers
        'Params': [
        {'treat': 'NM', 'val_typ':  None, 'elic_met':  None, 'BDM_typ':   None, 'Met_par':           None, 'end': [3, 4]},
        ],
        'app_sequence': ['zFake_searchTask','PTT_expression', 'payment_info'],
        'debug': True
    },
# DM WTP BLOCK
    {
        'name': 'PTT_express_DM_N2_WTP_BDM_CONT__0_end',
        'display_name': "Direct Message, N=2, WTP, BDM Continuous [0, endowment] ",
        'real_world_currency_per_point': 1,
        'num_demo_participants': 2,
        'targetIncome': [10.3],
        'num_readers': 0,
        'reader_endowment': [11],  # to be extended to a list for when there is more than one readers
        'Params': [
{'treat': 'DM', 'val_typ': 'WTP','elic_met': 'BDM', 'BDM_typ': 'CONT', 'Met_par': [0, 'end'], 'end': [5, 3]},
        ],
        'app_sequence': ['zFake_searchTask','PTT_expression', 'payment_info'],
        'debug': True
    },
    {
        'name': 'PTT_express_DM_N2_WTP_BDM_LIST__0_av_inc',
        'display_name': "Direct Message, N=2, WTP, BDM List [0, available_income] ",
        'real_world_currency_per_point': 1,
        'num_demo_participants': 2,
        'targetIncome': [10.3],
        'num_readers': 0,
        'reader_endowment': [11],  # to be extended to a list for when there is more than one readers
        'Params': [
{'treat': 'DM', 'val_typ': 'WTP', 'elic_met': 'BDM', 'BDM_typ': 'LIST', 'Met_par': [0, 'av_inc', 0.2], 'end': [4, 3]},
        ],
        'app_sequence': ['zFake_searchTask', 'PTT_expression', 'payment_info'],
        'debug': True
    },
    {
        'name': 'PTT_express_DM_N2_WTP_SOP',
        'display_name': "Direct Message, N=2, WTP, SOP ",
        'real_world_currency_per_point': 1,
        'num_demo_participants': 2,
        'targetIncome': [10.3],
        'num_readers': 0,
        'reader_endowment': [11],  # to be extended to a list for when there is more than one readers
        'Params': [
{'treat': 'DM', 'val_typ': 'WTP', 'elic_met': 'SOP', 'BDM_typ': None, 'Met_par': [.98], 'end': [4, 3]},
        ],
        'app_sequence': ['zFake_searchTask', 'PTT_expression', 'payment_info'],
        'debug': True
    },
# DM WTA BLOCK
    {
        'name': 'PTT_express_DM_N2_WTA_BDM_CONT__0_end',
        'display_name': "Direct Message, N=2, WTA, BDM Continuous [0, endowment] ",
        'real_world_currency_per_point': 1,
        'num_demo_participants': 2,
        'targetIncome': [10.3],
        'num_readers': 0,
        'reader_endowment': [11],  # to be extended to a list for when there is more than one readers
        'Params': [
{'treat': 'DM', 'val_typ': 'WTA','elic_met': 'BDM', 'BDM_typ': 'CONT', 'Met_par': [0, 'end'], 'end': [5, 3]},
        ],
        'app_sequence': ['zFake_searchTask','PTT_expression', 'payment_info'],
        'debug': True
    },
    {
        'name': 'PTT_express_DM_N2_WTA_BDM_LIST__0_av_inc',
        'display_name': "Direct Message, N=2, WTA, BDM List [0, available_income] ",
        'real_world_currency_per_point': 1,
        'num_demo_participants': 2,
        'targetIncome': [10.3],
        'num_readers': 0,
        'reader_endowment': [11],  # to be extended to a list for when there is more than one readers
        'Params': [
{'treat': 'DM', 'val_typ': 'WTA', 'elic_met': 'BDM', 'BDM_typ': 'LIST', 'Met_par': [0, 'av_inc', 0.2], 'end': [4, 3]},
        ],
        'app_sequence': ['zFake_searchTask', 'PTT_expression', 'payment_info'],
        'debug': True
    },
    {
        'name': 'PTT_express_DM_N2_WTA_SOP',
        'display_name': "Direct Message, N=2, WTA, SOP ",
        'real_world_currency_per_point': 1,
        'num_demo_participants': 2,
        'targetIncome': [10.3],
        'num_readers': 0,
        'reader_endowment': [11],  # to be extended to a list for when there is more than one readers
        'Params': [
{'treat': 'DM', 'val_typ': 'WTA', 'elic_met': 'SOP', 'BDM_typ': None, 'Met_par': [.98], 'end': [4, 3]},
        ],
        'app_sequence': ['zFake_searchTask', 'PTT_expression', 'payment_info'],
        'debug': True
    },

# TP WTP BLOCK
    {
        'name': 'PTT_express_TP_N2_WTP_BDM_CONT__0_end',
        'display_name': "Third Party, N=2, WTP, BDM Continuous [0, endowment] ",
        'real_world_currency_per_point': 1,
        'num_demo_participants': 3,
        'targetIncome': [10.3],
        'num_readers': 1,
        'reader_endowment': [11],  # to be extended to a list for when there is more than one readers
        'Params': [
{'treat': 'TP', 'val_typ': 'WTP','elic_met': 'BDM', 'BDM_typ': 'CONT', 'Met_par': [0, 'end'], 'end': [5, 3]},
        ],
        'app_sequence': ['zFake_searchTask','PTT_expression', 'payment_info'],
        'debug': True
    },
    {
        'name': 'PTT_express_TP_N2_WTP_BDM_LIST__0_av_inc',
        'display_name': "Third Party, N=2, WTP, BDM List [0, available_income] ",
        'real_world_currency_per_point': 1,
        'num_demo_participants': 3,
        'targetIncome': [10.3],
        'num_readers': 1,
        'reader_endowment': [11],  # to be extended to a list for when there is more than one readers
        'Params': [
{'treat': 'TP', 'val_typ': 'WTP', 'elic_met': 'BDM', 'BDM_typ': 'LIST', 'Met_par': [0, 'av_inc', 0.2], 'end': [4, 3]},
        ],
        'app_sequence': ['zFake_searchTask', 'PTT_expression', 'payment_info'],
        'debug': True
    },
    {
        'name': 'PTT_express_TP_N2_WTP_SOP',
        'display_name': "Third Party, N=2, WTP, SOP ",
        'real_world_currency_per_point': 1,
        'num_demo_participants': 3,
        'targetIncome': [10.3],
        'num_readers': 1,
        'reader_endowment': [11],  # to be extended to a list for when there is more than one readers
        'Params': [
{'treat': 'TP', 'val_typ': 'WTP', 'elic_met': 'SOP', 'BDM_typ': None, 'Met_par': [.98], 'end': [4, 3]},
        ],
        'app_sequence': ['zFake_searchTask', 'PTT_expression', 'payment_info'],
        'debug': True
    },
# TP WTA BLOCK
    {
        'name': 'PTT_express_TP_N2_WTA_BDM_CONT__0_end',
        'display_name': "Third Party, N=2, WTA, BDM Continuous [0, endowment] ",
        'real_world_currency_per_point': 1,
        'num_demo_participants': 3,
        'targetIncome': [10.3],
        'num_readers': 1,
        'reader_endowment': [11],  # to be extended to a list for when there is more than one readers
        'Params': [
{'treat': 'TP', 'val_typ': 'WTA','elic_met': 'BDM', 'BDM_typ': 'CONT', 'Met_par': [0, 'end'], 'end': [5, 3]},
        ],
        'app_sequence': ['zFake_searchTask','PTT_expression', 'payment_info'],
        'debug': True
    },
    {
        'name': 'PTT_express_TP_N2_WTA_BDM_LIST__0_av_inc',
        'display_name': "Third Party, N=2, WTA, BDM List [0, available_income] ",
        'real_world_currency_per_point': 1,
        'num_demo_participants': 3,
        'targetIncome': [10.3],
        'num_readers': 1,
        'reader_endowment': [11],  # to be extended to a list for when there is more than one readers
        'Params': [
{'treat': 'TP', 'val_typ': 'WTA', 'elic_met': 'BDM', 'BDM_typ': 'LIST', 'Met_par': [0, 'av_inc', 0.2], 'end': [4, 3]},
        ],
        'app_sequence': ['zFake_searchTask', 'PTT_expression', 'payment_info'],
        'debug': True
    },
    {
        'name': 'PTT_express_TP_N2_WTA_SOP',
        'display_name': "Third Party, N=2, WTA, SOP ",
        'real_world_currency_per_point': 1,
        'num_demo_participants': 3,
        'targetIncome': [10.3],
        'num_readers': 1,
        'reader_endowment': [11],  # to be extended to a list for when there is more than one readers
        'Params': [
{'treat': 'TP', 'val_typ': 'WTA', 'elic_met': 'SOP', 'BDM_typ': None, 'Met_par': [.98], 'end': [4, 3]},
        ],
        'app_sequence': ['zFake_searchTask', 'PTT_expression', 'payment_info'],
        'debug': True
    },
#############
    {
        'name': 'PTT_expression',
        'display_name': "PTT Expression",
        'real_world_currency_per_point': 1,
        'num_demo_participants': 11,
        'targetIncome': [4],
        'num_readers': 1,
        'reader_endowment': [45], # to be extended to a list for when there is more than one readers
        'Params': [
{'treat': 'DM', 'val_typ': 'WTP', 'elic_met': 'BDM', 'BDM_typ': 'CONT', 'Met_par':     [0, 'end'], 'end': [3, 4]},
{'treat': 'DM', 'val_typ': 'WTA', 'elic_met': 'BDM', 'BDM_typ': 'LIST', 'Met_par': [0, 'end', 0.25], 'end': [6, 3]}, # end or av_inc in Met_par[1] and step_size in Met_par[1]
{'treat': 'TP', 'val_typ': 'WTP', 'elic_met': 'SOP', 'BDM_typ':   None, 'Met_par':          [1.1], 'end': [1, 4]},
{'treat': 'NM', 'val_typ':  None, 'elic_met':  None, 'BDM_typ':   None, 'Met_par':           None, 'end': [3, 5]},
{'treat': 'FM', 'val_typ':  None, 'elic_met':  None, 'BDM_typ':   None, 'Met_par':           None, 'end': [2, 4]},
        ],
        'app_sequence': ['zFake_searchTask','PTT_expression', 'payment_info'],
        'debug': True
    },
    {
        'name': 'PTT_expression_13_paid',
        'display_name': "PTT Expression 14 subjects only paid treatments",
        'real_world_currency_per_point': 1,
        'num_demo_participants': 13,
        'targetIncome': [9],
        'num_readers': 1,
        'reader_endowment': [12],  # to be extended to a list for when there is more than one readers
        'Params': [
{'treat': 'DM', 'val_typ': 'WTA', 'elic_met': 'BDM', 'BDM_typ': 'CONT', 'Met_par': [0, 'end']           , 'end': [3, 4]},
{'treat': 'DM', 'val_typ': 'WTP', 'elic_met': 'SOP', 'BDM_typ':   None, 'Met_par': [0.9]                , 'end': [6, 3]},  # end or av_inc in Met_par[1] and step_size in Met_par[1]
{'treat': 'TP', 'val_typ': 'WTA', 'elic_met': 'BDM', 'BDM_typ': 'LIST', 'Met_par': [0, 'av_inc', 0.25]  , 'end': [2, 4]},
{'treat': 'DM', 'val_typ': 'WTP', 'elic_met': 'BDM', 'BDM_typ': 'CONT', 'Met_par': [0, 'av_inc']        , 'end': [3, 4]},
{'treat': 'DM', 'val_typ': 'WTA', 'elic_met': 'SOP', 'BDM_typ':   None, 'Met_par': [1.3]                , 'end': [6, 3]},
{'treat': 'TP', 'val_typ': 'WTP', 'elic_met': 'BDM', 'BDM_typ': 'LIST', 'Met_par': [0, 'end', 0.25]     , 'end': [2, 4]},
        ],
        'app_sequence': ['zFake_searchTask', 'PTT_expression', 'payment_info'],
        'debug': True
    },
    {
        'name': 'PTT_expression_BDM_CONT_WTP',
        'display_name': "PTT_expression_BDM_CONT_WTP",
        'real_world_currency_per_point': 1,
        'num_demo_participants': 2,
        'targetIncome': [10.5],
        'num_readers': 0,
        'reader_endowment': [7.5],  # to be extended to a list for when there is more than one readers
        'Params': [
            {'treat': 'DM', 'val_typ': 'WTP', 'elic_met': 'BDM', 'BDM_typ': 'CONT', 'Met_par': [0, 'av_inc'], 'end': [3, 4]},
        ],
        'app_sequence': ['zFake_searchTask', 'PTT_expression', 'payment_info'],
        'debug': True
    },
    {
        'name': 'PTT_expression_SOP_WTP',
        'display_name': "PTT_expression_SOP_WTP",
        'real_world_currency_per_point': 1,
        'num_demo_participants': 2,
        'targetIncome': [10.5],
        'num_readers': 0,
        'reader_endowment': [7.5],  # to be extended to a list for when there is more than one readers
        'Params': [
            {'treat': 'DM', 'val_typ': 'WTP', 'elic_met': 'SOP', 'BDM_typ': None, 'Met_par': [2.34],
             'end': [5, 4]},
        ],
        'app_sequence': ['zFake_searchTask', 'PTT_expression', 'payment_info'],
        'debug': True
    },
    {
        'name': 'PTT_expression_BDMLIST_WTP',
        'display_name': "PTT_expression_BDMLIST_WTP",
        'real_world_currency_per_point': 1,
        'num_demo_participants': 2,
        'targetIncome': [10.5],
        'num_readers': 0,
        'reader_endowment': [7.5],  # to be extended to a list for when there is more than one readers
        'Params': [
            {'treat': 'DM', 'val_typ': 'WTP', 'elic_met': 'BDM', 'BDM_typ': 'LIST', 'Met_par': [0, 'end', 0.1], 'end': [5, 4]},
        ],
        'app_sequence': ['zFake_searchTask', 'PTT_expression', 'payment_info'],
        'debug': True
    },
    {
        'name': 'PTT_expression_BDMLIST_WTA',
        'display_name': "PTT_expression_BDMLIST_WTA",
        'real_world_currency_per_point': 1,
        'num_demo_participants': 2,
        'targetIncome': [10.5],
        'num_readers': 0,
        'reader_endowment': [7.5],  # to be extended to a list for when there is more than one readers
        'Params': [
            {'treat': 'DM', 'val_typ': 'WTA', 'elic_met': 'BDM', 'BDM_typ': 'LIST', 'Met_par': [0, 'end', 0.2], 'end': [5, 4]},
        ],
        'app_sequence': ['zFake_searchTask', 'PTT_expression', 'payment_info'],
        'debug': True
    },
    {
        'name': 'PTT_expression_TP_DM',
        'display_name': "PTT_expression_TP_DM",
        'real_world_currency_per_point': 1,
        'num_demo_participants': 5,
        'targetIncome': [10.5],
        'num_readers': 1,
        'reader_endowment': [3],  # to be extended to a list for when there is more than one readers
        'Params': [
            {'treat': 'TP', 'val_typ': 'WTP', 'elic_met': 'BDM', 'BDM_typ': 'CONT', 'Met_par': [0, 'end'], 'end': [5, 4]},
            {'treat': 'DM', 'val_typ': 'WTP', 'elic_met': 'BDM', 'BDM_typ': 'CONT', 'Met_par': [0, 'end'], 'end': [3, 5]},
        ],
        'app_sequence': ['zFake_searchTask', 'PTT_expression', 'payment_info'],
        'debug': True
    },
    {
        'name': 'PTT_expression_2TP',
        'display_name': "PTT_expression_2TP",
        'real_world_currency_per_point': 1,
        'num_demo_participants': 5,
        'targetIncome': [10.5],
        'num_readers': 1,
        'reader_endowment': [3],  # to be extended to a list for when there is more than one readers
        'Params': [
            {'treat': 'TP', 'val_typ': 'WTP', 'elic_met': 'BDM', 'BDM_typ': 'CONT', 'Met_par': [0, 'end'],
             'end': [5, 4]},
            {'treat': 'TP', 'val_typ': 'WTP', 'elic_met': 'BDM', 'BDM_typ': 'CONT', 'Met_par': [0, 'end'],
             'end': [3, 5]},
        ],
        'app_sequence': ['zFake_searchTask', 'PTT_expression', 'payment_info'],
        'debug': True
    },

    {
        'name': 'PTT_expression_TP_BDMCONT_WTP',
        'display_name': "PTT_expression_TP_BDMCONT_WTP",
        'real_world_currency_per_point': 1,
        'num_demo_participants': 3,
        'targetIncome': [10.5],
        'num_readers': 1,
        'reader_endowment': [3],  # to be extended to a list for when there is more than one readers
        'Params': [
            {'treat': 'TP', 'val_typ': 'WTP', 'elic_met': 'BDM', 'BDM_typ': 'CONT', 'Met_par': [0, 'end'], 'end': [5, 4]},
        ],
        'app_sequence': ['zFake_searchTask', 'PTT_expression', 'payment_info'],
        'debug': True
    },
    # {
    #     'name': 'my_public_goods_',
    #     'display_name': "KLV Public Goods",
    #     'num_demo_participants': 3,
    #     'app_sequence': ['my_public_goods_', 'survey', 'payment_info'],
    # },
    # {
    #     'name': 'klv_trust_game',
    #     'display_name': "KLV Trust Game",
    #     'num_demo_participants': 2,
    #     'app_sequence': ['klv_trust_game', 'payment_info'],
    # },
    # {
    #     'name': 'klv_matching_pennies',
    #     'display_name': "KLV Matching Pennies",
    #     'num_demo_participants': 2,
    #     'app_sequence': ['klv_matching_pennies', 'payment_info'],
    # },
    # {
    #     'name': 'public_goods',
    #     'display_name': "Public Goods",
    #     'num_demo_participants': 3,
    #     'app_sequence': ['public_goods', 'payment_info'],
    # },
    # {
    #     'name': 'trust',
    #     'display_name': "Trust Game",
    #     'num_demo_participants': 2,
    #     'app_sequence': ['trust', 'payment_info'],
    # },
    # {
    #     'name': 'beauty',
    #     'display_name': "Beauty Contest",
    #     'num_demo_participants': 5,
    #     'num_bots': 5,
    #     'app_sequence': ['beauty', 'payment_info'],
    # },
    # {
    #     'name': 'survey',
    #     'display_name': "Survey",
    #     'num_demo_participants': 1,
    #     'app_sequence': ['survey', 'payment_info'],
    # },
    # {
    #     'name': 'prisoner',
    #     'display_name': "Prisoner's Dilemma",
    #     'num_demo_participants': 2,
    #     'app_sequence': ['prisoner', 'payment_info'],
    # },
    # {
    #     'name': 'ultimatum',
    #     'display_name': "Ultimatum (randomized: strategy vs. direct response)",
    #     'num_demo_participants': 2,
    #     'app_sequence': ['ultimatum', 'payment_info'],
    # },
    # {
    #     'name': 'ultimatum_strategy',
    #     'display_name': "Ultimatum (strategy method treatment)",
    #     'num_demo_participants': 2,
    #     'app_sequence': ['ultimatum', 'payment_info'],
    #     'treatment': 'strategy',
    # },
    # {
    #     'name': 'ultimatum_non_strategy',
    #     'display_name': "Ultimatum (direct response treatment)",
    #     'num_demo_participants': 2,
    #     'app_sequence': ['ultimatum', 'payment_info'],
    #     'treatment': 'direct_response',
    # },
    # {
    #     'name': 'battle_of_the_sexes',
    #     'display_name': "Battle of the Sexes",
    #     'num_demo_participants': 2,
    #     'app_sequence': [
    #         'battle_of_the_sexes', 'payment_info'
    #     ],
    # },
    # {
    #     'name': 'vickrey_auction',
    #     'display_name': "Vickrey Auction",
    #     'num_demo_participants': 3,
    #     'app_sequence': ['vickrey_auction', 'payment_info'],
    # },
    # {
    #     'name': 'volunteer_dilemma',
    #     'display_name': "Volunteer's Dilemma",
    #     'num_demo_participants': 3,
    #     'app_sequence': ['volunteer_dilemma', 'payment_info'],
    # },
    # {
    #     'name': 'cournot',
    #     'display_name': "Cournot Competition",
    #     'num_demo_participants': 2,
    #     'app_sequence': [
    #         'cournot', 'payment_info'
    #     ],
    # },
    # {
    #     'name': 'principal_agent',
    #     'display_name': "Principal Agent",
    #     'num_demo_participants': 2,
    #     'app_sequence': ['principal_agent', 'payment_info'],
    # },
    # {
    #     'name': 'dictator',
    #     'display_name': "Dictator Game",
    #     'num_demo_participants': 2,
    #     'app_sequence': ['dictator', 'payment_info'],
    # },
    # {
    #     'name': 'matching_pennies',
    #     'display_name': "Matching Pennies",
    #     'num_demo_participants': 2,
    #     'app_sequence': [
    #         'matching_pennies',
    #     ],
    # },
    # {
    #     'name': 'traveler_dilemma',
    #     'display_name': "Traveler's Dilemma",
    #     'num_demo_participants': 2,
    #     'app_sequence': ['traveler_dilemma', 'payment_info'],
    # },
    # {
    #     'name': 'bargaining',
    #     'display_name': "Bargaining Game",
    #     'num_demo_participants': 2,
    #     'app_sequence': ['bargaining', 'payment_info'],
    # },
    # {
    #     'name': 'common_value_auction',
    #     'display_name': "Common Value Auction",
    #     'num_demo_participants': 3,
    #     'app_sequence': ['common_value_auction', 'payment_info'],
    # },
    # {
    #     'name': 'stackelberg',
    #     'display_name': "Stackelberg Competition",
    #     'real_world_currency_per_point': 0.01,
    #     'num_demo_participants': 2,
    #     'app_sequence': [
    #         'stackelberg', 'payment_info'
    #     ],
    # },
    # {
    #     'name': 'bertrand',
    #     'display_name': "Bertrand Competition",
    #     'num_demo_participants': 2,
    #     'app_sequence': [
    #         'bertrand', 'payment_info'
    #     ],
    # },
    # {
    #     'name': 'real_effort',
    #     'display_name': "Real-effort transcription task",
    #     'num_demo_participants': 1,
    #     'app_sequence': [
    #         'real_effort',
    #     ],
    # },
    # {
    #     'name': 'lemon_market',
    #     'display_name': "Lemon Market Game",
    #     'num_demo_participants': 3,
    #     'app_sequence': [
    #         'lemon_market', 'payment_info'
    #     ],
    # },
    # {
    #     'name': 'public_goods_simple',
    #     'display_name': "Public Goods (simple version from tutorial)",
    #     'num_demo_participants': 3,
    #     'app_sequence': ['public_goods_simple', 'survey', 'payment_info'],
    # },
    #
    # {
    #     'name': 'trust_simple',
    #     'display_name': "Trust Game (simple version from tutorial)",
    #     'num_demo_participants': 2,
    #     'app_sequence': ['trust_simple'],
    # },

]

# anything you put after the below line will override
# oTree's default settings. Use with caution.
otree.settings.augment_settings(globals())
