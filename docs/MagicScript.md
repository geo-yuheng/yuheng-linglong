# MagicScript 魔法脚本

## 概述

MagicScript（魔法脚本）是玲珑框架中的一种标签处理机制，用于在数据处理过程中动态修改标签内容。MagicScript 使用 `%%MAGIC_SCRIPT%%` 键在数据中定义一系列操作命令，这些命令会在程序执行过程中被解析并执行。

## 基本语法

MagicScript 由一系列以分号（`;`）分隔的命令组成。每个命令都有特定的格式和功能。

```
COMMAND1(parameters);COMMAND2(parameters);COMMAND3(parameters)
```

## 支持的命令

### TRANSFER 命令

TRANSFER 命令用于转换或移动标签值。

#### 语法格式

1. **正则表达式提取**：`TRANSFER("target"<-"source".regex("pattern"))`
   - 从 `source` 标签中使用正则表达式 `pattern` 提取内容，并设置为 `target` 标签的值
   - 如果正则表达式包含捕获组，则使用第一个捕获组的内容

2. **设置为空**：`TRANSFER("source"->None)`
   - 删除 `source` 标签

3. **空参数**：`TRANSFER()`
   - 不执行任何操作，通常用作占位符

### DELETE 命令

DELETE 命令用于删除标签。

#### 语法格式

`DELETE("key")`
- 删除 `key` 标签

## 使用示例

在 CSV 数据文件中使用 MagicScript：

```csv
ACTION,TYPE,LAT,LON,ID,DATA
modify,node,24.968128,121.194666,4359497021,{"amenity":"bicycle_rental"&#44;"brand":"YouBike"&#44;"name":"大兴发中央大學圖書館"&#44;"name:en":"National Central University Library"&#44;"%%MAGIC_SCRIPT%%":"TRANSFER(\"branch\"<-\"name\".regex(\"^大兴发(.*?)$\"));TRANSFER();TRANSFER(\"name:en\"->None);DELETE(\"brand:wikidata\")"}
```

上述 MagicScript 将执行以下操作：

1. 从 `name` 标签中提取匹配 `^大兴发(.*?)$` 的内容，并设置为 `branch` 标签的值
2. 跳过空的 TRANSFER 命令
3. 删除 `name:en` 标签
4. 删除 `brand:wikidata` 标签

## 工作原理

1. 程序在处理数据时，检测是否存在 `%%MAGIC_SCRIPT%%` 键
2. 如果找到，解析其中的命令序列
3. 按顺序执行每个命令，修改数据中的标签
4. 执行完所有命令后，删除 `%%MAGIC_SCRIPT%%` 键
5. 返回处理后的数据

## 扩展 MagicScript

如需添加新的命令类型，可以修改 `magic/script.py` 文件中的 `process_command` 函数：

```python
def process_command(cmd: str, data: Dict[str, Any]) -> None:
    # 处理现有命令...
    
    # 添加新的命令类型
    elif cmd.startswith("NEW_COMMAND(") and cmd.endswith(")"):
        params = cmd[12:-1]  # 提取括号内的参数
        # 处理新命令的逻辑
        ...
```