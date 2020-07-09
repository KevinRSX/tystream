def to_server(original):
    if original == "mpc":
        return "mpc_server"
    elif original == "robustmpc":
        return "robust_mpc_server"
    elif original == "pensieve":
        return "rl_server_no_training"
    else:
        return None

def to_html(original):
    if original == 'mpc':
        return 'myindex_fastMPC'
    elif original == 'robustmpc':
        return 'myindex_robustMPC'
    elif original == 'pensieve':
        return 'RL'
    else:
        return None