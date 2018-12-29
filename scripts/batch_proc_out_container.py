import os

DEBUG=1

def solve_mismatch(container_name):
    """Solve the issue https://github.com/piaozhx/DockerMonitor/issues/12
    :return:
    """
    cudafiles = os.path.join(container_name, "usr/lib/x86_64-linux-gnu/libcuda*")
    nvidiafiles = os.path.join(container_name, "usr/lib/x86_64-linux-gnu/libnvidia*")

    cmd1 = "mv " + "./" + cudafiles + f" /public/inbox/containers/{container_name}"
    cmd2 = "mv " + "./" + nvidiafiles + f" /public/inbox/containers/{container_name}"

    if DEBUG:
        print("Before batch-processing, please think three times before executing!!!")
        print(cmd1)
        print(cmd2)
        import pdb;
        pdb.set_trace()
    import pdb;pdb.set_trace()
    os.system(cmd1)
    os.system(cmd2)

if __name__ == '__main__':
    os.chdir("/public/docker")
    for i, container_name in enumerate(os.listdir()):
        print(container_name)
        solve_mismatch(container_name)


