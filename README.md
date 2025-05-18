# yuheng-linglong


linglong 是一个用于进行自动化OSM编辑的bot
这里不使用AI完全用手作自定义实现了一套osmapi（传说中的CRUD仙人），不过其实你也可以试一下接入其他的能OSM操作的python库

具体的推荐列表和适配方法会后续补充。

目前linglong是专门用于全台自行车更新，所以部分方法依然不够抽象，而且比如在match上的方法不一定适用于其他任务。

不过会尽量提供适合各类自动编辑任务的基于距离半径的match、基于特征tag和标识符的match（如brand:wikidata或ref或addr之类），这些匹配应该在其他应用中也可以起作用的我想。

## OAuth2获取授权

### 获取授权登录

用的oauth2

看这个地方的文档

https://wiki.openstreetmap.org/wiki/OAuth#Development_(OAuth_2.0)

### 供调试用的测试APP

```json
{
  "name": "TEST APP",
  "redirect": "urn:ietf:wg:oauth:2.0:oob",
  "id": "d7reaA4FDtkX9mcD2bP4jSftznCSuc2GN-R4jqJQVzU",
  "secret": "0MxXPMD0Ya_px6Ny8QRPtZAWKmsRSPHFI0dlvwF4dVk"
}

```

secret不一定需要写，但id是一定要写的。

## 访问OSM API

文档可以看这里： https://wiki.openstreetmap.org/wiki/API_v0.6

其他的就是通常操作，记得带access_token即可。


### 操作changeset内容

想要对一个changeset进行变更有好几种方法，既可以进行若干次对某个元素的element_update，也可以直接传一个changeset_upload

对于大量元素似乎changeset_upload更有价值更快，但是需要更好的构造XML，可能需要后续接入yuheng来完成。

初期性测试可以先用大量打element_update的方式来完成。

## 特殊功能与系统特性

### 魔法字符串替换系统

linglong 实现了一个强大的魔法字符串替换系统（Magic Word System），允许在配置文件和任务定义中使用特殊标记，这些标记会在运行时自动替换为实际值。例如：

- `%%TIME%%` - 自动替换为当前时间戳
- `%%UA_LINGLONG%%` - 替换为 linglong 的用户代理字符串
- `%%UA_OSMAPI%%` - 替换为 OSMAPI 的用户代理字符串
- `%%PROJECT_URL%%` - 替换为项目 URL
- `%%ENDPOINT(osm-dev)%%` - 替换为开发环境 OSM API 端点
- `%%ENDPOINT(osm)%%` - 替换为生产环境 OSM API 端点
- `%%ENDPOINT(ogf)%%` - 替换为 OGF API 端点

这使得配置文件更加灵活，无需硬编码这些值。

### 多种任务文件格式支持

linglong 支持多种任务文件格式，使其适用于不同的数据源和编辑需求：

1. **action_csv** - 简单的 CSV 格式，包含操作类型（create/modify/delete）和相关数据
2. **osm** - 兼容 JOSM 服务器文件格式
3. **osc (osmchange)** - 支持标准的 OSM 变更格式

### 抽象层设计

项目采用抽象层设计，允许轻松切换不同的 OSM API 实现：

- 默认使用自定义的 yuheng_osmapi 库
- 包含适配层，可以集成其他第三方 OSM 操作库

### 自动化匹配系统

正在开发中的匹配系统将支持：

- 基于地理距离的匹配
- 基于标签（tag）的匹配
- 基于特征标识符（如 brand:wikidata、ref、addr 等）的匹配

这使得 bot 能够智能地识别和更新现有 OSM 元素，而不是创建重复数据。
