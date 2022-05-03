from argparse import ArgumentParser
from apscheduler.schedulers.blocking import BlockingScheduler
from threading import Thread
from os import _exit

from project.config import CONFIG_FILE, CLEANER_TIME_INTERVAL_IN_SECONDS, HOST, PORT
from project import app
from project.docker_manager import *

SETTINGS_FILE = 'config.ini'

parser = ArgumentParser(description=f'Docker application server. Look for parameters in the {CONFIG_FILE}.')
parser.add_argument('-d', '--debug', help='run in debug mode', action='store_const', const=True, default=False)
args = parser.parse_args()

scheduler = BlockingScheduler()
scheduler.add_job(clean_containers, 'interval', seconds=CLEANER_TIME_INTERVAL_IN_SECONDS)
cleaner_thread = Thread(target=scheduler.start, args=())
cleaner_thread.start()

with app.app_context():
    try:
        app.run(host=HOST, port=PORT, debug=args.debug)
    except Exception as e:
        print(e)
    finally:
        clean_containers(True)
        _exit(0)
