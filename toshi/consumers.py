import json
from asgiref.sync import async_to_sync


from channels.generic.websocket import WebsocketConsumer
from .consumer_modules import Receive, Disconnect, FrontendResponse, Connect
from .frontend_profile import ProfileConnect, ProfileDisconnect, ProfileReceive, ProfileFrontendResponse
from .consumer_history_modules import ConsumerHistoryReceive, ConsumerHistoryDisconnect

class HistoryConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        self.room_name = self.scope['client'][0] + '-' + str(self.scope['client'][1])
        self.room_group_name = "frontend_%s" % self.room_name

    def receive(self, text_data):
        print('WebSocket.receive(): STARTED')
        text_data = json.loads(text_data)
        ConsumerHistoryReceive.run(self,text_data)
        print('WebSocket.receive(): ENDED')


    def disconnect(self, close_code):
        print('History.disconnect(): STARTED')
        ConsumerHistoryDisconnect.run(self)
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )
        print('History.disconnect(): FINISHED')

class FrontendConsumer(WebsocketConsumer):

    def connect(self):
        print('FontendConsumer.connect(): STARTED')
        self.room_name = self.scope['client'][0] + \
            '-' + str(self.scope['client'][1])
        self.room_group_name = "frontend_%s" % self.room_name
        print('CONNECT')
        print(self.room_name, self.room_group_name)

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )
        Connect.run(self)
        self.accept()

        print('FontendConsumer.connect(): FINISHED')

    def disconnect(self, close_code):
        print('FontendConsumer.disconnect(): STARTED')

        print(self.room_name, self.room_group_name)

        Disconnect.run(self)
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )
        print('FontendConsumer.disconnect(): FINISHED')

    def receive(self, text_data):
        print('FontendConsumer.receive(): STARTED')
        text_data = json.loads(text_data)
        Receive.run(self, text_data)

    def frontend_response(self, event):
        print('FrontendConsumer.frontend_response(): STARTED')
        FrontendResponse.run(self, event)
        print('FrontendConsumer.frontend_response(): FINISHED')


class FrontendProfileConsumer(WebsocketConsumer):

    def connect(self):
        print('FrontendProfileConsumer.connect(): STARTED')
        self.room_name = self.scope['client'][0] + \
            '-' + str(self.scope['client'][1])
        self.room_group_name = "frontend_%s" % self.room_name
        print('CONNECT')
        print(self.room_name, self.room_group_name)

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )
        self.accept()

        ProfileConnect.run(self)

        print('FrontendProfileConsumer.connect(): FINISHED')

    def disconnect(self, close_code):
        print('FrontendProfileConsumer.disconnect(): STARTED')

        print(self.room_name, self.room_group_name)

        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )
        ProfileDisconnect.run(self)
        print('FrontendProfileConsumer.disconnect(): FINISHED')

    def receive(self, text_data):
        print('FrontendProfileConsumer.receive(): STARTED')
        text_data = json.loads(text_data)
        ProfileReceive.run(self, text_data)

    def profilefrontend_response(self, event):
        print('FrontendProfileConsumer.frontend_response(): STARTED')
        ProfileFrontendResponse.run(self, event)
        print('FrontendProfileConsumer.frontend_response(): FINISHED')





