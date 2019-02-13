import time
from collections import defaultdict
from datetime import date, timedelta

from django.db.models import Count, Min

from .models import Run, Category


def _ts(d):
    d = d.replace(day=1)
    return int(time.mktime(d.timetuple()) * 1000)


def _process_run_stats(stats):
    ret = []
    for k in sorted(stats.keys()):
        ret.append([k, stats[k]])
    return ret


def _process_nmg_stats(data):
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

    qs = Run.objects.filter(status='verified', date__gte=date(2014, 1, 1), category=nmg)

    current_pb = {}
    pbs_by_year = defaultdict(lambda: defaultdict(set))

    for run in qs:
        new_pb = int('%d%02d' % (int(run.time / 60 / 60), int(run.time / 60 % 60)))
        if new_pb < 130 and current_pb.get(run.player_id, 130) != new_pb:
            for x in range(new_pb, 130):
                pbs_by_year[run.date.year][x].add(run.player_id)
        current_pb[run.player_id] = new_pb

    return _process_nmg_stats(pbs_by_year)


def get_run_stats(category_id):
    stats = {
        'total': defaultdict(int),
        'runs': defaultdict(int),
        'new': defaultdict(int),
    }

    qs = Run.objects.filter(status='verified', date__gte=date(2014, 1, 1))
    if category_id != 'all':
        qs = qs.filter(category_id=category_id)

    total = 0
    added_players = set()
    added_ts = set()

    min_rundate = date.today()
    max_rundate = date(2000, 1, 1)

    for run in qs:
        max_rundate = max(max_rundate, run.date)
        min_rundate = min(min_rundate, run.date)

        ts = _ts(run.date)
        added_ts.add(ts)
        total += 1

        stats['total'][ts] = total
        stats['runs'][ts] += 1

        if run.player_id not in added_players:
            stats['new'][ts] += 1
            added_players.add(run.player_id)

    # Add in missing 0's
    d = min_rundate.replace(day=1)
    last_d = max_rundate.replace(day=1)
    while d < last_d:
        ts = _ts(d)
        stats['new'][ts] = stats['new'][ts] or 0
        stats['runs'][ts] = stats['runs'][ts] or 0
        d = (d + timedelta(days=33)).replace(day=1)

    return {
        'total': _process_run_stats(stats['total']),
        'runs': _process_run_stats(stats['runs']),
        'new': _process_run_stats(stats['new']),
    }


def _order_by_max(d):
    return sorted(d.items(), key=lambda x: x[1], reverse=True)[:10]


def get_table_stats():
    stats = {
        'pbs': defaultdict(int),
        'country': defaultdict(int),
        'categories': defaultdict(set),
    }
    all_players = {}

    qs = Run.objects.filter(status='verified', date__gte=date(2014, 1, 1)).select_related('player')
    for run in qs:
        all_players[run.player_id] = run.player

        stats['pbs'][run.player_id] += 1
        stats['country'][run.player.location] += 1
        stats['categories'][run.player_id].add(run.category_id)

    for player_id in stats['categories']:
        stats['categories'][player_id] = len(stats['categories'][player_id])

    ret = {
        'pbs': [],
        'country': [],
        'categories': [],
        'moderators': [],
    }
    for player_id, num_pbs in _order_by_max(stats['pbs']):
        ret['pbs'].append({
            'key': all_players[player_id].name,
            'value': num_pbs,
        })
    for country, num_pbs in _order_by_max(stats['country']):
        ret['country'].append({
            'key': country or '(Not set)',
            'value': num_pbs,
        })
    for player_id, num_categories in _order_by_max(stats['categories']):
        ret['categories'].append({
            'key': all_players[player_id].name,
            'value': num_categories,
        })
    for data in Run.objects.values('moderator__name').annotate(Count('id')).order_by('-id__count')[:10]:
        ret['moderators'].append({
            'key': data['moderator__name'],
            'value': data['id__count'],
        })

    return ret


def get_stats(category_id):
    return {
        'nmg': get_nmg_stats(),
        'run': get_run_stats(category_id),
        'table': get_table_stats(),
    }


def parse_time(t):
    h = int(t / 60 / 60)
    m = int(t / 60 % 60)
    s = int(t % 60)
    return '%d:%02d:%02d' % (h, m, s)


def get_leaderboards(category_id, lbs_date):
    qs = Run.objects.filter(date__lte=lbs_date, status='verified', category=category_id)
    qs = qs.values('player__name').annotate(best=Min('time')).order_by('best')
    ret = []
    for data in qs:
        ret.append({
            'player': data['player__name'],
            'time': parse_time(data['best'])
        })
    return ret
