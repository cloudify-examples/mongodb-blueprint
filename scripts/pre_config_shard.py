from cloudify import ctx


def main():
    try:
        ctx.source.instance.runtime_properties['mongo_config_hosts'] = ','.join(
            value
            for key, value in ctx.target.instance.runtime_properties.iteritems()
            if key.startswith('mongo_config_host_')
        )
    except:
        ctx.logger.exception('failed')
        raise


if __name__ == '__main__':
    main()

