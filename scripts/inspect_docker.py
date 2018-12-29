import argparse
import sys
import subprocess
import psutil

def insepect_process(pid):
    """Determine
    1. is the process running in the container
    2. if it's true, ourput the container id and the user

    :return:
    """
    assert psutil.pid_exists(pid), "The process doesn't exist"
    try:
        result = subprocess.check_output(f'cat /proc/{pid}/cgroup', shell=True)
        # print(result)
    except subprocess.CalledProcessError as e:
        return_code = e.returncode
        print(f"Inspect Wrong Error Code{return_code}")
        sys.exit(1)

    line = result.decode('utf-8').split('\n')[0].strip()

    is_in_container = 'docker' in line
    container_id = ''
    user_name = ''

    if is_in_container:
        container_id = line.split('/')[-1][:12] #Only save first 12 char of container id
        container_info = subprocess.check_output(f'docker ps -a|grep {container_id}', shell=True).decode('utf-8')
        user_name = container_info.strip().split()[-1]

    return is_in_container, container_id, user_name

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Inspector for docker")
    parser.add_argument("-p", type=int, help="the pid")
    args = parser.parse_args()

    is_in_container, container_id, user_name = insepect_process(args.p)

    print(f"Is the process running in the container :{is_in_container}")
    print(f"The container id {container_id}")
    print(f"The user name {user_name}")