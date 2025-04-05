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
