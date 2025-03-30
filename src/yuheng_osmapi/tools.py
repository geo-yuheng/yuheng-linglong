import yuheng
from yuheng import logger


def transform_tag_xml(tag: dict):
    paragraph = ""
    for key, value in tag.items():
        single_line = f'<tag k="{key}" v="{value}"/>\n'
        paragraph += single_line

    return paragraph

def parse_result(result: str) -> yuheng.Carto:
    single_element_world = yuheng.Carto()
    single_element_world.read(mode="memory", text=str(result))
    return single_element_world

def get_version_from_world(node_dict: dict) -> int:
    version_list = []
    for id, obj in node_dict.items():
        version_list.append(obj.version)
    logger.debug(version_list)
    return version_list[0]