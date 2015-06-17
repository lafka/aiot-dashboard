import requests

from django.core.management.base import BaseCommand
from django.conf import settings

class Command(BaseCommand):
    help = 'Creates a new viewer token (but you should probably reuse an old one, if it still works :)'

    def _get_viewer_token_response(self):
        headers = {
            'Authorization': settings.BIMSYNC_API_AUTH_HEADER,
        }
        # TODO: I get 404 when passing in this. But it's OK since it will create from newest revision anyway.
        #       Needs to be fixed if we want a different revision, though.
        # body = [{'model_id': settings.BIMSYNC_MODEL_ID, 'revision_id': settings.BIMSYNC_MODEL_REVISION}]
        r = requests.post('https://api.bimsync.com/1.0/viewer/access?project_id=%s' % settings.BIMSYNC_PROJECT_ID, headers=headers)
        if r.status_code == 200:
            return r.json()
        raise Exception('API request returned %s (%s)' % (r.status_code, repr(r.text)))

    def handle(self, *args, **options):
        token_response = self._get_viewer_token_response()
        print token_response
