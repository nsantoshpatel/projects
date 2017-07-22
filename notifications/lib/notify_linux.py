import time
print('Import Linux OS notifications modules: pynotify')
try:
    import pynotify
except ImportError as e:
    print('Import Error: {}'.format(e))
    exit(1)

class notify_linux(object):
    def __init__(self):
        print("{}::{}".format('notify_linux', '__init__'))
        if not pynotify.is_initted():
            print("{}::{}::{}".format('notify_linux', '__init__', 'Initiating pynotify'))
            if not pynotify.init('PythonTaskbar'):
                print("{}::{}::{}".format('notify_linux', '__init__', 'Initiating pynotify Failed'))
                exit(1)
        self.open_notify_obj = []

    def popup(self, title, msg, icon="/usr/share/pixmaps/xterm-color_48x48.xpm", wait=None):
        print("{}::{}".format('notify_linux', 'popup'))
        n = pynotify.Notification(title, msg, icon)
        if wait is None:
            print("{}::{}::{}".format('notify_linux', 'popup', 'Timeout=0'))
            n.set_timeout(0)
        else:
            print("{}::{}::{}{}".format('notify_linux', 'popup', 'Timeout=', wait))
            n.set_timeout(wait*1000)
        print("{}::{}::{}".format('notify_linux', 'popup', 'Show Notification'))
        if not n.show():
            print("{}::{}::{}".format('notify_linux', 'popup', 'Show Notification Failed'))
            exit(1)
        try: time.sleep(wait)
        except: pass
        self.open_notify_obj.append(n)
        return n

    def close(self, notify_obj=None):
        print("{}::{}".format('notify_linux', 'close'))
        if notify_obj is None:
            print("{}::{}::{}".format('notify_linux', 'close', 'Closing All Popups'))
            for i in self.open_notify_obj:
                i.close()
                self.open_notify_obj.remove(i)
        else:
            print("{}::{}::{}".format('notify_linux', 'close', 'Closing a Popup'))
            notify_obj.close()
            self.open_notify_obj.remove(notify_obj)


if __name__ == '__main__':
    print('Executing py file directly')
    notify = notify_linux()
    r = notify.popup('Header','Body of the PopUP', icon='/usr/share/pixmaps/firefox.png', wait=10)
    # r1 = notify.popup('Header','Body of the PopUP...............')
    notify.close(r)
