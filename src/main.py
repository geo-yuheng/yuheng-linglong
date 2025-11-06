import json
import time
from typing import Optional, Union

import yuheng
from yuheng import logger
from yuheng.method.network import get_endpoint_api
from yuheng_osmapi.core_changeset import (
    changeset_close,
    changeset_create,
    changeset_update,
    changeset_upload,
)
from yuheng_osmapi.core_element import (
    element_create,
    element_delete,
    element_read,
    element_update,
)
from yuheng_osmapi.oauth import oauth_login
from yuheng_osmapi.tools import get_attribute_from_world, parse_result

from magic import is_there_magic_word, magic_replace, magic_transform


class Task:
    def __init__(self):
        self.read_task()
        if self.task != {}:
            self.endpoint = self.task.get("endpoint")
            self.changeset_tags = self.task.get("changeset_tags")
        else:
            self.endpoint = get_endpoint_api("osm-dev")
            self.changeset_tags = {
                "created_by": "yuheng-linglong framework/(failed to load task)",
            }

    def run(self):
        pass

    def format(self):

        if self.task != {}:
            self.task["endpoint"] = magic_replace(self.task["endpoint"])

            for key in self.task["changeset_tags"]:
                self.task["changeset_tags"][key] = magic_replace(
                    self.task["changeset_tags"][key]
                )

    def read_task(self, task_profile: str = "task.json") -> Optional[dict]:
        with open(task_profile, "r", encoding="utf-8") as f:
            task_raw: str = f.read()
        try:
            task_json = json.loads(task_raw)
            self.task = task_json
            self.format()
            logger.trace(self.task)
            return task_json
        except Exception as e:
            logger.error(e)
            self.task = {}
            return None


def conduct_action(toy: Task, access_token: str, changeset_id: str):

    task_format = toy.task["task_format"]
    logger.debug(task_format)

    def read_action():
        with open(toy.task["task_file"], "r", encoding="utf-8") as f:
            task_raw = f.read()

        logger.debug(task_raw)

        if task_format == "action_csv":
            import pandas as pd

            df = pd.read_csv(toy.task["task_file"])
            dict_list = df.to_dict("records")

        else:
            dict_list = None

        logger.debug(dict_list)

        # 每个逗号都要消灭
        action_list = []
        if dict_list != None:
            for record in dict_list:
                record_replica = record
                record_replica["DATA"] = json.loads(
                    magic_replace(record_replica["DATA"].replace("&#44;", ","))
                )
                action_list.append(record_replica)
        del dict_list
        logger.debug(action_list)

        return action_list

    action_list = read_action()

    for action in action_list:
        if action["ACTION"] == "create":
            # TEST: create element

            element_create(
                endpoint=toy.endpoint,
                access_token=access_token,
                changeset_id=changeset_id,
                element_type=action["TYPE"],
                data=action["DATA"],
                node_lat=action["LAT"],
                node_lon=action["LON"],
            )
        if action["ACTION"] == "modify":
            # modify = read + update

            # TEST: read element

            element_xml_text = element_read(
                endpoint=toy.endpoint,
                access_token=access_token,
                element_type="node",
                element_id=action["ID"],
            )
            element_version = get_attribute_from_world(
                parse_result(element_xml_text).node_dict, attribute="version"
            )
            if action["TYPE"] == "node":
                node_lat = get_attribute_from_world(
                    parse_result(element_xml_text).node_dict, attribute="lat"
                )
                node_lon = get_attribute_from_world(
                    parse_result(element_xml_text).node_dict, attribute="lon"
                )
            logger.debug(f"element_version = {element_version}")

            # IF NEED TAG ETL
            
            # 使用 magic 模块中的函数处理 magic script
            from magic.script import process_magic_script
            action["DATA"] = process_magic_script(action["DATA"])

            # TEST: update element

            if action["TYPE"] == "node":
                element_update(
                    endpoint=toy.endpoint,
                    access_token=access_token,
                    changeset_id=changeset_id,
                    element_type=action["TYPE"],
                    element_id=action["ID"],
                    element_version=element_version,
                    data=action["DATA"],
                    node_lat=node_lat,
                    node_lon=node_lon,
                )
            else:

                element_update(
                    endpoint=toy.endpoint,
                    access_token=access_token,
                    changeset_id=changeset_id,
                    element_type=action["TYPE"],
                    element_id=action["ID"],
                    element_version=element_version,
                    data=action["DATA"],
                )
        if action["ACTION"] == "delete":
            # delete = read + delete

            # TEST: read element

            element_xml_text = element_read(
                endpoint=toy.endpoint,
                access_token=access_token,
                element_type="node",
                element_id=action["ID"],
            )
            element_version = get_attribute_from_world(
                parse_result(element_xml_text).node_dict, attribute="version"
            )
            if action["TYPE"] == "node":
                node_lat = get_attribute_from_world(
                    parse_result(element_xml_text).node_dict, attribute="lat"
                )
                node_lon = get_attribute_from_world(
                    parse_result(element_xml_text).node_dict, attribute="lon"
                )
            logger.debug(f"element_version = {element_version}")

            # TEST: delete element

            if action["TYPE"] == "node":
                element_delete(
                    endpoint=toy.endpoint,
                    access_token=access_token,
                    changeset_id=changeset_id,
                    element_type=action["TYPE"],
                    element_id=action["ID"],
                    element_version=element_version,
                    node_lon=node_lon,
                    node_lat=node_lat,
                )
            else:
                element_delete(
                    endpoint=toy.endpoint,
                    access_token=access_token,
                    changeset_id=changeset_id,
                    element_type=action["TYPE"],
                    element_id=action["ID"],
                    element_version=element_version,
                )


@logger.catch(level="CRITICAL")
def main():

    # 创建任务

    toy = Task()

    # 登录获得token（所有api操作使用，有时间限制）

    access_token = oauth_login(
        redirect_uri="urn:ietf:wg:oauth:2.0:oob",
        client_id="1lMl1Wdv8GRAGqtB9ptzaWqxdvWkee6Jsf6xwD8oeoE",
        client_secret="",
        endpoint_api=get_endpoint_api("osm-dev"),
    )

    # 登录之后的操作

    logger.info(toy.endpoint)

    # TEST: create changeset
    # VITAL
    changeset_id = changeset_create(
        endpoint=toy.endpoint,
        access_token=access_token,
        changeset_tag=toy.changeset_tags,
    )
    logger.info(
        get_endpoint_api("osm-dev").replace("/api", "")
        + f"/changeset/{changeset_id}"
    )

    toy.read_task("task.json")
    logger.debug(toy.task)

    # -------

    conduct_action(
        toy=toy, access_token=access_token, changeset_id=changeset_id
    )
    # exit()

    # -------

    # TEST: close changeset
    # VITAL
    changeset_close(
        endpoint=toy.endpoint,
        access_token=access_token,
        changeset_id=changeset_id,
    )
    logger.warning(
        get_endpoint_api("osm-dev").replace("/api", "")
        + f"/changeset/{changeset_id}"
    )


if __name__ == "__main__":
    main()
