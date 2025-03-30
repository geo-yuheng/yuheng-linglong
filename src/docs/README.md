对于linglong支持的任务文件，初步考虑是提供以下几种形式
1. action_csv
这个会比较便于按照OSMAPI抽象，类似josm的服务器文件一样，也便于快速构造

2. osm
这种的就是jsom服务器文件，一定是得带有action的才行，对于平凡的osm文件，不带有action的element会被直接忽略掉，也应当这么做，因为你不确定它是增添还是服务器上已有。

3. osc （osmchange）
直接按照osm里面的三种操作工作，也是类似josm服务器文件

总之就是想法传进来create/modify/delete以及操作面向的对象就可以了。上面是三种可以传入操作的格式。

而纯粹的数据，例如一个点位和数据的csv，因为它不包含具体的osm操作，就需要写一个转换器转换到linglong支持的格式