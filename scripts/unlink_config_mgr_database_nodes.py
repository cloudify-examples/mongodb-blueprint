from cloudify import ctx


def main():
    ctx.source.instance.runtime_properties.pop('mongo_database_nodes_list', None)


if __name__ == '__main__':
    main()
