# MagicWord 魔法字

## 概述

MagicWord（魔法字）是玲珑框架中的一种特殊字符串替换机制，用于在运行时动态替换配置文件和数据中的特定标记。魔法字使用 `%%KEYWORD%%` 格式，在程序执行过程中会被自动替换为对应的值。

## 支持的魔法字

| 魔法字 | 描述 | 示例值 |
|--------|------|--------|
| `%%TIME%%` | 当前的 Unix 时间戳 | `1621234567.89` |
| `%%UA_LINGLONG%%` | 玲珑框架的 User-Agent | `YuhengLinglong/1.0` |
| `%%UA_OSMAPI%%` | OSM API 的 User-Agent | `YuhengOSMAPI/1.0` |
| `%%PROJECT_URL%%` | 项目 URL | `https://github.com/geo-yuheng/yuheng-linglong` |
| `%%ENDPOINT(osm-dev)%%` | OSM 开发环境的 API 端点 | `https://master.apis.dev.openstreetmap.org` |
| `%%ENDPOINT(osm)%%` | OSM 生产环境的 API 端点 | `https://api.openstreetmap.org` |
| `%%ENDPOINT(ogf)%%` | OGF API 端点 | `https://opengeofiction.net/api` |

## 使用方法

魔法字可以在以下位置使用：

1. **任务配置文件**：在 `task.json` 中使用魔法字来动态设置端点、标签等
   ```json
   {
       "endpoint": "%%ENDPOINT(osm-dev)%%",
       "changeset_tags": {
           "created_by": "%%UA_LINGLONG%% framework/(%%UA_OSMAPI%%) %%PROJECT_URL%%",
           "comment": "Test edit | %%TIME%%"
       }
   }
   ```

2. **数据文件**：在 CSV 或其他数据文件中使用魔法字
   ```
   ACTION,TYPE,LAT,LON,ID,DATA
   modify,node,24.968128,121.194666,4359497021,{"name":"Test %%TIME%%"}
   ```

## 工作原理

1. 程序在读取配置和数据时，会检测是否存在魔法字
2. 如果找到魔法字，会调用 `magic_transform` 函数将其替换为实际值
3. 替换过程会递归进行，直到所有魔法字都被替换完毕

## 扩展魔法字

如需添加新的魔法字，可以修改 `magic/word.py` 文件中的 `magic_transform` 函数：

```python
def magic_transform(magic_word: str) -> str:
    dict = {
        "%%TIME%%": str(time.time()),
        "%%UA_LINGLONG%%": UA,
        # 在此添加新的魔法字
        "%%NEW_MAGIC_WORD%%": "新的值",
    }
    return dict.get(magic_word, magic_word.replace("%%",""))
```