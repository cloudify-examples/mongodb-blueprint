from pymongo import MongoClient

from cloudify import ctx


def _setup_initiate_database(address, nodes_list):
    address, port = address.split(':')
    ctx.logger.info('starting mongo configuration: IP={}, PORT={}'.format(address, port))
    config = {
        '_id': 'mongo_cluster',
        'version': 1,
        'members': [
            {'_id': index, 'host': address}
            for index, address in enumerate(nodes_list)
        ],
    }
    with MongoClient(host=address, port=int(port)) as mongo_config:
        ctx.logger.info('mongo configuration: {}'.format(config))
        result = mongo_config.admin.command('replSetInitiate', config)
        ctx.logger.info('mongo config message result: {}'.format(result))
        ctx.logger.info('mongo status: {}'.format(mongo_config.admin.last_status()))


def _setup_shard_database(address, nodes_list):
    address, port = address.split(':')
    ctx.logger.info('starting mongo shard: IP={}, PORT={}'.format(address, port))
    with MongoClient(host=address, port=int(port)) as mongos:
        nodes = 'mongo_cluster/' + ','.join(nodes_list)
        ctx.logger.info('adding mongo shard: {}'.format(nodes))
        result = mongos.admin.command('addShard', nodes)
        ctx.logger.info('mongo shard message result: {}'.format(result))
        ctx.logger.info('mongo status: {}'.format(mongos.admin.last_status()))


def main():
    try:
        database_config_address = ctx.instance.runtime_properties['mongo_config_server_address']
        database_shard_address = ctx.instance.runtime_properties['mongo_shard_server_address']
        database_nodes_list = ctx.instance.runtime_properties['mongo_database_nodes_list']
        _setup_initiate_database(database_config_address, database_nodes_list)
        _setup_shard_database(database_shard_address, database_nodes_list)
    except:
        ctx.logger.exception('failed')
        raise


if __name__ == '__main__':
    main()

