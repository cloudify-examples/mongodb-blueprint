[![Build Status](https://circleci.com/gh/cloudify-examples/cloudify-mongodbV3.2-blueprint.svg?style=shield&circle-token=:circle-token)](https://circleci.com/gh/cloudify-examples/cloudify-mongodbV3.2-blueprint)

# cloudify-mongodbV3.2-blueprint

This repo contains a blueprint that orchestrates a replicated and sharded [MongoDb](https://docs.mongodb.org/v3.2.3/) version 3.2.3 database cluster.


## prerequisites

You will need a *Cloudify Manager* running in either AWS, Azure, or Openstack.

If you have not already, set up the [example Cloudify environment](https://github.com/cloudify-examples/cloudify-environment-setup). Installing that blueprint and following all of the configuration instructions will ensure you have all of the prerequisites, including keys, plugins, and secrets.


### Execute Install

Next you provide those inputs to the blueprint and execute install:


#### For AWS run:

```shell
$ cfy install \
    https://github.com/cloudify-examples/cloudify-mongodbV3.2-blueprint/archive/4.0.1.1.zip \
    -b mongo \
    -n aws-blueprint.yaml
```


#### For Azure run:

```shell
$ cfy install \
    https://github.com/cloudify-examples/cloudify-mongodbV3.2-blueprint/archive/4.0.1.1.zip \
    -b mongo \
    -n azure-blueprint.yaml
```


#### For Openstack run:

```shell
$ cfy install \
    https://github.com/cloudify-examples/cloudify-mongodbV3.2-blueprint/archive/4.0.1.1.zip \
    -b mongo \
    -n openstack-blueprint.yaml
```
