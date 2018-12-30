import os

DEBUG = 0


def solve_mismatch(container_path):
    """Solve the issue https://github.com/piaozhx/DockerMonitor/issues/12
    :return:
    """
    cudafiles = os.path.join(container_path, "usr/lib/x86_64-linux-gnu/libcuda*")
    nvidiafiles = os.path.join(container_path, "usr/lib/x86_64-linux-gnu/libnvidia*")

    cmd1 = "rm " + cudafiles
    cmd2 = "rm " + nvidiafiles

    print(cmd1)
    print(cmd2)

    os.system(cmd1)
    os.system(cmd2)


def modify_sshconfig(container_path):
    ssh_config = os.path.join(container_path, "etc/ssh/sshd_config")
    cmd = f"echo 'GatewayPorts yes' >> {ssh_config}"
    print(cmd)
    os.system(cmd)


def get_all_container_path():
    root_path = "/public/docker"
    container_path_list = []
    for i, container_name in enumerate(os.listdir(root_path)):
        if container_name == 'prepare_baseline-1':
            continue
        container_path_list.append(os.path.join(root_path, container_name))

    for container_name in os.listdir(os.path.join(root_path, 'prepare_baseline-1')):
        container_path_list.append(os.path.join(root_path, 'prepare_baseline-1', container_name))

    return container_path_list


def main():
    container_path_list = get_all_container_path()
    for container_path in container_path_list:
        print(container_path)
        # solve_mismatch(container_path)
        modify_sshconfig(container_path)


if __name__ == '__main__':
    main()
