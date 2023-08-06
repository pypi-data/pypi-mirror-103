import functools
import json
import logging
import os
import ast

import requests
from requests.exceptions import ConnectionError
from sys import platform


def get_script_code(record):
    split_record = record.exc_text.split('File')
    split_line = split_record[-1].split(',')
    file_code = split_line[0]
    if platform == "linux" or platform == "linux2":
        file_code.strip()
        file_code.replace('"', "'")
        handle = open(file_code, encoding="utf8")
        script_code = handle.read()
        handle.close()
    elif platform == "win32":
        path_replace = file_code.replace('\"', "")
        path_file = path_replace.replace(':', ':\\').strip()
        handle = open(path_file, encoding="utf8")
        script_code = handle.read()
        handle.close()
    return script_code


class MyHandler(logging.Handler):
    func_data = []
    project_unic = None

    def __init__(self):
        logging.Handler.__init__(self)
        self.args = None

    def emit(self, record):
        message = self.format(record)
        all_args = MyHandler.func_data
        project_id = MyHandler.project_unic
        script_code = get_script_code(record)
        if not all_args:
            my_json = {
                "project_id": project_id,
                "message": message,
                "script_code": script_code,
                "exist": 1
            }
        else:
            MyHandler.func_data = []
            name_function = all_args[0]
            args = all_args[1]
            kwargs = all_args[2]
            my_json = {"project_id": project_id,
                       "script_code": script_code,
                       "message": message,
                       "exist": 0,
                       "name_function": json.dumps(name_function),
                       "args": json.dumps(args, ensure_ascii=False),
                       "kwargs": json.dumps(kwargs)
                       }
        try:
            try:
                f = open('candy.log')
                f.close()
            except FileNotFoundError:
                with open('candy.log', 'w'):
                    pass
            if os.stat("candy.log").st_size == 0:
                requests.post("http://90.189.217.244:8000/api/send/message", json=my_json)
            else:
                json_lines = [line.strip() for line in open("candy.log")]
                for line in json_lines:
                    data = json.loads(json.dumps(line))
                    my_dict = ast.literal_eval(data)
                    requests.post("http://90.189.217.244:8000/api/send/message", json=my_dict)
                requests.post("http://90.189.217.244:8000/api/send/message", json=my_json)
                with open('candy.log', 'w'):
                    pass
        except ConnectionError as e:
            with open("candy.log", 'a') as file:
                file.write(json.dumps(my_json) + '\n')

class InfoHandler(logging.Handler):
    def __init__(self):
        logging.Handler.__init__(self)
        self.args = None

    def emit(self, record):
        message = self.format(record)
        if record.levelname == 'INFO':
            print(message)
        else:
            pass


candy_config = {
    'version': 1,
    'disable_existing_loggers': False,

    'formatters': {
        'my_format': {
            'format': '{asctime} $ {levelname} $ {name} $ '
                      '{module}:{funcName}:{args}:{lineno} $ {message}',
            'datefmt': '%Y-%m-%d %H:%M:%S',
            'style': '{'
        }
    },
    'handlers': {
        'console': {
            '()': MyHandler,
            'level': 'ERROR',
            'formatter': 'my_format'},
    },
    'loggers': {
        '': {
            'level': 'DEBUG',
            'handlers': ['console']
        }
    }
}


def project_key(id_project):
    MyHandler.project_unic = id_project
    return


def candy_wraps(*, entry=True, exit=True, level="ERROR"):
    def wrapper(super):
        name = super.__name__

        @functools.wraps(super)
        def wrapped(*args, **kwargs):
            if entry:
                MyHandler.func_data = [name, args, kwargs]
            result = super(*args, **kwargs)
            if exit:
                pass
            return result

        return wrapped

    return wrapper
