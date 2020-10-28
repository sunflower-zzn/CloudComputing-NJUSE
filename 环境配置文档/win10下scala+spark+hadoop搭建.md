# win10下scala+spark+hadoop搭建

> 本文主要介绍win10环境下搭建hadoop伪分布式集群
>
> 说明：不推荐使用3.0以上Hadoop，因为笔者在HDFS格式化时出现主机地址映射问题无法解决

环境：

- JDK：1.8.0.261
- scala：2.12.12
- spark：3.0.1
- hadoop：2.7.7
# 环境搭建
## JDK 1.8
**下载地址**：

**注意**：建议选择JAVA 8，详细的安装配置教程请Google，注意环境变量JAVA_HOME和PATH的配置

**验证**：命令行输入 ` java -version ` 

![image.png](https://cdn.nlark.com/yuque/0/2020/png/295691/1602348324760-91c67f95-32ba-405c-b594-42b1b1acc49c.png)

### Scala
**下载地址**：[https://www.scala-lang.org/download/all.html](https://www.scala-lang.org/download/all.html)，页面下方下载msi文件进行安装

**注意**：Scala和JDK、Spark均有版本对应关系

- Spark runs on Java 8+, Python 2.7+/3.4+ and R 3.1+. For the Scala API, Spark 2.4.0 uses Scala 2.11. You will need to use a compatible Scala version (2.11.x).
- _![image.png](https://cdn.nlark.com/yuque/0/2020/png/295691/1602348170678-bc14fd3e-6b5f-47da-8128-37a57512131e.png)_



**验证**：命令行输入 ` scala `

_![image.png](https://cdn.nlark.com/yuque/0/2020/png/295691/1602348418238-729de30a-438e-4bec-947a-c8dab6fee12b.png)_

### Spark
**下载地址**：[http://spark.apache.org/downloads.html](http://spark.apache.org/downloads.html)，选择对应版本的spark和hadoop并下载解压

注意：Spark文件目录中**不允许含有空格**！记得将/bin添加至环境变量中

**验证**：命令行输入 ` spark-shell` 

![image.png](https://cdn.nlark.com/yuque/0/2020/png/295691/1602350314258-1b8700ce-1e03-40f4-8fff-fdbe9f3c8fe6.png)

### Hadoop
**下载地址**：[https://archive.apache.org/dist/hadoop/common/](https://archive.apache.org/dist/hadoop/common/)，选择对应的版本解压并配置环境变量

**注意**：hadoop在windows上运行需要**winutils**支持和hadoop.dll等文件

#### winutils支持
下载地址：[https://github.com/cdarlint/winutils](https://github.com/cdarlint/winutils)

下载对应版本的winutils并替换hadoop的bin文件（下载可以使用[Github文件夹下载](https://minhaskamal.github.io/DownGit/#/home)）

#### jdk支持
Hadoop基于Java实现的，所以依赖了JDK，需要修改etc\hadoop\hadoop-env.cmd文件（**根据自己的jdk路径**）

![image.png](https://cdn.nlark.com/yuque/0/2020/png/295691/1602350705472-d74f4059-496c-47ea-8648-1cf3870eb3db.png)

（此处修改是因为Hadoop本身存在bug，无法识别JAVA_HOME的环境变量读取到jdk地址，所以直接写死）

**验证**：命令行输入 ` hadoop version ` 
![image.png](https://cdn.nlark.com/yuque/0/2020/png/295691/1602350797645-3df8914f-1314-4e6f-94d7-068b9de66d94.png)

# Hadoop分布式集群配置

## 分布式集群配置

注：以下配置文件请均按照自己hadoop的安装路径进行相应修改

**\etc\hadoop\core-site.xml**

```xml
<configuration>
	<property>
       <name>fs.default.name</name>
       <value>hdfs://localhost:9000</value>
   </property>
</configuration>
```
**\etc\hadoop\hdfs-site.xml**
```xml
<configuration>
    <property>
        <name>dfs.replication</name>
        <value>1</value>
    </property>
	<property> 
     <name>dfs.permissions</name> 
     <value>false</value> 
  </property>
   <property>
       <name>dfs.namenode.name.dir</name>
       <value>/C:/develop/hadoop-2.7.7/data/namenode</value>
   </property>
   <property>
		<name>fs.checkpoint.dir</name>
		<value>/C:/develop/hadoop-2.7.7/data/snn</value>
	</property>
	<property>
		<name>fs.checkpoint.edits.dir</name>
		<value>/C:/develop/hadoop-2.7.7/data/snn</value>
	</property>
	   <property>
       <name>dfs.datanode.data.dir</name>
       <value>/C:/develop/hadoop-2.7.7/data/datanode</value>
   </property>
</configuration>
```
**\etc\hadoop\mapred-site.xml**
```xml
<configuration>
	<property>
       <name>mapreduce.framework.name</name>
       <value>yarn</value>
   </property>
</configuration>
```
**\etc\hadoop\yarn-site.xml**
```xml
<configuration>
	<property>
    	<name>yarn.nodemanager.aux-services</name>
    	<value>mapreduce_shuffle</value>
   </property>
   <property>
      	<name>yarn.nodemanager.auxservices.mapreduce.shuffle.class</name>  
		<value>org.apache.hadoop.mapred.ShuffleHandler</value>
   </property>
</configuration>
```
## 启动Hadoop
1、命令行输入 ` hdfs namenode -format ` 格式化文件系统
![image.png](https://cdn.nlark.com/yuque/0/2020/png/295691/1602351313845-57b0f391-138f-4d17-849c-507675ae29e3.png)

说明：可能会出现如下中断，但只要没有其他错误并且有红框内容即为成功（win特有问题，主机地址映射）

![image.png](https://cdn.nlark.com/yuque/0/2020/png/295691/1602351421477-d556e8b1-a828-4db3-9f69-be120fe55f88.png)

【以上命令只在初始化时执行，格式化完成后再次使用时直接从下面命令开始即可】

2、接下来进入路径："C:\develop\hadoop-2.7.7\sbin"，执行命令` .\start-all.cmd` 

![hadoop运行截图.png](https://cdn.nlark.com/yuque/0/2020/png/295691/1602351616587-0f454759-5769-4d78-8ded-9c9994b588c8.png)

可以看到我们启动了四个服务，通过命令` jps ` 显示得，分别是

- Hadoop Namenode（文件系统目录，类似于书的目录部分）
- Hadoop datanode（数据文件内容，就是书的正文）
- YARN Resourc Manager（统一节点管理、调度者）
- YARN Node Manager （各个子节点）
## HDFS应用管理
### 查询节点状态
浏览器访问：[http://localhost:8088/](http://localhost:9870/)

![8088.png](https://cdn.nlark.com/yuque/0/2020/png/295691/1602351830163-bac2aa95-0053-402e-ac51-bc2c58d199a8.png)

由于以上配置为单节点，所以可以看到我们的一个节点以及集群状况

### 文件管理
浏览器访问：[http://localhost:50070/](http://localhost:9870/)（3.0以上Hadoop：[http://localhost:9870/](http://localhost:9870/)）

![namenode.png](https://cdn.nlark.com/yuque/0/2020/png/295691/1602351978756-cb7050a2-f2c2-4285-9a97-d385570c0e29.png)

# 参考文章
[Window（win10）下安装Hadoop3.0.0安装步骤介绍](https://blog.csdn.net/caopeng721210/article/details/108750671?depth_1-)

[Spark在Windows下的环境搭建](https://blog.csdn.net/u011513853/article/details/52865076)

[windows环境搭建hadoop集群](https://www.jianshu.com/p/1e7e9a70262d)