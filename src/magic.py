# this file provide magic word parse service
import time
import re
from typing import Union, Dict, Any

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


# Magic Script 处理功能
def process_magic_script(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    处理 DATA 中的 magic script
    
    Args:
        data: 包含标签的字典
        
    Returns:
        处理后的字典
    """
    # 检查是否存在 MAGIC_SCRIPT
    if "%%MAGIC_SCRIPT%%" not in data:
        return data
    
    logger.warning("Found MAGIC_SCRIPT in DATA")
    magic_script = data["%%MAGIC_SCRIPT%%"]
    logger.warning(f"Raw MAGIC_SCRIPT: {magic_script}")
    
    # 解析 MAGIC_SCRIPT 命令（以分号分隔）
    commands = magic_script.split(";")
    logger.warning(f"Total commands in MAGIC_SCRIPT: {len(commands)}")
    
    # 处理每个命令
    for i, cmd in enumerate(commands):
        cmd = cmd.strip()
        if not cmd:  # 跳过空命令
            continue
        
        logger.warning(f"Command {i+1}: {cmd}")
        process_command(cmd, data)
    
    # 删除 MAGIC_SCRIPT 键
    del data["%%MAGIC_SCRIPT%%"]
    logger.warning("Removed %%MAGIC_SCRIPT%% key from DATA")
    
    # 输出处理后的所有标签
    logger.warning("Final DATA tags:")
    for k, v in data.items():
        logger.warning((k, v))
    
    return data


def process_command(cmd: str, data: Dict[str, Any]) -> None:
    """
    处理单个 magic script 命令
    
    Args:
        cmd: 命令字符串
        data: 包含标签的字典
    """
    # 处理 TRANSFER 命令
    if cmd.startswith("TRANSFER(") and cmd.endswith(")"):
        params = cmd[9:-1]  # 提取括号内的参数
        logger.warning(f"TRANSFER params: {params}")
        
        # 处理空参数的 TRANSFER
        if not params:
            logger.warning("Empty TRANSFER command, skipping")
            return
        
        # 处理正则表达式转换: "target"<-"source".regex("pattern")
        regex_match = re.match(r'"([^"]+)"<-"([^"]+)"\.regex\("([^"]+)"\)', params)
        if regex_match:
            target_key, source_key, pattern = regex_match.groups()
            logger.warning(f"Regex transfer: {source_key} -> {target_key} with pattern {pattern}")
            
            if source_key in data:
                source_value = data[source_key]
                match = re.search(pattern, source_value)
                if match and match.groups():
                    data[target_key] = match.group(1)
                    logger.warning(f"Extracted '{data[target_key]}' from '{source_value}' and set to '{target_key}'")
                else:
                    logger.warning(f"No match found for pattern '{pattern}' in '{source_value}'")
            else:
                logger.warning(f"Source key '{source_key}' not found in data")
            return
        
        # 处理 "source"->None 格式（清除标签）
        none_match = re.match(r'"([^"]+)"->None', params)
        if none_match:
            key = none_match.group(1)
            logger.warning(f"Setting {key} to None (removing)")
            if key in data:
                del data[key]
            return
    
    # 处理 DELETE 命令
    elif cmd.startswith("DELETE(") and cmd.endswith(")"):
        params = cmd[7:-1]  # 提取括号内的参数
        logger.warning(f"DELETE params: {params}")
        
        # 提取键名（去掉引号）
        key_match = re.match(r'"([^"]+)"', params)
        if key_match:
            key = key_match.group(1)
            logger.warning(f"Deleting key: {key}")
            
            if key in data:
                del data[key]
                logger.warning(f"Deleted key '{key}' from data")
            else:
                logger.warning(f"Key '{key}' not found in data")
        else:
            logger.warning(f"Invalid DELETE parameter format: {params}")
    else:
        logger.warning(f"Unknown command format: {cmd}")
