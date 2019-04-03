#!/usr/bin/env python3
import dateutil.parser
import csv

from django.core.management.base import BaseCommand

from server.apps.stats.models import Run, Player, Category


CATEGORY_MAP = {
    '100%': Category.objects.get(id='rqvx6jrl'),
    'All Dungeons': Category.objects.get(id='xqko9pd1'),
    'Any%': Category.objects.get(id='p129ogdl'),
    'No Exploration Glitch': Category.objects.get(id='81pe4rvl'),
    'No Major Glitches': Category.objects.get(id='013xwzr1'),
    'No Out of Bounds': Category.objects.get(id='z1958jyq'),
}


PLAYER_MAP = {
    'Albrecht84': 'Verniy',
    'Bob_Loblaw_Law': 'Bob',
    'Danshow': 'Danshow1',
    'DireVVolf': 'Dire_vVolf',
    'Elminster': 'azder',
    'Falco Eagle': 'FalcoEagle',
    'Fenrir227': 'fenrirplayz',
    'Haunter': 'Ms_Haunter',
    'Ineb_tfm': 'Andy',
    'ItsTenchy': 'Tenchy',
    'JSR2gamers': 'JSR_',
    'MrCab': 'mrcab55',
    'Official Fern': 'OfficialFern',
    'PrincessViviana': 'Viviana',
    'RRHAN 1JZ': 'RRHAN',
    'Released': 'JoshRTA',
    'SP Chocobo': 'SP_Chocobo',
    'Sandsky0': 'sandskyzero',
    'SpaceCowX12345': 'SpaceCowX',
    'SpaceCowX33': 'SpaceCowX',
    'TortoiseGamer': 'TortoiseGaming',
    'VforExtreme': 'VforExtreme12',
    'andrew': 'andreww',
    'chanchacorin': 'barnowl',
    'saiboT': 'saibot__',
    'timmon_': 'timmon',
    'まーおり(orima_r)': 'orima_r',
}


def parse_date(s):
    return dateutil.parser.parse(s).date()


class Command(BaseCommand):
    help = 'Import runs from ZSR export'
    path = None

    def add_arguments(self, parser):
        parser.add_argument('--path', action='store',
                            dest='path')

    def handle(self, **options):
        self.path = options['path']
        with open(options['path'], 'r') as f:
            reader = csv.reader(f, delimiter=';')
            lines = list(reader)
        lines.pop(0)

        keys = ['category', 'player', 'time', '_', 'date', 'vod', 'comment']
        for line in lines:
            run_data = dict(zip(keys, line))
            self.import_run(run_data)

    def import_run(self, data):
        data['category'] = CATEGORY_MAP[data['category']]
        data['player'] = self.find_player(data)
        data['date'] = parse_date(data['date'])

        run = Run.objects.filter(player=data['player'], time=data['time'], category=data['category']).first()
        if run is not None:
            print('duplicate run', run)
            return

        id = 'zsr-{}-{}'.format(data['player'].name, data['time'])

        run = Run.objects.create(id=id, link=data['vod'], category=data['category'], comment=data['comment'],
                                 status='verified', time=data['time'], player=data['player'], date=data['date'])
        print('created run', run)

    def find_player(self, run):
        player_name = PLAYER_MAP.get(run['player'], run['player'])

        player = Player.objects.filter(name__iexact=player_name).first()
        if player is None:
            id = 'zsr-{}'.format(player_name)
            player = Player.objects.create(id=id, name=player_name)

        return player
