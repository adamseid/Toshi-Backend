import os
from ....models import ProfileConnections


def run(self, data):
    walletAddress = data['time_frame']
    if(walletAddress != ""):
        if not ProfileConnections.objects.filter(roomGroupName=self.room_group_name).exists():
            pc = ProfileConnections(roomGroupName = self.room_group_name, walletID = walletAddress )
            pc.save()
        else:
            ProfileConnections.objects.filter(roomGroupName=self.room_group_name).update(walletID = walletAddress)
    print('Header.py')