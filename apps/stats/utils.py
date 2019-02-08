import time
from collections import defaultdict
from datetime import date, timedelta

from .models import Run, Category


def _ts(d):
    d = d - timedelta(days=d.weekday())
    return int(time.mktime(d.timetuple()) * 1000)


def _group_stats(stats):
    ret = []
    for k in sorted(stats.keys()):
        ret.append([k, stats[k]])
    return ret


def _pb_stats(data):
    ret = []
    all_pbs = list(sorted(set(pb for pb_data in data.values() for pb in pb_data.keys())))
    for year, pb_data in sorted(data.items()):
        for pb, players in sorted(pb_data.items()):
            data[year][pb] = len(players)

        pb_data = [year]
        for pb in all_pbs:
            pb_data.append(data[year][pb] or 0)
        ret.append(pb_data)

    return {
        'data': ret,
        'pbs': all_pbs,
    }


def get_nmg_stats():
    nmg = Category.objects.get(id='013xwzr1')

    qs = Run.objects.order_by('date')
    qs = qs.filter(status='verified', date__gte=date(2014, 1, 1), category=nmg)

    current_pb = {}
    pbs_by_year = defaultdict(lambda: defaultdict(set))

    for run in qs:
        new_pb = int('%d%02d' % (int(run.time / 60 / 60), int(run.time / 60 % 60)))
        if new_pb < 130 and current_pb.get(run.player_id, 130) != new_pb:
            for x in range(new_pb, 130):
                pbs_by_year[run.date.year][x].add(run.player_id)
        current_pb[run.player_id] = new_pb

    return _pb_stats(pbs_by_year)


def get_stats(category_id):
    stats = {
        'total': defaultdict(int),
        'runs': defaultdict(int),
        'new': defaultdict(int),
    }

    qs = Run.objects.order_by('date')
    qs = qs.filter(status='verified', date__gte=date(2014, 1, 1))
    if category_id != 'all':
        qs = qs.filter(category_id=category_id)

    total = 0
    added_players = set()
    added_ts = set()

    for run in qs:
        ts = _ts(run.date)
        added_ts.add(ts)
        total += 1

        stats['total'][ts] = total
        stats['runs'][ts] += 1

        if run.player_id not in added_players:
            stats['new'][ts] += 1
            added_players.add(run.player_id)

    for stat in stats.values():
        for ts in added_ts:
            stat[ts] = stat[ts] or 0

    return {
        'pbStats': get_nmg_stats(),
        'total': _group_stats(stats['total']),
        'runs': _group_stats(stats['runs']),
        'new': _group_stats(stats['new']),
    }
