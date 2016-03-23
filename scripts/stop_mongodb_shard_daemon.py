import os
from signal import SIGKILL

from cloudify import ctx


def _stop_process():
    os.killpg(
        ctx.instance.runtime_properties['pid'],
        SIGKILL)


def _unset_runtime_properties():
    ctx.instance.runtime_properties.pop('pid', None)
    for runtime_property in ctx.instance.runtime_properties:
        if runtime_property.startswith('mongo_shard_host_'):
            ctx.instance.runtime_properties.pop(runtime_property)


def main():
    try:
        _stop_process()
        _unset_runtime_properties()
    except:
        ctx.logger.exception('failed')
        raise


if __name__ == '__main__':
    main()
