#!/usr/bin/env python3
from django.core.management.base import BaseCommand

from server.apps.stats.models import Run


class Command(BaseCommand):
    help = 'Set `Run.first_run_by_player` based on the database'

    def handle(self, *args, **options):
        print('Updating everything to False')
        Run.objects.filter(first_run_by_player=True).update(first_run_by_player=False)

        submitted_players = set()
        for run in Run.objects.order_by('date'):
            if run.player_id in submitted_players:
                continue
            print(run.player_id, run.date)
            run.first_run_by_player = True
            run.save()
            submitted_players.add(run.player_id)
