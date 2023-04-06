from ..models import ProfileConnections


FILE_NAME = 'Connect'
DEBUG = True


def run(self):
    FUNCTION_NAME = 'run'

    room_group_name = self.room_group_name
    print(room_group_name)
    oc = ProfileConnections(
        roomGroupName=room_group_name, timeFrame="1H")
    oc.save()
