from ..models import ProfileConnections
import pandas as pd

FILE_NAME = 'Disconnect'
DEBUG = True
STATE_CSV_PATH = './toshi/state/top_performer.csv'



def run(self):
    ProfileConnections.objects.filter(
        roomGroupName=self.room_group_name).delete()
