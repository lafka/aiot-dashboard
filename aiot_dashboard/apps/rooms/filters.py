from aiot_dashboard.apps.db.models import Room, RoomType

from django.shortcuts import get_object_or_404

def get_filter_context(request):
    active_rooms = Room.get_active_rooms()
    num_active_rooms = active_rooms.count()

    available_room_types = RoomType.objects.filter(rooms__in=active_rooms).distinct()

    filter_room_type = request.GET.get('room_type', 'all')
    if filter_room_type == 'all':
        rooms = active_rooms
    else:
        filter_room_type = int(filter_room_type)
        room_type = get_object_or_404(available_room_types, pk=filter_room_type)
        rooms = active_rooms.filter(room_type=room_type)

    return {
        'room_type': filter_room_type,
        'available_room_types': available_room_types,
        'rooms': rooms,
        'num_active_rooms': num_active_rooms,
    }
