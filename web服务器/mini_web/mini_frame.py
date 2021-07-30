import time


def index():
    return '---index page---'


def login():
    return '---登录界面---'


def register():
    return '---register page---'


def application(env, start_response):
    print("--->>>", env)
    file_name = env['path_info']
    start_response('200 OK', [('Content-Type', 'text/html;charset=utf-8;')])
    if file_name == '/index.py':
        return index()
    elif file_name == '/login.py':
        return login()
    elif file_name == '/register.py':
        return register()
    return '---no this page---%s' % time.time()
