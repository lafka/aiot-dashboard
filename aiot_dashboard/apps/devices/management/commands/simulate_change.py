import random
import uuid

from django.core.management.base import BaseCommand
from django.utils import timezone

from aiot_dashboard.apps.devices.models import Room, RoomState

class Command(BaseCommand):
    help = 'Adds a simulated random room update'

    def _get_random_room(self):
        qs = Room.objects.all()
        return qs[random.randrange(0, qs.count())]

    def handle(self, *args, **options):
        room = self._get_random_room()

        print "Toggling movement for room %s" % (room.key)

        movement = random.randrange(0, 2) == 1
        # See if there's a previous roomstate
        rs = RoomState.objects.filter(room=room).first()
        if not rs:
            rs = RoomState(room=room, guid=uuid.uuid4())
        else:
            movement = not rs.s_movement

        rs.s_movement = movement
        rs.datetime = timezone.now()

        print " .. setting movement to %s" % (movement)

        rs.save()
