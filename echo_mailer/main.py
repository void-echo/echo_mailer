import json
import logging
import os
import smtplib
from email.mime.text import MIMEText
from getpass import getpass
from pathlib import Path
from time import sleep
from typing import Dict

# import partial
from echo_logger import *

# from flask import Flask
# from flask_cors import CORS
#
# #
# app = Flask(__name__)
# CORS(app, supports_credentials=True)

home = str(Path.home())

config_file_path = os.path.join(home, '.echo_mailer', 'config.json')


def __set_config(config_dict_json_like):
    with open(config_file_path, 'w') as f:
        f.write(config_dict_json_like)
        f.write('\n')


def set_config(config_dict: Dict = None):
    if config_dict is None:
        config_dict = {
            'token': '',
            'smtp_server_site': '',
            'smtp_port': 465,
            'smtp_user_addr': '',
            'from_addr': '',
            'remote_server': '',
        }
        # interactive mode
        print_warn('Echo Mailer is not configured yet. Please follow the instructions to configure it.')
        config_dict['from_addr'] = input(">>> Your email address: ")
        config_dict['smtp_server_site'] = input(">>> Your smtp server site: ")
        config_dict['smtp_port'] = int(input(">>> Your smtp port(leave blank if use default 465): ") or 465)
        config_dict['smtp_user_addr'] = input(">>> Your smtp user address(leave blank if use the same as from_addr): ")
        if not config_dict['smtp_user_addr'] or config_dict['smtp_user_addr'].strip() == '':
            config_dict['smtp_user_addr'] = config_dict['from_addr']
        config_dict['token'] = getpass(">>> Your access token: ")
        config_dict['remote_server'] = input(">>> Your remote server(leave blank if you don't have one): ")

        __set_config(json.dumps(config_dict, indent=4))
    else:
        __set_config(json.dumps(config_dict, indent=4))
    print_debug(f"Echo Mailer is configured successfully. See {config_file_path} for details.")


def get_config() -> Dict:
    with open(config_file_path, 'r') as f:
        config_dict = json.loads(f.read())
    return config_dict


def __send_email(from_addr, to_addr, smtp_server_site, smtp_port, smtp_user_addr=None,
                 subject='No subject', body='Null Text body', access_token=None):
    # 邮件内容
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = from_addr
    smtp_user_addr = from_addr if smtp_user_addr is None else smtp_user_addr
    smtp_server = smtp_server_site
    smtp_port = smtp_port
    smtp_user = smtp_user_addr
    smtp_passwd = access_token
    server = smtplib.SMTP_SSL(smtp_server, smtp_port)
    server.login(smtp_user, smtp_passwd)
    server.sendmail(smtp_user, to_addr, msg.as_string())
    server.quit()


def send_email(to_addr, subject, body):
    config = get_config()
    __send_email(from_addr=config['from_addr'], to_addr=to_addr, smtp_server_site=config['smtp_server_site'],
                 smtp_port=config['smtp_port'], smtp_user_addr=config['smtp_user_addr'], subject=subject, body=body,
                 access_token=config['token'])


def email_monitor(to, task_name='Your Task', use_server=False):
    if not use_server:
        def decorator(func):
            @functools.wraps(func)
            def wrapper_decorator(*args, **kwargs):
                logger = logging.Logger('catch_all')
                try:
                    time_start = time.time()
                    value = func(*args, **kwargs)
                    time_end = time.time()
                    total_time_seconds = time_end - time_start
                    hours, rem = divmod(total_time_seconds, 3600)
                    minutes, seconds = divmod(rem, 60)
                    # print seconds reserving 4 digits
                    if total_time_seconds < 60:
                        time_str = "{:05.4f} seconds".format(seconds)
                    elif total_time_seconds < 3600:
                        time_str = "{:0>2} minutes {:05.4f} seconds".format(int(minutes), seconds)
                    else:
                        time_str = "{:0>2} hours {:0>2} minutes {:05.4f} seconds".format(int(hours), int(minutes),
                                                                                         seconds)
                    print_debug(f"Function {func.__name__}() costs {time_str}.", with_time=True)
                    send_email(to, f"Completion for {task_name}", f"Function {func.__name__}() finished "
                                                                  f"with no error. \n\nTotal time cost: {time_str}")
                    return value
                except Exception as e:
                    logger.error(e, exc_info=True)
                    send_email(to, f"Error for {task_name}", f"Function {func.__name__}() finished "
                                                             f"with error. \n\nError message: \n\n{e}")
                    pass

            return wrapper_decorator

        return decorator

