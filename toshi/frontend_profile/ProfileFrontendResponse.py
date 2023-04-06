

def run(self, event):
    print('ProfileFrontendResponse.py')
    print(event['data'])
    self.send(text_data=event['data'])
