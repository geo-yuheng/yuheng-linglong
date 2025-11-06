# this layer will pass operation to yuheng default library directly.
from yuheng_osmapi.oauth import oauth_login as yh_osmapi_login
from yuheng.method.network import get_endpoint_api


def changeset_close():
    pass


def changeset_create():
    pass


def changeset_update():
    pass


def changeset_upload():
    pass


def element_create():
    pass


def element_delete():
    pass


def element_read():
    pass


def element_update():
    pass


def oauth_login(
    redirect_uri="urn:ietf:wg:oauth:2.0:oob",
    client_id="",
    client_secret="",
    endpoint_api=get_endpoint_api("osm"),
):

    return yh_osmapi_login(
        redirect_uri="urn:ietf:wg:oauth:2.0:oob",
        client_id="1lMl1Wdv8GRAGqtB9ptzaWqxdvWkee6Jsf6xwD8oeoE",
        client_secret="",
        endpoint_api=get_endpoint_api("osm-dev"),
    )
