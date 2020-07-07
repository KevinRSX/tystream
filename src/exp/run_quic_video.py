import sys
import subprocess
import time
import signal
import os

import pyautogui

from client import Client

trace_name = sys.argv[1]
cmd_rlserver = "python2 ./abr_server/mpc_server.py " + "qcubic_" + trace_name

# cmd_chrome = "google-chrome-stable \
# --no-proxy-server \
# --enable-quic \
# --origin-to-force-quic-on=www.quictest.com:443 \
# --host-resolver-rules='MAP www.quictest.com:443 100.64.0.1:6121' \
# https://www.quictest.com/myindex_fastMPC.html"

client = Client('mpc')
cmd_client = client.generate_client_cmd()

print(cmd_rlserver)
print(cmd_client)

proc1 = subprocess.Popen("exec " + cmd_rlserver, shell=True)
proc2 = subprocess.Popen("exec " + cmd_client, shell=True)
time.sleep(2)
pyautogui.click(102, 449)
time.sleep(220)
proc1.send_signal(signal.SIGINT)
proc2.send_signal(signal.SIGINT)
