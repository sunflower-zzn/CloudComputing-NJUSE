## 使用linux虚拟机配置一个纯分布式的spark集群

​                                                                                                                                         author:wjw

[toc]

#### 1. 更改映射文件/etc/hosts

##### 命令

````shell
vi /etc/hosts
写入另外两台虚拟机的ip地址以及对应主机名称
````

#### 2. 安装jdk并修改环境变量

##### 命令

````shell
tar -zxvf jdk-8u261-linux-x64.tar.gz -C /usr
#环境变量配置
vi ~/.bashrc
export JAVA_HOME=/usr/jdk1.8.0_261/jre
export PATH=$PATH:$JAVA_HOME/bin
#退出文件编辑
source ~/.bashrc
````

#### 3. 安装配置hadoop

##### 命令

````shell
tar -zxvf hadoop-3.2.1.tar.gz -C /usr

#配置环境变量
vi ~/.bashrc
export HADOOP_HOME=/usr/hadoop-3.2.1
export PATH=$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin

source ~/.bashrc

#以下配置三台机器都要配置
vi /usr/hadoop-3.2.1/etc/hadoop/hadoop-env.sh
export JAVA_HOME=/usr/jdk1.8.0_261

vi /usr/hadoop-3.2.1/etc/hadoop/core-site.xml
<configuration>
	<property>
        <name>fs.defaultFS</name>
        <value>hdfs://cMaster:9000</value>
    </property>
    <property>
        <name>hadoop.tmp.dir</name>
        <value>/data/hadoop</value>
    </property>
</configuration>

vi /usr/hadoop-3.2.1/etc/hadoop/mapred-site.xml
<configuration>
    <property>
        <name>mapreduce.framework.name</name>
        <value>yarn</value>
    </property>
</configuration>

vi /usr/hadoop-3.2.1/etc/hadoop/yarn-site.xml
<configuration>
    <property>
        <name>yarn.nodemanager.aux-services</name>
        <value>mapreduce_shuffle</value>
    </property>
    <property>
        <name>yarn.resourcemanager.hostname</name>
        <value>cMaster</value>
    </property>
</configuration>
````

##### 开启hadoop所需命令

````shell
hdfs namenode -format

#进入安装目录下sbin
start-all.sh
````

##### 查看hadoop状态

![0cI3aF.png](https://s1.ax1x.com/2020/10/11/0cI3aF.png)

#### 4. 安装配置spark

````shell
tar -zxvf spark-3.0.1-bin-hadoop3.2.tgz -C /usr

#进入安装文件夹，start-all.sh
#进入安装文件夹，尝试运行实例程序
./bin/run-example SparkPi
#求pi值的一个程序
````

##### 查看spark状态

![0c5og1.png](https://s1.ax1x.com/2020/10/11/0c5og1.png)

#### 5. 查看对应运行状态

````shell
/usr/java/jdk1.8.0._261/bin/jps
````

````
或者直接进入对应端口查看
````

#### 6. 使用root搭建时需要修改的地方

````shell
#root用户需要start-dfs.sh及stop-dfs.sh需要开头添加如下几行
HDFS_DATANODE_USER=root
HADOOP_SECURE_DN_USER=hdfs
HDFS_NAMENODE_USER=root
HDFS_SECONDARYNAMENODE_USER=root
#root用户需要start-yarn.sh及stop-yarn.sh需要开头添加如下几行
YARN_RESOURCEMANAGER_USER=root
HADOOP_SECURE_DN_USER=yarn
YARN_NODEMANAGER_USER=root
````

