import os
cmd_rlserver = "python ../rl_server/mpc_server.py tcp &"

cmd_chrome = "google-chrome-stable \
--no-proxy-server \
http://144.214.121.6/myindex_fastMPC.html"

print(cmd_rlserver)
print(cmd_chrome)

os.system(cmd_rlserver)
os.system(cmd_chrome)