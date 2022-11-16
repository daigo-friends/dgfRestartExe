import argparse
import os
import json
import subprocess
import sys

from logging import getLogger, config, handlers
from time import sleep
import time

import psutil
script_dir = os.path.dirname(sys.argv[0])
script_name = os.path.splitext(os.path.basename(sys.argv[0]))[0]
script_json = os.path.join(script_dir, script_name + '.json')

with open(script_json, 'r') as f:
    conf = json.load(f)
config.dictConfig(conf['log_conf'])
logger = getLogger('main')
time_out = int(conf['timeout'])

if __name__ == "__main__":
    logger.debug(__file__)

    parser = argparse.ArgumentParser(description="指定されたPIDのプログラムの終了を待って再起動を行うプログラム")
    parser.add_argument("pid", help="再起動するPIDを指定してください。")
    parser.add_argument("cmd", help="再起動するコマンドラインを指定してください。")
    args = parser.parse_args()
    logger.info('args:%s, %s', args.pid, args.cmd)

    # 時間計測開始
    time_sta = time.time()

    while True:
        if not psutil.pid_exists(int(args.pid)):
            # VSCodeで実行すると、dgfRestartExeの終了とともに、ここで起動したプログラムも終了してしまうので注意する
            # ⇒pyInstallerでexe化したものを実行すれば良い
            #result = subprocess.Popen(args.cmd,shell=False) 
            result = subprocess.Popen(args.cmd,shell=False) 
            break
        sleep(0.1)

        # 時間計測終了
        time_end = time.time()
        # 経過時間（秒）
        tim = time_end- time_sta

        if tim > time_out:
            logger.info('タイムアウトしました。')
            break
