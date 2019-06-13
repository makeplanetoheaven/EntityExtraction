# 1.知识图谱基础介绍
　　一个完整的知识图谱数据，主要由七个部分组成：\
　　**（1）类型**\
　　类型是根据不同实体所包含的属性来进行划分的，类型是对具有相同特点或属性的实体集合的抽象。例如，中国是一个实体，美国是一个实体，法国是一个实体，这些实体都具有共同的特征，可以抽象为国家类型。\
　　**（2）域**\
　　域是类型的集合，凌驾于类型之上，是对某一领域所有类型的抽象。例如，国家是对中国、美国这样实体的一种抽象，是一种类型，而一个地理位置除了国家类型之外，还包括其他类型：城市，区，州等，而把这些类型抽象起来，就形成了地理位置域。\
　　**（3）实体**\
　　实体是对客观个体的抽象，一个人，一部电影，一句话都可以看作是一个实体。另外，实体既可表示真实世界的个体信息，也可以用于表示某个抽象概念（概念网络）。\
　　**（4）实体属性**\
　　实体属性是一个实体所具有特征的描述，属性本身不能在进行细分。例如，一个人的年龄，姓名，性别，身高。\
　　**（5）关系**\
　　关系是实体与实体之间关系的抽象，关系是有向的。\
　　**（6）关系属性（权重）**\
　　关系属性描述了一个关系所具有的特征，例如关系建立的时间，关系的重要性（权值）等。\
　　**（7）属性值**\
　　属性值是用来描述一个实体或关系的具体信息，可以分为文本型和数值型。
# 2.数据类型介绍``
　　知识图谱数据的存储，主要分为两个部分：\
　　**（1）实体属性存储**\
　　实体属性存储通过一个链表（list）来完成，链表中的每一个元素是一个字典(dict)，该字典只包含两个key，一个是实体的类型（type）,另外一个是实体属性（property），实体属性也是一个字典，字典中的每一个key代表实体的一个属性，对应的value代表相应属性值。整个链表最终以json格式存储。其结构如下图：\
　　![在这里插入图片描述](https://img-blog.csdnimg.cn/2019042416274737.?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzI4Mzg1NTM1,size_16,color_FFFFFF,t_70)
　　**（2）实体间关系存储**\
　　实体间关系存储是通过一个实体关系三元组链表（list(list)）来完成，链表中的每一个元素是一个实体关系三元组：\
　　**[实体1，关系，实体2]**。\
　　其中，实体1，实体2分别是实体在实体信息链表里面的位置索引，关系是一个字典，该字典包含两个key，一个是关系的名字（name）,另外一个是关系属性（property）。整个链表最终以json格式存储。其结构如下图：\
![在这里插入图片描述](https://img-blog.csdnimg.cn/20190424163056538.)
# 3.数据集介绍（数据持续更新）
　　目前已有的数据如下：
<table>
    <tr>
        <th>域</th>
        <th>实体类型</th>
        <th>关系类型</th>
        <th>数据量</th>
        <th>下载链接</th>
        <th>提取码</th>
   </tr>
    <tr>
        <td rowspan='3'>地理位置域</td>
        <td>中国城市</td>
        <td>首都，省会，属于，包含，直辖市</td>
        <td>70W+城市实体</td>
        <td><a> https://pan.baidu.com/s/1q_Ji58A2tN9dtY3tg4Be_w </a></td>
        <td>9isc</td>
    </tr>
    <tr>
        <td>中国飞机场</td>
        <td>位于</td>
        <td>298个机场实体</td>
        <td><a> https://pan.baidu.com/s/1g7RuL7GnTIRcqorn9tjVMg </a></td>
        <td>gy7f</td>
    </tr>
    <tr>
        <td>中国火车站</td>
        <td>位于</td>
        <td>1022个火车站实体</td>
        <td><a> https://pan.baidu.com/s/1t8nbt4OsHjIcCq8o7BCOhA</a> </td>
        <td>jrm2</td>
    </tr>
</table>

# 4.代码介绍（代码持续更新）
**github**:https://github.com/makeplanetoheaven/EntityExtraction
## 4.1 实体及实体间关系爬取
目前已有代码内容如下
<table>
    <tr>
        <th>域</th>
        <th>实体类型</th>
        <th>关系类型</th>
        <th>抽取网站</th>
        <th>代码位置</th>
        <th>调用位置</th>
   </tr>
    <tr>
        <td rowspan='3'>地理位置域</td>
        <td>中国城市</td>
        <td>首都，省会，属于，包含，直辖市</td>
        <td><a>http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2018/</a></td>
        <td>./EntityRelation/GeographicalDomain/China/CityCrawler</td>
        <td>./Debug</td>
    </tr>
    <tr>
        <td>中国飞机场</td>
        <td>位于</td>
        <td><a>https://baike.baidu.com/item/%E6%9C%BA%E5%9C%BA/74273</a></td>
        <td>./EntityRelation/GeographicalDomain/China/AirportCrawler</td>
        <td>./Debug</td>
    </tr>
    <tr>
        <td>中国火车站</td>
        <td>位于</td>
        <td><a>http://hcp.bendibao.com/station.html</a></td>
        <td>./EntityRelation/GeographicalDomain/China/TrainStationCrawle </td>
        <td>./Debug</td>
    </tr>
</table>

## 4.2 实体信息爬取
### 4.2.1 基于百度百科的实体信息抽取
　　基于百度百科的实体信息抽取，主要是通过爬取百科中相应实体的基本介绍，基本属性，来作为实体属性进行存储。代码目录位于`./EntityInformation/BaiduEncyclopedia.py`。代码如下：\
![在这里插入图片描述](https://img-blog.csdnimg.cn/20190424165354559.?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzI4Mzg1NTM1,size_16,color_FFFFFF,t_70)
## 4.3 数据存储到图数据库Neo4j
　　本项目提供连接到图数据，并将爬取到数据存储到图数据库的接口，代码目录位于`./Neo4j/Neo4j.py`。通过创建一个Neo4j对象，输入相应链接信息（用户名，密码，端口等）后，即可调用相应函数进行操作。
　　**（1）数据存储到图数据库调用顺序如下**\
![在这里插入图片描述](https://img-blog.csdnimg.cn/20190424170209685.)