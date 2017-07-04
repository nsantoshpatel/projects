import os
if os.name == 'nt':
    print('Create Windows notification py object')
    from notify_windows import notify_windows as notify

elif os.name == 'posix':
    print('Create Linux notification py object')
    from notify_linux import notify_linux as notify

else:
    print('Unsupported Operating System found: '+ os.name)
    exit(1)