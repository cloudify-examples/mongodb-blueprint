from cloudify import ctx


def main():
    ctx.source.instance.runtime_properties.pop('mongo_config_server_address', None)


if __name__ == '__main__':
    main()