from .profile_receive import Select

FILE_NAME = 'ProfileReceive'
DEBUG = True


def run(self, data):
    print('ProfileReceive.py')

    if data['request'] == 'select':
        print('select')
        Select.run(self, data)

    

