from cloudify import ctx


def main():
    for key, value in ctx.target.instance.runtime_properties.iteritems():
        if key.startswith('mongo_config_host_'):
            ctx.logger.info('found mongo config server: {}'.format(key))
            ctx.source.instance.runtime_properties['mongo_config_server_address'] = value
            break
    else:
        raise Exception('No Mongo Shard nodes found')


if __name__ == '__main__':
    main()

