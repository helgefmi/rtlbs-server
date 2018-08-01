import json
from collections import defaultdict

from django.core.management.base import BaseCommand

from server.apps.rooms.models import Segment, Room


class Command(BaseCommand):
    help = 'Outputs fixtures.js needed for the client'

    def handle(self, *args, **options):
        segments = []
        segments_by_slug = {}
        for segment in Segment.objects.all():
            segment_data = {
                'slug': segment.slug,
                'name': segment.name,
            }
            segments_by_slug[segment.slug] = segment_data
            segments.append(segment_data)

        rooms = []
        rooms_by_slug = {}
        rooms_by_segments = defaultdict(list)
        for room in Room.objects.all():
            room_data = {
                'slug': room.slug,
                'name': room.name,
                'segment': segments_by_slug[room.segment.slug],
            }
            rooms.append(room_data)
            rooms_by_slug[room.slug] = room_data
            rooms_by_segments[room.segment.slug].append(room_data)

        output = ''
        output += 'export const segments = ' + json.dumps(segments) + '\n'
        output += 'export const segmentsBySlug = ' + json.dumps(segments_by_slug) + '\n'
        output += 'export const rooms = ' + json.dumps(rooms) + '\n'
        output += 'export const roomsBySlug = ' + json.dumps(rooms_by_slug) + '\n'
        output += 'export const roomsBySegment = ' + json.dumps(rooms_by_segments)

        print(output.replace("'", "\\'").replace('"', "'"))
