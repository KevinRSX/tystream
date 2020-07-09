import log_reader.rl_server as rl
import numpy as np
import matplotlib.pyplot as plt
import os
import glob

def add_to_list(file_path, data_list):
    for file_path in glob.glob(os.path.join(cubic_path, "pensieve_default", "log*")):
        rl_res = rl.RLReader(file_path)
        data_list += rl_res.all_qoe
    for file_path in glob.glob(os.path.join(cubic_path, "sliding_windows", "log*")):
        rl_res = rl.RLReader(file_path)
        data_list += rl_res.all_qoe
    for file_path in glob.glob(os.path.join(cubic_path, "ewma", "log*")):
        rl_res = rl.RLReader(file_path)
        data_list += rl_res.all_qoe

cubic_means = []
cubic_std = []
cubic_fastmpc_list = []
cubic_robustmpc_list = []
cubic_rl_list = []

cubic_path = "../../results/quic/cubic/fcc0/fastMPC"
add_to_list(cubic_path, cubic_fastmpc_list)
cubic_means.append(np.mean(cubic_fastmpc_list))
cubic_std.append(np.std(cubic_fastmpc_list))
cubic_path = "../../results/quic/cubic/fcc0/robustMPC"
add_to_list(cubic_path, cubic_robustmpc_list)
cubic_means.append(np.mean(cubic_robustmpc_list))
cubic_std.append(np.std(cubic_robustmpc_list))
cubic_path = "../../results/quic/cubic/fcc0/RL"
add_to_list(cubic_path, cubic_rl_list)
cubic_means.append(np.mean(cubic_rl_list))
cubic_std.append(np.std(cubic_rl_list))

x = np.arange(3)
width = 0.3
fig, ax = plt.subplots()
ax.bar(x - width, cubic_means, width, label="cubic", yerr=cubic_std)

print("Cubic\n------------------------------------------------------")
print("Mean QoE (fastMPC): " + str(np.mean(cubic_fastmpc_list)))
print("Mean QoE (robustMPC): " + str(np.mean(cubic_robustmpc_list)))
print("Mean QoE (rl): " + str(np.mean(cubic_rl_list)))
print("------------------------------------------------------\n")


bbr_means = []
bbr_std = []
bbr_fastmpc_list = []
bbr_robustmpc_list = []
bbr_rl_list = []

bbr_path = "../../results/quic/bbr/fcc0/fastMPC"
for f in glob.glob(os.path.join(bbr_path, "log*")):
    rl_res = rl.RLReader(f)
    bbr_fastmpc_list += rl_res.all_qoe
bbr_means.append(np.mean(bbr_fastmpc_list))
bbr_std.append(np.std(bbr_fastmpc_list))
bbr_path = "../../results/quic/bbr/fcc0/robustMPC"
for f in glob.glob(os.path.join(bbr_path, "log*")):
    rl_res = rl.RLReader(f)
    bbr_robustmpc_list += rl_res.all_qoe
bbr_means.append(np.mean(bbr_robustmpc_list))
bbr_std.append(np.std(bbr_robustmpc_list))
bbr_path = "../../results/quic/bbr/fcc0/RL"
for f in glob.glob(os.path.join(bbr_path, "log*")):
    rl_res = rl.RLReader(f)
    bbr_rl_list += rl_res.all_qoe
bbr_means.append(np.mean(bbr_rl_list))
bbr_std.append(np.std(bbr_rl_list))

ax.bar(x, bbr_means, width, label="bbr", yerr=bbr_std)

print("BBR\n------------------------------------------------------")
print("Mean QoE (fastMPC): " + str(np.mean(bbr_fastmpc_list)))
print("Mean QoE (robustMPC): " + str(np.mean(bbr_robustmpc_list)))
print("Mean QoE (rl): " + str(np.mean(bbr_rl_list)))
print("------------------------------------------------------\n")


sim_means = []
sim_std = []
sim_fastmpc_list = []
sim_robustmpc_list = []
sim_rl_list = []

sim_path = "../simulator/simulator_fastMPC_fcc0"
rl_res = rl.RLReader(sim_path)
sim_fastmpc_list += rl_res.all_qoe
sim_means.append(np.mean(sim_fastmpc_list))
sim_std.append(np.std(sim_fastmpc_list))
sim_path = "../simulator/simulator_robustMPC_fcc0"
rl_res = rl.RLReader(sim_path)
sim_robustmpc_list += rl_res.all_qoe
sim_means.append(np.mean(sim_robustmpc_list))
sim_std.append(np.std(sim_robustmpc_list))
sim_path = "../simulator/simulator_RL_fcc0"
rl_res = rl.RLReader(sim_path)
sim_rl_list += rl_res.all_qoe
sim_means.append(np.mean(sim_rl_list))
sim_std.append(np.std(sim_rl_list))

ax.bar(x + width, sim_means, width, label="Simulation", yerr=sim_std)

print("Simulation\n------------------------------------------------------")
print("Mean QoE (fastMPC): " + str(np.mean(sim_fastmpc_list)))
print("Mean QoE (robustMPC): " + str(np.mean(sim_robustmpc_list)))
print("Mean QoE (rl): " + str(np.mean(sim_rl_list)))
print("------------------------------------------------------\n")
plt.show()