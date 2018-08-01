import random

from django.core.management.base import BaseCommand, CommandError

from django_seed import Seed

from server.apps.players.models import Player
from server.apps.rooms.models import Room, RoomTime


def random_frames(x):
    return random.randint(0, 20) + (random.randint(0, 60) / 100)


class Command(BaseCommand):
    help = 'Automatically populates the database with random data'

    def add_arguments(self, parser):
        parser.add_argument(
            '--qty',
            type=int,
            default=10
        )

    def handle(self, *args, **options):
        seeder = Seed.seeder()

        num_players = Player.objects.count()
        if num_players < 20:
            print('Adding', 20 - num_players, 'players..')
            seeder.add_entity(Player, 20 - num_players)

        qty = options.get('qty', 10)
        print('Adding', qty, 'room times..')

        seeder.add_entity(RoomTime, qty, {
            'player': lambda x: Player.objects.order_by('?')[0],
            'room': lambda x: Room.objects.order_by('?')[0],
            'frames': random_frames,
            'idle': random_frames,
            'menues': random_frames,
        })

        seeder.execute()
