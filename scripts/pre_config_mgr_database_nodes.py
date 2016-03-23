from cloudify import ctx


def main():
    ctx.source.instance.runtime_properties['mongo_database_nodes_list'] = [
        value
        for key, value in ctx.target.instance.runtime_properties.iteritems()
        if key.startswith('mongo_primery_host_')
    ]
    if not ctx.source.instance.runtime_properties['mongo_database_nodes_list']:
        raise Exception('No Mongo databases nodes found')


if __name__ == '__main__':
    main()

