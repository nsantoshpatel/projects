import os
import sys
import time
print('Import Windows OS notifications modules: win32gui, win32api, win32con')
try:
    from win32api import *
    from win32gui import *
    import win32con, winerror
    from win32gui import error as win_error
except ImportError as e:
    print('Import Error: {}'.format(e))
    exit(1)

class notify_windows(object):
    def __init__(self):
        print("{}::{}".format('notify_windows', '__init__'))
        self.message_map = {
            win32con.WM_DESTROY: self.OnDestroy,
        }
        self.hinst = ''
        self.classAtom = ''
        # Register the Window class.
        wc = WNDCLASS()
        self.hinst = wc.hInstance = GetModuleHandle(None)
        wc.lpszClassName = "PythonTaskbar"
        wc.lpfnWndProc = self.message_map  # could also specify a wndproc.
        self.classAtom = RegisterClass(wc)
        print("{}::{}::{}".format('notify_windows', '__init__', 'Registered Window class'))

    def popup(self, title, msg, icon="red.ico", wait=None):
        print("{}::{}".format('notify_windows', 'popup'))
        # Create the Window.
        style = win32con.WS_OVERLAPPED
        self.hwnd = CreateWindow( self.classAtom, "Taskbar", style, \
                0, 0, win32con.CW_USEDEFAULT, win32con.CW_USEDEFAULT, \
                0, 0, self.hinst, None)
        UpdateWindow(self.hwnd)
        print("{}::{}::{}".format('notify_windows', 'popup', 'Created the Window'))
        iconPathName = os.path.abspath(os.path.join(sys.path[0], icon))
        icon_flags = win32con.LR_LOADFROMFILE | win32con.LR_DEFAULTSIZE
        try:
            hicon = LoadImage(self.hinst, iconPathName, win32con.IMAGE_ICON, 0, 0, icon_flags)
            print("{}::{}::{}".format('notify_windows', 'popup', 'Loaded the Icon Image'))
        except:
            hicon = LoadIcon(0, win32con.IDI_APPLICATION)
            print("{}::{}::{}".format('notify_windows', 'popup', 'Icon Image Not Found. Default Loaded'))
        flags = NIF_ICON | NIF_MESSAGE | NIF_TIP
        nid = (self.hwnd, 0, flags, win32con.WM_USER+20, hicon, "tooltip")
        Shell_NotifyIcon(NIM_ADD, nid)
        Shell_NotifyIcon(NIM_MODIFY, \
                         (self.hwnd, 0, NIF_INFO, win32con.WM_USER+20,\
                          hicon, "Balloon  tooltip",msg,200,title))
        if wait is None:
            time.sleep(2)
        else:
            time.sleep(wait)
            self.close()
        return None

    def close(self):
        # while True:
            try:
                print("{}::{}".format('notify_windows', 'close'))
                DestroyWindow(self.hwnd)
                self.classAtom = UnregisterClass(self.classAtom, self.hinst)
            except win_error as err_info:
                print("{}::{}::{}".format('notify_windows', 'close', 'window handle already opened. Wait'))
                if err_info.winerror != winerror.ERROR_CLASS_ALREADY_EXISTS:
                    print err_info.winerror


    def OnDestroy(self, hwnd, msg, wparam, lparam):
        print("{}::{}".format('notify_windows', 'OnDestroy'))
        nid = (self.hwnd, 0)
        Shell_NotifyIcon(NIM_DELETE, nid)
        PostQuitMessage(0) # Terminate the app.

if __name__ == '__main__':
    print('Executing py file directly')
    notify = notify_windows()
    notify.popup('Header','Body of the PopUP')
    # time.sleep(2)
    notify.popup('Header11111','Body of the PopUP111111111')
    # notify.   close()
    notify.close()
