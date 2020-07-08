def to_server(original):
    if original == "mpc":
        return "mpc_server"
    elif original == "robust_mpc":
        return "robust_mpc_server"
    elif original == "pensieve":
        return "rl_server_no_training"
    else:
        return None

def to_html(original):
    if original == 'mpc':
        return 'myindex_fastMPC'
    elif abr_rule == 'robust_mpc':
        return 'myindex_robustMPC'
    elif abr_rule == 'pensieve':
        return 'RL'
    else:
        return None