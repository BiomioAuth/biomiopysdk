from coreapi.biomio_messaging_api import BiomioMessagingAPI


if __name__ == "__main__":
    app_type = "probe"
    dev_id = "c1d277535c7fbc2"
    os_id = "Android_6.0.1"
    network_type = "WIFI"
    api = BiomioMessagingAPI(app_type=app_type, dev_id=dev_id, os_id=os_id)
    response = api.hello({'secret': ""})
    print response
    if response.header.oid == 'serverHello':
        api.ack()
