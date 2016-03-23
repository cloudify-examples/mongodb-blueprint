# cloudify-mongodbV3.2-blueprint
Cloudify MongoDB version 3.2 

### MongoDb Blueprint

This repo contains a blueprint that orchestrates a replicated and sharded [MongoDb](https://docs.mongodb.org/v2.6/) version 2.4.9 database cluster.  The blueprint is compatible with Cloudify version 3.3, targeted at [Openstack](http://docs.getcloudify.org/3.3.1/plugins/openstack/), and utilizes the [script plugin](http://docs.getcloudify.org/3.3.1/plugins/script/) to perform orchestration.

#### Blueprint Operation
The blueprint takes three inputs:
* `image`: The Openstack image ID.  It will be used for all nodes.  Note that any image used must support passwordless sudo.
* `flavor`: The flavor id of the machine.
* `agent_user`: The user used to log in remotely to the image instance.

The following outputs are produced:
* `cluster_info`, with the following key/values:
  * `cfghosts`: the comma separated list of IP:Port identifiers of mongocfg node hosts.
  * `dbhosts`: the comma separated list of IP:Port identifiers of mongod node hosts.

`cfghosts` can be used to connect mongos instances not participating in the blueprint (perhaps from a non-Cloudify managed web tier).  Like all outputs, it is accessible via the REST API and CLI.

The blueprint starts a pair of replication `mongod` nodes, three (for redundancy) `mongocfg` nodes, and a single `mongos` node.  The  `mondgod` nodes are started with the `--shardsvr` option.  The `joiner` node configures the `mongod` nodes into a replicaset, along with publishing the outputs.

#### Blueprint Details
The blueprint, by virtue of the `types/mongotypes.yaml` file, defines 4 key node types and two relationship types that are used in the orchestration:

* <b>Node: `cloudify.nodes.mongod`</b> Represents a [`mongod`](https://docs.mongodb.org/v2.6/reference/program/mongod/) node in the orchestration.  Includes a property, `rsetname`, that defines a replicaset for this node to participate in.  If `rsetname` is omitted, the node will not establish a replicaset (i.e. not be started with the `--replset` option).
* <b>Node: `cloudify.nodes.mongocfg`</b> Represents a [`mongod`](https://docs.mongodb.org/v2.6/reference/program/mongod/) node configured as a config server using the `--configsvr` option.
* <b>Node: `cloudify.nodes.mongos`</b> Represents a [sharding router](https://docs.mongodb.org/v2.6/reference/program/mongos/) for the cluster.  Normally instances of this service are deployed close to consumers (e.g. web or middle tier), but an instance is included in the blueprint for illustration.  Note that the blueprint publishes the addresses and ports of the config servers, and that these outputs can be used to configure mongos services in a production environment, with or without Cloudify orchestration.
* <b> Relationships: `joiner_connected_to_mongocfg` and `joiner_connected_to_mongod`</b>.  These relationships are similar in function, and serve two purposes: to establish a dependency relationship that ensure their targets start first, and to gather IP and port information about the target instances.  Basically, the source side of the relationship recieves runtime properties that contain the IP addresses and ports of each instance in the target.  In this blueprint, the practical effect is that the "joiner" node can gather the appropriate information to initialize replicasets on the cluster after the mongo config and mongod nodes have started.

#### Honorable Mention: the `joiner`

The `joiner` is a node defined in the blueprint itself, because it doesn't represent anything that maps to MongoDb orchestration directly, but is required for blueprint operation. It executes explictly on the server and doesn't require a compute node.  The `joiner` functions much like a thread gate or gatekeeper, and also performs some post deployment tasks for the blueprint.  These tasks could be performed by a separate workflow, but that would make deployment a multi-step process, which was undesirable.  The `joiner` exploits the `joiner_connected_to_mongocfg` and `joiner_connected_to_mongod` relationships as described in the relationships entry above.  After those relationships have fed it the mongod and mongocfg host details, it publishes them to the outputs, and initializes any defined replicasets.  In this blueprint, there is only one.

