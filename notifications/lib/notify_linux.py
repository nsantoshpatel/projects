import os, sys, time
print('Import Linux OS notifications modules: pynotify')
try:
    import pynotify
except ImportError as e:
    print('Import Error: {}'.format(e))
    exit(1)

class notify_linux(object):
    def __init__(self):
        print("{}::{}".format('notify_linux', '__init__'))

    def popup(self, title, msg, icon="red.ico", wait=None):
        print("{}::{}".format('notify_linux', 'popup'))

    def close(self):
        print("{}::{}".format('notify_linux', 'close'))

if __name__ == '__main__':
    print('Executing py file directly')
    notify = notify_linux()
    notify.popup('Header','Body of the PopUP', wait=10)
    notify.close()