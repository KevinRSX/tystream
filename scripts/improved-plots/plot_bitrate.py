import numpy as np
import matplotlib.pyplot as plt

all_log_paths = []
# fastMPC
all_log_paths.append("../../results/fastMPC/cubic/verizon_short/log_fastMPC_Verizon-LTE-short.down")
all_log_paths.append("../../results/fastMPC/bbr/verizon_short/log_fastMPC_Verizon-LTE-short.down")
all_log_paths.append("../../results/fastMPC/cubic/verizon_driving/log_fastMPC_Verizon-LTE-driving.down")
all_log_paths.append("../../results/fastMPC/bbr/verizon_short/log_fastMPC_Verizon-LTE-short.down")
all_log_paths.append("../../results/fastMPC/cubic/att_driving/log_fastMPC_ATT-LTE-driving.down")
all_log_paths.append("../../results/fastMPC/bbr/verizon_short/log_fastMPC_Verizon-LTE-short.down")

# robustMPC
all_log_paths.append("../../results/robustMPC/cubic/verizon_short/log_robustMPC_Verizon-LTE-short.down")
all_log_paths.append("../../results/robustMPC/bbr/verizon_short/log_robustMPC_Verizon-LTE-short.down")
all_log_paths.append("../../results/robustMPC/cubic/verizon_driving/log_robustMPC_Verizon-LTE-driving.down")
all_log_paths.append("../../results/robustMPC/bbr/verizon_short/log_robustMPC_Verizon-LTE-short.down")
all_log_paths.append("../../results/robustMPC/cubic/att_driving/log_robustMPC_ATT-LTE-driving.down")
all_log_paths.append("../../results/robustMPC/bbr/verizon_short/log_robustMPC_Verizon-LTE-short.down")

# naive reinforcement learning
all_log_paths.append("../../results/rl/cubic/verizon_short/log_rl_Verizon-LTE-short.down")
all_log_paths.append("../../results/rl/bbr/verizon_short/log_rl_Verizon-LTE-short.down")
all_log_paths.append("../../results/rl/cubic/verizon_driving/log_rl_Verizon-LTE-driving.down")
all_log_paths.append("../../results/rl/bbr/verizon_short/log_rl_Verizon-LTE-short.down")
all_log_paths.append("../../results/rl/cubic/att_driving/log_rl_ATT-LTE-driving.down")
all_log_paths.append("../../results/rl/bbr/verizon_short/log_rl_Verizon-LTE-short.down")

def get_mean(pos_in_path):
    total_bitrate = 0
    change_num = 0
    for i in range(1, 11):
        with open(all_log_paths[pos_in_path] + str(i),  'r') as f:
            for line in f:
                row = str.split(line)
                total_bitrate += int(row[1])
                change_num += 1
    return total_bitrate / change_num

def autolabel(rects, xpos='center'):
    ha = {'center': 'center', 'right': 'left', 'left': 'right'}
    offset = {'center': 0, 'right': 1, 'left': -1}

    for rect in rects:
        height = int(rect.get_height())
        ax.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(offset[xpos]*3, 3),  # use 3 points offset
                    textcoords="offset points",  # in both directions
                    ha=ha[xpos], va='bottom')


fastMPC = []
for i in range(6):
    fastMPC.append(get_mean(i))
robustMPC = []
for i in range(6, 12):
    robustMPC.append(get_mean(i))
rl = []
for i in range(12, 18):
    rl.append(get_mean(i))

width = 0.3
ind = np.arange(6)
fig, ax = plt.subplots()
reacts1 = ax.bar(ind - width, fastMPC, width, label='fastMPC')
reacts2 = ax.bar(ind, robustMPC, width, label='robustMPC')
reacts3 = ax.bar(ind + width, rl, width, label='reinforcement learning')
"""
autolabel(reacts1)
autolabel(reacts2)
autolabel(reacts3)
"""
ax.set_xticks(ind)
ax.set_xticklabels(("cubic verizon short", "bbr verizon short", "cubic verizon driving",
"bbr verizon driving", "cubic att driving", "bbr att driving"), rotation=45, ha="right")
ax.set_ylim([0, 6000])
plt.xlabel("congestion control and trace")
plt.ylabel("bitrate(Mbit/s)")
ax.legend()
fig.tight_layout()
plt.show()
