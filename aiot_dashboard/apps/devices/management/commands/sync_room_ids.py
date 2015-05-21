import requests

from django.core.management.base import BaseCommand
from django.conf import settings

from aiot_dashboard.apps.devices.models import Room

class Command(BaseCommand):
    help = 'Contact the bimsync API and pull a list of room IDs'

    def _get_spaces_in_revision(self, model_id, revision_id, page_id=1, per_page=1000):
        r = requests.get('https://api.bimsync.com/1.0/revision/products?model_id=%s&revision_id=%s&page=%s&per_page=%s' % (model_id, revision_id, page_id, per_page),
                          headers={'Authorization': settings.BIMSYNC_API_AUTH_HEADER,
                                   'Accept': 'application/json',
                                   'Content-Type': 'application/x-www-form-urlencode'})
        if r.status_code == 200:
            return r.json()
        print r.text
        raise Exception('API request returned %s' % r.status_code)

    def handle(self, *args, **options):
        more = True
        page = 1
        count = 0
        while more:
            res = self._get_spaces_in_revision(settings.BIMSYNC_MODEL_ID,
                                               settings.BIMSYNC_MODEL_REVISION,
                                               page_id=page)

            for o in res:
                room, _ = Room.objects.get_or_create(key=o['objectId'])
                room.name = o['name']
                room.save()
                count += 1

            page += 1
            if len(res) < 1000:
                more = False

        print "Created / updated %d rooms" % (count)
