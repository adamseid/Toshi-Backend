DEBUG = True


def printDebug(object_name, function_name, status, debug):
    if DEBUG:
        if debug:
            print(object_name + '.' + function_name + '(): ' + status)
        else:
            pass
    else:
        pass