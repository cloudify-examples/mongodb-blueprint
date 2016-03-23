import os
import subprocess
from collections import defaultdict
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError

from cloudify import ctx


def _default_handler():
    return lambda *args, **kwargs: ctx.logger.info(
        'No handling to do in this workflow')


def _scale_handler(mongod_address, mongos_address, mongod_primary_address):
    ctx.logger.info('handling scale workflow')
    _add_mongod_to_repset(mongod_primary_address, mongod_address)
    _add_mongod_as_shard_db(mongos_address, mongod_address)


def _add_mongod_to_repset(mongod_primary_address, mongod_address):
    ctx.logger.info(
        'connecting to primary MongoD: Address={}'.format(mongod_primary_address))
    mongo_binaries_path = ctx.source.instance.runtime_properties['mongo_binaries_path']
    command = ' '.join([
        os.path.join(mongo_binaries_path, 'bin/mongo'),
        '--eval', '"rs.add(\'{}\')"'.format(mongod_address),
        mongod_primary_address
    ])
    output = subprocess.check_output(
        command,
        stderr=subprocess.STDOUT,
        shell=True)
    ctx.logger.info('add mongod to repSet output: {}'.format(output))

    command = ' '.join([
        os.path.join(mongo_binaries_path, 'bin/mongo'),
        '--eval', '"rs.conf()"',
        mongod_primary_address
    ])
    output = subprocess.check_output(
        command,
        stderr=subprocess.STDOUT,
        shell=True)
    ctx.logger.info('mongod repSet status: {}'.format(output))


def _add_mongod_as_shard_db(mongos_address, mongod_address):
    address, port = mongos_address.split(':')
    ctx.logger.info(
        'connecting to MongoS: IP={}, PORT={}'.format(address, port))
    try:
        with MongoClient(host=address, port=int(port)) as mongos:
            node = 'mongo_cluster/{}'.format(mongod_address)
            ctx.logger.info('adding mongo shard: {}'.format(node))
            result = mongos.admin.command('addShard', node)
            ctx.logger.info('mongo shard message result: {}'.format(result))
            ctx.logger.info('mongo status: {}'.format(mongos.admin.last_status()))
    except DuplicateKeyError:
        ctx.logger.exception(
            'connecting to MongoS: IP={}, PORT={}'.format(address, port))


_WORKFLOW_HANDLERS = defaultdict(
    _default_handler,
    scale=_scale_handler,
)


def mongod_address():
    for key, value in ctx.target.instance.runtime_properties.iteritems():
        if key.startswith('mongo_primery_host_'):
            return value
    raise Exception('No Mongo databases nodes found')


def mongod_primary_address():
    return ctx.source.instance.runtime_properties[
        'mongo_database_nodes_list'][0]


def main():
    _WORKFLOW_HANDLERS[ctx.workflow_id](
        mongod_address=mongod_address(),
        mongos_address=ctx.source.instance.runtime_properties[
            'mongo_shard_server_address'],
        mongod_primary_address=mongod_primary_address()
    )


if __name__ == '__main__':
    main()
