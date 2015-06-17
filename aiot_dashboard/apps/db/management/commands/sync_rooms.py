import requests
import random
import json
import sys

from django.core.management.base import BaseCommand
from django.conf import settings

from aiot_dashboard.apps.db.models import Room, RoomType

class Command(BaseCommand):
    help = 'Contact the bimsync API and pull a list of rooms'

    def _get_spaces_in_revision(self, model_id, revision_id, page_id=1, per_page=1000):
        r = requests.get('https://api.bimsync.com/1.0/revision/products?model_id=%s&revision_id=%s&page=%s&per_page=%s' % (model_id, revision_id, page_id, per_page),
                         headers={'Authorization': settings.BIMSYNC_API_AUTH_HEADER,
                                  'Accept': 'application/json',
                                  'Content-Type': 'application/x-www-form-urlencode'},
                         data={"type": ["IfcSpace"]})
        if r.status_code == 200:
            return r.json()
        raise Exception('API request returned %s' % r.status_code)

    def _get_room_details(self, obj):
        r = requests.post('https://api.bimsync.com/ifc/products',
                          headers={'Authorization': settings.BIMSYNC_API_AUTH_HEADER,
                                   'Content-Type': 'application/json'},
                          data=json.dumps({"products": [int(obj.key)],
                                           "format": "FLAT"
                                           }))
        if r.status_code == 200:
            return r.json()
        raise Exception('API request returned %s' % r.status_code)

    def _get_attribute_by_path(self, data, path):
        for rec in data:
            if '/'.join(rec['path']) == path:
                return rec['value']
        return None

    def _get_room_type(self, value):
        try:
            return RoomType.objects.get(description=value)
        except RoomType.DoesNotExist:
            rt = RoomType(description=value)
            rt.save()
            return rt

    def _create_room(self, data):
        obj, _ = Room.objects.get_or_create(key=data['objectId'])
        obj.name = data['name']
        obj.area = random.randrange(5.0, 50.0)

        details = self._get_room_details(obj)[0]
        obj.floor = self._get_attribute_by_path(details['attributes'], 'ElevationWithFlooring')
        longname = self._get_attribute_by_path(details['attributes'], 'LongName')
        capacity = self._get_attribute_by_path(details['propertySets'], 'Pset_SpaceOccupancyRequirements/OccupancyNumber')

        if longname:
            if not capacity:
                capacity = random.randint(4, 18)
            obj.room_type = self._get_room_type(longname)

        obj.manminutes_capacity = capacity

        obj.save()
        return obj

    def handle(self, *args, **options):
        more = True
        page = 1
        room_count = 0
        while more:
            res = self._get_spaces_in_revision(settings.BIMSYNC_MODEL_ID,
                                               settings.BIMSYNC_MODEL_REVISION,
                                               page_id=page)

            for o in res:
                if o['type'] == 'IfcSpace':
                    self._create_room(o)
                    room_count += 1

            page += 1
            if len(res) < 1000:
                more = False

        print "Created / updated %d rooms" % (room_count)
