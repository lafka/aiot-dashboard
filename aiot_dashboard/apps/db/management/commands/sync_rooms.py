import requests
import random

from django.core.management.base import BaseCommand
from django.conf import settings

from aiot_dashboard.apps.db.models import Room, Device, MapDeviceRoom, RoomType

class Command(BaseCommand):
    help = 'Contact the bimsync API and pull a list of rooms'

    def _get_spaces_in_revision(self, model_id, revision_id, page_id=1, per_page=1000):
        r = requests.get('https://api.bimsync.com/1.0/revision/products?model_id=%s&revision_id=%s&page=%s&per_page=%s' % (model_id, revision_id, page_id, per_page),
                          headers={'Authorization': settings.BIMSYNC_API_AUTH_HEADER,
                                   'Accept': 'application/json',
                                   'Content-Type': 'application/x-www-form-urlencode'})
        if r.status_code == 200:
            return r.json()
        raise Exception('API request returned %s' % r.status_code)

    def _create_object(self, cls, data):
        obj, _ = cls.objects.get_or_create(key=data['objectId'])
        obj.name = data['name']
        obj.type = RoomType.objects.order_by('?').first()
        obj.save()
        return obj

    def _create_random_room_types(self):
        while RoomType.objects.all().count() < 10:
            RoomType(description="Random room type %d" % RoomType.objects.all().count(),
                     manminutes_capacity=random.randint(5, 100)).save()

    def handle(self, *args, **options):
        self._create_random_room_types()

        more = True
        page = 1
        room_count = 0
        while more:
            res = self._get_spaces_in_revision(settings.BIMSYNC_MODEL_ID,
                                               settings.BIMSYNC_MODEL_REVISION,
                                               page_id=page)

            for o in res:
                if o['type'] == 'IfcSpace':
                    self._create_object(Room, o)
                    room_count += 1

            page += 1
            if len(res) < 1000:
                more = False

        print "Created / updated %d rooms" % (room_count)
