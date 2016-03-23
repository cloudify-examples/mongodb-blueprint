import os
import socket
import time
import subprocess

from cloudify import ctx


def _port_available(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.bind(('0.0.0.0', port))
        return True
    except:
        return False
    finally:
        s.close()


def _wait_for_server(port, process, server_name):
    ctx.logger.info("Running {} liveness detector on port {}".format(server_name, port))
    for _ in xrange(120):
        if not _port_available(port):
            break
        if process.returncode is not None:
            ctx.logger.error('Process {} finished with return-code: {}'.format(server_name, process.returncode))
            ctx.logger.error('Process {} stdout: {}'.format(server_name, process.returncode))
            raise Exception('Process {} finished with return-code: {}'.format(server_name, process.returncode))
        ctx.logger.info("{} has not started. waiting...".format(server_name))
        time.sleep(1)
    else:
        ctx.logger.error("{} failed to start. waiting for 120 seconds".format(server_name))
        raise Exception()


def _set_runtime_properties(pid, ip, port):
    ctx.instance.runtime_properties.update({
        'pid': pid,
        'mongo_config_host_{}'.format(ip): '{}:{}'.format(ip, port),
    })


def main():
    try:
        mongo_binaries_path = ctx.instance.runtime_properties['mongo_binaries_path']
        mongo_data_path = ctx.instance.runtime_properties['mongo_data_path']
        port = ctx.node.properties['port']
        ip = ctx.instance.host_ip
        process = subprocess.Popen([
                os.path.join(mongo_binaries_path, 'bin/mongod'),
                '--configsvr',
                '--bind_ip', ip,
                '--port', str(port),
                '--dbpath', mongo_data_path,
            ],
            stdout=open(os.path.join('/tmp', 'mongo_config.stdout'), 'w'),
            stderr=open(os.path.join('/tmp', 'mongo_config.stderr'), 'w'))

        _wait_for_server(port, process, 'MongoConfig')
        _set_runtime_properties(process.pid, ip, port)
        ctx.logger.info("Successfully started Mongo Config Server ({})".format(process.pid))
    except:
        ctx.logger.exception('failed')
        raise


if __name__ == '__main__':
    main()
