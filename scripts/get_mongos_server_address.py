from cloudify import ctx


def main():
    for key, value in ctx.target.instance.runtime_properties.iteritems():
        if key.startswith('mongo_shard_host_'):
            ctx.logger.info('found mongo shard server: {}'.format(key))
            ctx.source.instance.runtime_properties['mongo_shard_server_address'] = value
            break
    else:
        raise Exception('No Mongo Shard nodes found')


if __name__ == '__main__':
    main()

