from .select import Header, Profile

FILE_NAME = 'Select'
DEBUG = True


def run(self, data):
    print('Select.py')

    if data['location'][0] == 'header':
        Header.run(self, data)

    if data['location'][0] == 'profile':
        print('profile')
        Profile.run(self, data)


