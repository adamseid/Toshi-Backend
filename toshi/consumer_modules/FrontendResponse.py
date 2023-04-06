from . import Misc


FILE_NAME = 'FrontendResponse'
DEBUG = True


def run(self, event):
    FUNCTION_NAME = 'run'
    Misc.printDebug(FILE_NAME, FUNCTION_NAME, 'STARTED', DEBUG)

    self.send(text_data=event['data'])
    Misc.printDebug(FILE_NAME, FUNCTION_NAME, 'FINISHED', DEBUG)
