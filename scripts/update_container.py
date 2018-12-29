import docker


if __name__ == '__main__':
    update_args = {
        'mem_limit': '4G',
        'mem_reservation': '2G',
        'memswap_limit': '8G',
    }
    client = docker.from_env()
    containers = client.containers.list()

    for container in containers:
        container.update(**update_args)




