import requests
from yuheng import logger

from .tools import transform_tag_xml


def element_create(
    endpoint: str,
    access_token: str,
    changeset_id: int,
    element_type: str,
    data: dict,
) -> int:
    """
    element_type:str -> 三种类型nwr或者完整类型名
    id:int -> 做好区分
    data:dict -> 考虑还有什么需要传入的看加参数还是造字典

    # https://wiki.openstreetmap.org/wiki/API_v0.6#Create:_POST_/api/0.6/[nodes|ways|relations]
    # 注意，这个API的英语单词拼写是复数形式！
    """
    url = endpoint + f"/0.6/{element_type}s"
    logger.trace(url)

    xml_payload = f"""
    <osm>
        <{element_type} changeset="{changeset_id}" lat="31.2356811" lon="121.4685278" visible="true">
            {transform_tag_xml(tag=data)}
        </{element_type}>
    </osm>
    """
    logger.trace(xml_payload)

    r = requests.post(
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


def element_read(
    endpoint: str,
    element_type: str,
    element_id: int,
    access_token: str = "",
):
    """

    # https://wiki.openstreetmap.org/wiki/API_v0.6#Read:_GET_/api/0.6/[node|way|relation]/#id
    """
    url = endpoint + f"/0.6/{element_type}/{element_id}"
    logger.trace(url)

    r = requests.get(
        url=url,
        headers=(
            {
                "Authorization": f"Bearer {access_token}",
            }
            if access_token is not ""
            else {}
        ),
    )
    (
        logger.success(r.status_code)
        if r.status_code == 200
        else logger.warning(r.status_code)
    )
    logger.debug(r.content)
    logger.success(r.text)

    return r.text


def element_update(
    endpoint: str,
    access_token: str,
    changeset_id: int,
    element_type: str,
    element_id: int,
    element_version: int,
    data: dict,
):
    """
    element_type:str -> 三种类型nwr或者完整类型名
    id:int -> 做好区分
    data:dict -> （考虑还有什么需要传入的加参数）

    # https://wiki.openstreetmap.org/wiki/API_v0.6#Update:_PUT_/api/0.6/[node|way|relation]/#id
    """
    url = endpoint + f"/0.6/{element_type}/{element_id}"
    logger.trace(url)

    xml_payload = f"""
    <osm>
        <{element_type} changeset="{changeset_id}" id="{element_id}" lat="31.2356811" lon="121.4685278" version="{element_version}" visible="true">
            {transform_tag_xml(tag=data)}
        </{element_type}>
    </osm>
    """
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


def element_delete(
    endpoint: str,
    access_token: str,
    changeset_id: int,
    element_type: str,
    element_id: int,
    element_version: int,
):
    """
    element_type:str -> 三种类型nwr或者完整类型名
    id:int -> 做好区分

    # https://wiki.openstreetmap.org/wiki/API_v0.6#Delete:_DELETE_/api/0.6/[node|way|relation]/#id
    """
    url = endpoint + f"/0.6/{element_type}/{element_id}"
    logger.trace(url)

    xml_payload = f"""
    <osm>
        <{element_type} changeset="{changeset_id}" id="{element_id}" lat="31.2356811" lon="121.4685278" version="{element_version}" visible="true">
        </{element_type}>
    </osm>
    """
    logger.trace(xml_payload)

    r = requests.delete(
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
