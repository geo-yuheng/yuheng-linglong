# Magic word processing module
import time
from typing import Union

from yuheng import logger
from yuheng.method.network import get_endpoint_api
from yuheng_osmapi.const import UA as UA_osmapi

from const import PROJECT_URL, UA


def magic_transform(magic_word: str) -> str:
    """
    转换指定的玲珑魔法字到指定的python变量值
    找不到的时候返回原内容
    """
    dict = {
        "%%TIME%%": str(time.time()),
        "%%UA_LINGLONG%%": UA,
        "%%UA_OSMAPI%%": UA_osmapi,
        "%%PROJECT_URL%%": PROJECT_URL,
        "%%ENDPOINT(osm-dev)%%": get_endpoint_api("osm-dev"),
        "%%ENDPOINT(osm)%%": get_endpoint_api("osm"),
        "%%ENDPOINT(ogf)%%": get_endpoint_api("ogf"),
    }
    return dict.get(magic_word, magic_word.replace("%%",""))


def is_there_magic_word(uncertain_value) -> Union[str, bool]:
    """
    如果找得到魔法字就返回第一个魔法字
    如果找不到就返回False
    """
    import re

    result = re.findall(pattern=r"%%(?!MAGIC_SCRIPT%%).*?%%", string=uncertain_value)
    logger.trace(result)
    if result != []:
        return result[0]
    else:
        return False


def magic_replace(uncertain_string) -> str:
    """
    对一条字符串进行判断是否存在魔法字并自动替换的操作
    """
    cached_string = uncertain_string
    while is_there_magic_word(cached_string):
        current_time_magic_word = is_there_magic_word(cached_string)
        logger.trace(current_time_magic_word)
        cached_string = cached_string.replace(
            current_time_magic_word,
            magic_transform(current_time_magic_word),
        )
    certain_string = cached_string
    return certain_string