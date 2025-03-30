from typing import Optional

import requests
from yuheng import logger

from .tools import transform_tag_xml


def changeset_create(
    endpoint: str, access_token: str, changeset_tag: dict = {}
) -> int:
    """
    # https://wiki.openstreetmap.org/wiki/API_v0.6#Create:_PUT_/api/0.6/changeset/create
    """

    url = endpoint + "/0.6/changeset/create"
    logger.trace(url)

    xml_payload = """
    <osm>
        <changeset>
            {tags}
        </changeset>
    </osm>
    """.replace(
        "{tags}", transform_tag_xml(tag=changeset_tag)
    )
    logger.trace(xml_payload)

    r = requests.put(
        url=url,
        headers={
            "Authorization": f"Bearer {access_token}",
        },
        data=xml_payload,
    )
    (
        logger.success(r.status_code)
        if r.status_code == 200
        else logger.warning(r.status_code)
    )
    logger.debug(r.content)
    return r.text


def changeset_update(endpoint: str, access_token: str, element_id: int):
    """
    # https://wiki.openstreetmap.org/wiki/API_v0.6#Update:_PUT_/api/0.6/changeset/#id
    """

    def squash_to_changeset():
        pass

    url = endpoint + "/0.6/changeset/{element_id}"
    logger.trace(url)

    r = requests.put(
        url="url",
        headers={
            "Authorization": f"Bearer {"access_token"}",
        },
        data="xml_payload",
    )
    (
        logger.success(r.status_code)
        if r.status_code == 200
        else logger.warning(r.status_code)
    )
    logger.debug(r.content)
    return r.text


def changeset_upload(
    endpoint: str,
    access_token: str,
    changeset_id: int,
    osmchange: str = "",
    changeset_data: dict = {},
) -> Optional[None]:
    """
    # https://wiki.openstreetmap.org/wiki/API_v0.6#Diff_upload:_POST_/api/0.6/changeset/#id/upload
    """

    url = endpoint + f"/0.6/changeset/{changeset_id}/upload"
    logger.trace(url)

    if changeset_data != None and changeset_data != {}:
        element_id = changeset_data.get("element_id")
        pass
    else:
        element_id = 1

    def get_osmchange() -> str:
        data = f"""
        <osmChange version="0.6" generator="acme osm editor">
            <modify>
                <node id="{element_id}" changeset="{changeset_id}" version="2" lat="12.1234567" lon="-8.7654321">
                    <tag k="amenity" v="school"/>
                </node>
            </modify>
        </osmChange>
        """
        return data

    xml_payload = get_osmchange()
    logger.trace(xml_payload)

    r = requests.put(
        url=url,
        headers={
            "Authorization": f"Bearer {access_token}",
        },
        data=xml_payload,
    )
    (
        logger.success(r.status_code)
        if r.status_code == 200
        else logger.warning(r.status_code)
    )
    logger.debug(r.content)
    return None


def changeset_close(
    endpoint: str, access_token: str, changeset_id: int
) -> Optional[bool]:
    """
    # https://wiki.openstreetmap.org/wiki/API_v0.6#Close:_PUT_/api/0.6/changeset/#id/close
    """
    url = endpoint + f"/0.6/changeset/{changeset_id}/close"
    logger.trace(url)

    r = requests.put(
        url=url,
        headers={
            "Authorization": f"Bearer {access_token}",
        },
    )
    (
        logger.success(r.status_code)
        if r.status_code == 200
        else logger.warning(r.status_code)
    )
    logger.debug(r.content)
    return r.text
