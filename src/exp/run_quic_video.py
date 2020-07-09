import sys
import subprocess
import time
import signal
import os
import argparse

import pyautogui

from client import Client
import abr_name_converter

parser = argparse.ArgumentParser()
parser.add_argument("abr")
parser.add_argument("cc")
parser.add_argument("transport")
parser.add_argument("trace_name")
parser.add_argument("id")
args = parser.parse_args()
trace_name = args.trace_name
abr = args.abr
transport = args.transport
cc = args.cc
id = args.id
cmd_abrserver = "python2 ./abr_server/" + abr_name_converter.to_server(abr) + ".py " + transport + "_" + cc + "_" + trace_name + id

# cmd_chrome = "google-chrome-stable \
# --no-proxy-server \
# --enable-quic \
# --origin-to-force-quic-on=www.quictest.com:443 \
# --host-resolver-rules='MAP www.quictest.com:443 100.64.0.1:6121' \
# https://www.quictest.com/myindex_fastMPC.html"

client = Client(abr, transport)
cmd_client = client.generate_client_cmd()

print(cmd_abrserver)
print(cmd_client)

proc1 = subprocess.Popen("exec " + cmd_abrserver, shell=True)
proc2 = subprocess.Popen("exec " + cmd_client, shell=True)
time.sleep(2)
pyautogui.click(102, 449)
time.sleep(220)
proc1.send_signal(signal.SIGINT)
proc2.send_signal(signal.SIGINT)
