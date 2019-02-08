import time
from collections import defaultdict
from datetime import date, timedelta

from .models import Run


def _ts(d):
    d = d - timedelta(days=d.weekday())
    return int(time.mktime(d.timetuple()) * 1000)


def _group_stats(stats):
    ret = []
    for k in sorted(stats.keys()):
        ret.append([k, stats[k]])
    return ret


def get_stats():
    stats = {
        'total': defaultdict(int),
        'runs': defaultdict(int),
        'new': defaultdict(int),
    }

    total = 0
    for run in Run.objects.filter(date__gte=date(2014, 1, 1)).order_by('date'):
        ts = _ts(run.date)
        total += 1

        stats['total'][ts] = total
        stats['runs'][ts] += 1
        if run.first_run_by_player:
            stats['new'][ts] += 1

    return {
        'total': _group_stats(stats['total']),
        'runs': _group_stats(stats['runs']),
        'new': _group_stats(stats['new']),
    }
