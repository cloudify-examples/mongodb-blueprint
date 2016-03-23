from cloudify import ctx


def main():
    ctx.source.instance.runtime_properties.pop('mongo_config_hosts', None)


if __name__ == '__main__':
    main()

