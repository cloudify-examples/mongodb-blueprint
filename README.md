# cloudify-mongodbV3.2-blueprint
Cloudify MongoDB version 3.2 and above

### MongoDb Blueprint

This repo contains a blueprint that orchestrates a replicated and sharded [MongoDb](https://docs.mongodb.org/v3.2.3/) version 3.2.3 database cluster.
The blueprint is compatible with Cloudify version 3.4, targeted at [Openstack](http://docs.getcloudify.org/3.3.1/plugins/openstack/),
And utilizes the [script plugin](http://docs.getcloudify.org/3.3.1/plugins/script/) to perform orchestration.

#### Blueprint Operation
The blueprint takes three inputs:
* `image`: The Openstack image ID.  It will be used for all nodes.  Note that any image used must support passwordless sudo.
* `flavor`: The flavor id of the machine.
* `user`: The user used to log in remotely to the image instance.
* `mongo_verion`: the MondoDB verion to install [defuolt 3.2.3]
* `mongod_port`: Mongod process port [default 27017]
* `mongos_port`: Mongos process port [default 27018]
* `mongo_config_port`: Mongo config process MGR port [default 27019]

The blueprint starts a replication of one `mongod` node,
One (for redundancy) `mongo_config` node,
And a single `mongos` node.
The `mondgod` nodes are started with the `--shardsvr` option.
The `mongo_mgr` node configures the `mongod` nodes into a replicaset,
And `mongo_mgr` node configures the `mongod` nodes a shard.

#### Blueprint Details
The blueprint, by virtue of the `types/mongodbtypes.yaml` file, defines 4 key node types and 4 relationship types that are used in the orchestration:

* <b>Node: `cloudify.nodes.mongod`</b> Represents a [`mongod`](https://docs.mongodb.org/v3.2.3/reference/program/mongod/) node in the orchestration.
* <b>Node: `cloudify.nodes.mongo_config`</b> Represents a [`mongod`](https://docs.mongodb.org/v3.2.3/reference/program/mongod/) node configured as a config server using the `--configsvr` option.
* <b>Node: `cloudify.nodes.mongos`</b> Represents a [sharding router](https://docs.mongodb.org/v3.2.3/reference/program/mongos/) for the cluster.  Normally instances of this service are deployed close to consumers (e.g. web or middle tier), but an instance is included in the blueprint for illustration.  Note that the blueprint publishes the addresses and ports of the config servers, and that these outputs can be used to configure mongos services in a production environment, with or without Cloudify orchestration.
* <b> Relationships: `mongos_depends_on_mongo_config`, `mongo_mgr_connect_mondo_config`, `mongo_mgr_connect_mondos`, and `mongo_mgr_connect_mondod`</b>.  These relationships are similar in function, and serve two purposes: to establish a dependency relationship that ensure their targets start first, and to gather IP and port information about the target instances.  Basically, the source side of the relationship recieves runtime properties that contain the IP addresses and ports of each instance in the target.  In this blueprint, the practical effect is that the "mongo_mgr" node can gather the appropriate information to initialize replicasets and create a shard on the cluster after the mongo config and mongod nodes have started.

#### Honorable Mention: the `mongo_mgr`

The `mongo_mgr` is a node defined in the blueprint itself, because it doesn't represent anything that maps to MongoDb orchestration directly, but is required for blueprint operation. It executes explictly on the server and doesn't require a compute node.  The `mongo_mgr` functions much like a thread gate or gatekeeper, and also performs some post deployment tasks for the blueprint.  These tasks could be performed by a separate workflow, but that would make deployment a multi-step process, which was undesirable.  The `mongo_mgr` exploits the `mongo_mgr_connect_mondo_config`, `mongo_mgr_connect_mondos`, and `mongo_mgr_connect_mondod` relationships as described in the relationships entry above.  After those relationships have fed it the mongod and mongocfg host details, it publishes them to the outputs, and initializes any defined replicasets and shards.  In this blueprint, there is only one for each.
