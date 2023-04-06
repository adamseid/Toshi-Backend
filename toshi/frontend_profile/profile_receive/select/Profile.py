from ....models import ProfileConnections

def run(self, data):
    print('Profile.py')
    # ProfileConnections.objects.filter(roomGroupName=self.room_group_name).update(timeFrame = data['time_frame'])
    ProfileConnections.objects.all().update(timeFrame=data['time_frame'])


