# stackstorm3.1自定义镜像制作

## 1.file目录说明

```shell
.
├── Dockerfile_st2actionrunner    #构建st2actionrunner容器
├── Dockerfile_st2api    #构建st2actionrunner容器
└── file
    ├── ansible.tar.gz    #ansible2.08的virtualenvs虚拟环境，以免安装慢，所以预制
    ├── ansible-file    #固定目录，ansible的playbook及配置文件目录，懂ansible的都能看懂
    │   ├── playbooks    #固定目录，playbooks目录，执行ansible指定此目录下的步骤进行
    │   │   └── test    #自定义名称目录，test测试playbooks目录
    │   ├── roles    #固定目录，脚本目录，在playbooks定义调用此目录下脚本
    │   │   └── test    #自定义名称目录，test脚本目录
    │   │       ├── install_docker_ce    #自定义名称目录，安装docer脚本的目录
    │   │       │   └── tasks    #固定目录，脚本目录，名称固定
    │   │       └── test    #自定义名称目录，测试的脚本目录
    │   │           └── tasks    #固定目录，脚本目录，名称固定
    │   └── stage    #固定目录，hosts目录
    │       └── test    #自定义名称目录，test的hosts目录
    ├── packs			#固定目录，stackstorm的packs模块目录
    │   ├── ansible_core    #自定义名称目录，名称为ansible_core的pack模块目录
    │   │   └── actions    #固定目录，脚本目录
    │   │       ├── scripts    #自定义名称目录，调用的脚本类型分类目录
    │   │       └── workflows    #自定义名称目录，调用的脚本类型分类目录
    │   └── test    #自定义名称目录，名称为test的pack模块目录
    │       ├── actions    #固定目录，脚本目录
    │       │   ├── shell     #自定义名称目录，调用的脚本类型分类目录
    │       │   └── workflows    #自定义名称目录，调用的脚本类型分类目录
    │       └── rules    #固定目录，规则脚本目录
    └── python-tests-file	#python脚本目录
        └── __pycache__

```

## 2.文件说明
### 2.1 Dockerfile_st2actionrunner文件说明

```shell
.
├── Dockerfile_st2actionrunner    #此文件说明
├── Dockerfile_st2api
├── file
└── README.md
```

此文件为安装ansible必要组件及更新ansible脚本使用

```shell
FROM stackstorm/st2actionrunner:3.3.0

RUN sudo apt-get update && sudo apt-get install -y gcc libkrb5-dev sshpass

ADD file/ansible.tar.gz /opt/stackstorm/virtualenvs/

COPY file/ansible-file /etc/ansible
COPY file/python-tests-file /src/tests
```
修改好file文件夹内的ansible脚本执行如下命令构建镜像
```shell
docker build -f Dockerfile_st2actionrunner -t st2actionrunner:v1 ./
```
### 2.2 Dockerfile_st2actionrunner文件说明

```shell
.
├── Dockerfile_st2actionrunner
├── Dockerfile_st2api    #此文件说明
├── file
└── README.md
```



此文件为安装stackstorm的pack包或者自己编写pack包使用（因st2api和st2actionrunner同时挂载了/opt/stackstorm/packs/目录，并且st2api先写入此目录到本地存储，所以更新此容器）

```shell
FROM stackstorm/st2api:3.3.0

COPY file/packs/ /opt/stackstorm/packs/
```
修改好file文件夹内的pack包执行如下命令构建镜像
```shell
docker build -f Dockerfile_st2api -t st2api:v1 ./
```


### 2.3 ansible文件说明
#### 2.3.1 ansible.tar.gz文件说明
```shell
.
├── Dockerfile
├── file
│   ├── ansible.tar.gz    #此文件说明
│   ├── ansible-file
│   ├── packs
│   └── python-tests-file
└── README.md
```
此文件为ansible 2.08版本的virtualenvs虚拟环境，以免安装慢，所以预制
在st2actionrunner容器内安装过程如下

```shell
apt-get update && apt-get install -y gcc libkrb5-dev

bash -c 'source /opt/stackstorm/st2/bin/activate \
    && virtualenv -p /usr/bin/python3 /opt/stackstorm/virtualenvs/ansible'

bash -c 'source /opt/stackstorm/virtualenvs/ansible/bin/activate \
    && pip install setuptools==44.0.0 -i http://liyulei.f3322.net:8081/repository/pypi/simple --trusted-host liyulei.f3322.net \
    && pip install zipp==0.5.0 -i http://liyulei.f3322.net:8081/repository/pypi/simple --trusted-host liyulei.f3322.net'

RUN bash -c 'source /opt/stackstorm/virtualenvs/ansible/bin/activate \
    && pip install -r /stackstorm-ansible-requirements.txt -i http://liyulei.f3322.net:8081/repository/pypi/simple --trusted-host liyulei.f3322.net'

```

stackstorm-ansible-requirements.txt文件内容如下
```shell
ansible>=1.9
pywinrm[credssp,kerberos]>=0.2.2
netaddr>=0.7.19
```

#### 2.3.2 ansible.cfg配置文件
```shell
.
├── Dockerfile
├── file
│   ├── ansible.tar.gz
│   ├── ansible-file
│   ├── packs
│   │   ├── ansible_core
│   │   │   ├── ansible.cfg    #此文件说明
│   │   │   ├── playbooks
│   │   │   ├── roles 
│   │   │   └── stage
│   │   └── test
│   │       └── actions
│   │       └── rules
│   └── python-tests-file
└── README.md
```
build-stackstorm-image/file/ansible-file/ansible.cfg文件为ansible默认的配置文件
```shell
[defaults]
roles_path = roles    #指定role存放路径
host_key_checking = False    #ansible第一次连接客户端是是否要检查ssh密钥
deprecation_warnings = False    #运行时是否报deprecation_warnings警告信息
```

#### 2.3.3 main.yml脚本
```shell
.
├── Dockerfile
├── file
│   ├── ansible.tar.gz
│   ├── ansible-file
│   │   ├── ansible.cfg
│   │   ├── playbooks
│   │   ├── roles
│   │   │   └── test
│   │   │       └── install_docker_ce
│   │   │           └── tasks
│   │   │               └── main.yml    #此文件说明
│   │   └── stage
│   ├── packs
│   │   ├── ansible_core
│   │   └── test
│   └── python-tests-file
└── README.md
```
build-stackstorm-image/file/ansible-file/roles/test/install_docker_ce/tasks/main.yml文件为脚本文件
```shell
---
- name: install yum-utils device-mapper-persistent-data lvm2    #步骤名称
  yum:    #调用yum模块
    name: ['yum-utils', 'device-mapper-persistent-data', 'lvm2']    #yum安装的软件名称
    state: present    #安装选项present或者installed为安装套件，latest为安装最新版套件；absent、removed 为卸载
    update_cache: yes    #是否更新缓存
    use_backend: yum

- name: install docker-ce.repo    #步骤名称
  shell: "yum-config-manager --add-repo http://mirrors.aliyun.com/docker-ce/linux/centos/docker-ce.repo && yum makecache fast"    #使用shell模块执行命令

- name: install docker-ce    #步骤名称
  yum:
    name: ['docker-ce']
    state: present
    update_cache: yes
    use_backend: yum

- name: start docker    #步骤名称
  systemd:    #调用systemd模块（服务管理模块）
    name: docker    #服务名称
    state: restarted    #为服务执行重启操作
    enabled: yes    #是否设置为开机启动
    daemon_reload: yes    #是否读取配置文件

- stat:    #模块名称（检查文件或文件系统的状态）
    path: /usr/local/bin/docker-compose    #获取的文件绝对路径
  register: docker_compose    #设定调用名称在下面会调用此步骤结果

- name: download docker-compose    #步骤名称
  get_url:    #模块名称（下载文件模块）
    url: "{{ docker_compose_download_url }}"    #地址，此处调用变量，此变量可在build-stackstorm-image/file/ansible-file/stage/用户自定义名称/group_vars/all.yml中定义，本项目中在stackstorm的ansible模块中定义，定义方式在stackstorm案例4中
    dest: /usr/local/bin/docker-compose    #文件下载位置
    validate_certs: no    #SSL证书是否验证，没有ssl证书的网站填no
    mode: 0755    #文件权限
  when: not docker_compose.stat.exists    #调用docker_compose的结果，如果docker_compose下的stat模块返回信息为exists（没有）则执行此步骤
```

模块说明连接
```shell
https://www.kancloud.cn/louis1986/ansible/544332
```

#### 2.3.4 install_docker_ce.yml乐本文件，定义执行步骤
```shell
.
├── Dockerfile
├── file
│   ├── ansible.tar.gz
│   ├── ansible-file
│   │   ├── ansible.cfg
│   │   ├── playbooks
│   │   │   └── test
│   │   │       └── install_docker_ce.yml    #此文件说明
│   │   ├── roles
│   │   └── stage
│   ├── packs
│   │   ├── ansible_core
│   │   └── test
│   └── python-tests-file
└── README.md
```
build-stackstorm-image/file/ansible-file/playbooks/test/install_docker_ce.yml乐本文件，定义执行步骤
```shell
---
- name: install_docker_ce    #定义步骤名称
  hosts: all    #运行此步骤的主机all为全部，也可写分组或者指定主机名称
  roles:
    - test/install_docker_ce    #脚本所在目录
  tags: install_docker_ce    #任务标签名称
```

#### 2.3.5 inventory文件，hosts文件
```shell
.
├── Dockerfile
├── file
│   ├── ansible.tar.gz
│   ├── ansible-file
│   │   ├── ansible.cfg
│   │   ├── playbooks
│   │   ├── roles
│   │   └── stage
│   │       └── test
│   │           └── inventory    #此文件说明
│   ├── packs
│   │   ├── ansible_core
│   │   └── test
│   └── python-tests-file
└── README.md
```
build-stackstorm-image/file/ansible-file/stage/test/inventory为hosts文件，定义执行脚本的主机信息
```shell
registry ansible_host=10.211.55.151   ansible_port=22     ansible_user=root   ansible_password=huacloud
主机名称  ip地址                        ssh端口号            用户名               密码
```
可以在build-stackstorm-image/file/ansible-file/stage/test/group_vars/all.yml中定义变量，例如上面build-stackstorm-image/file/ansible-file/roles/test/install_docker_ce/tasks/main.yml文件变量docker_compose_download_url
```shell
docker_compose_download_url=http://*******
```

有了以上文件，可以在安装有ansible的服务器上执行如下命令启动脚本
```shell
ansible ­playbook -­i /etc/ansible/stage/test/inventory /etc/ansible/playbooks/test/install_docker_ce.yml
```


### 2.4stackstorm文件说明
#### 2.4.1 icon.png文件
```shell
.
├── Dockerfile
├── file
│   ├── ansible.tar.gz
│   ├── ansible-file
│   ├── packs
│   │   ├── ansible_core
│   │   └── test
│   │       ├── actions
│   │       ├── rules
│   │       ├── icon.png    #此文件说明
│   │       └── pack.yaml
│   └── python-tests-file
└── README.md
```

build-stackstorm-image/file/packs/test/icon.png
此文件为图片文件，最终显示在stackstorm的web页面下图1样式

（图1）
![Image text](https://raw.githubusercontent.com/liyuleizhang/img/main/stackstorm/WX20210422-161215.png)

#### 2.4.2 pack.yaml文件说明
```shell
.
├── Dockerfile
├── file
│   ├── ansible.tar.gz
│   ├── ansible-file
│   ├── packs
│   │   ├── ansible_core
│   │   └── test
│   │       ├── actions
│   │       ├── rules
│   │       ├── icon.png
│   │       └── pack.yaml    #此文件说明
│   └── python-tests-file
└── README.md
```

build-stackstorm-image/file/packs/test/pack.yaml
此文件为模块说明文件
```shell
---
ref: test    #模块名称，只能英文，web页面显示，见图2，和模块文件夹保持一致build-stackstorm-image/file/packs/test
name: test    #模块名称，只能英文，可以当做说明使用，web页面不显示，安装的时候显示
description: 测试各种功能    #模块说明
keywords:    #搜索时的标签
    - example
    - test
version: 0.0.1    #模块版本，自定义
python_versions:    #stackstorm平台的python版本（下面所写python2和3均可用）
  - "2"
  - "3"
author: 张三    #此模块作者
email: zhangsan@163.com    #此模块作者邮箱
```
（图2）
![Image text](https://raw.githubusercontent.com/liyuleizhang/img/main/stackstorm/WX20210422-161424.png)

#### 2.4.3 actions脚本文件
任务脚本
文件路径build-stackstorm-image/file/packs/包名称/actions/

web页面位置

![Image text](https://raw.githubusercontent.com/liyuleizhang/img/main/stackstorm/WX20210426-112908.png)

##### 2.4.3.1 例1
build-stackstorm-image/file/packs/test/actions/1.touch_ansible_inventory.yaml
build-stackstorm-image/file/packs/test/actions/workflows/1.touch_ansible_inventory.yaml 
```shell
.
├── Dockerfile
├── file
│   ├── ansible.tar.gz
│   ├── ansible-file
│   ├── packs
│   │   ├── ansible_core
│   │   └── test
│   │       ├── actions
│   │       │   ├── 1.touch_ansible_inventory.yaml    #此文件说明   
│   │       │   ├── shell
│   │       │   └── workflows
│   │       │       └── 1.touch_ansible_inventory.yaml    #此文件说明
│   │       ├── rules
│   │       ├── icon.png
│   │       └── pack.yaml
│   └── python-tests-file
└── README.md
```
build-stackstorm-image/file/packs/test/actions/1.touch_ansible_inventory.yaml文件为模块文件，对比见图3
```shell
---
name: 1.touch_ansible_inventory    #模块名称，与文件名相同
description: 创建ansible的...ssword。    #模块说明
runner_type: orquesta    #模块类型，orquesta为调用yaml或json文件
entry_point: workflows/1.touch_ansible_inventory.yaml    #调用的文件位置
enabled: true
parameters:    #输入框
  node01_1_ansible_hosts:    #输入框名称
    type: string    #输入框内填写的文件类型
    required: true    #输入框是否比填
    description: node1节点ip地址（例如：192.168.1.2）    #输入框说明文字
    default: ''    #如果不输入的默认值，此处为空值，必须人工填写
    position: 1    #输入框内填写后的默认变量是$1,供entry_point: workflows/1.touch_ansible_inventory.yaml调用
  node01_2_ansible_port:
    type: integer
    required: true
    description: node1节点ssh端口,不填默认22端口（例如：22）
    default: 22
    position: 2
  node01_3_ansible_user:
    type: string
    required: true
    description: node1节点用户名，不填默认root用户（例如：root）
    default: root
    position: 3
  node01_4_ansible_password:
    required: true
    description: node1节点密码（例如：123456）
    default: ''
    position: 4
```

（图3）
![Image text](https://raw.githubusercontent.com/liyuleizhang/img/main/stackstorm/WX20210422-164050.png)

build-stackstorm-image/file/packs/test/actions/workflows/1.touch_ansible_inventory.yaml脚本文件
```shell
version: 1.0   #版本
description: 创建inventory文件，并输入一条记录   #本脚本说明
input:    #调用build-stackstorm-image/file/packs/test/actions/1.touch_ansible_inventory.yaml下的输入框内容
- node01_1_ansible_hosts    #输入框名称
- node01_2_ansible_port    #输入框名称
- node01_3_ansible_user    #输入框名称
- node01_4_ansible_password    #输入框名称
tasks:    #脚本
  touch_ansible_inventory:    #名称
    action: core.local_sudo    #调用core下的local_sudo模块
    input:    #调用上面input导入的变量
      cmd: 'echo "node01 ansible_host="{{ ctx("node01_1_ansible_hosts") }}" ansible_port="{{ ctx("node01_2_ansible_port") }}" ansible_user="{{ ctx("node01_3_ansible_user") }}" ansible_password="{{ ctx("node01_4_ansible_password") }}"" >/etc/ansible/stage/test/inventory && cat /etc/ansible/stage/test/inventory'    #在local_sudo模块下的cmd输入框输入''内的内容，"{{ ctx("##") }}"为调用的变量
```

actions/1.touch_ansible_inventory.yaml和actions/workflows/1.touch_ansible_inventory.yaml文件关系图如图4

（图4）
![Image text](https://raw.githubusercontent.com/liyuleizhang/img/main/stackstorm/WX20210423-092025.png)

实际例1编写的两个脚本的功能可以在core模块下的local_sudo中的cmd中输入如下内容，执行后和例1结果相同，如图5
```shell
echo "node01 ansible_host=ip地址 ansible_port=端口号 ansible_user=用户名 ansible_password=密码" >/etc/ansible/stage/test/inventory && cat /etc/ansible/stage/test/inventory
```
（图5）
![Image text](https://raw.githubusercontent.com/liyuleizhang/img/main/stackstorm/WX20210423-093105.png)

例1与2.add_ansible_hosts.yaml和2.add_ansible_hosts.yaml写法与调用相同，参照例1理解

##### 2.4.3.2 例2
build-stackstorm-image/file/packs/test/actions/3.create_ansible_inventory.yaml
build-stackstorm-image/file/packs/test/actions/shell/3.create_ansible_inventory.sh
```shell
.
├── Dockerfile
├── file
│   ├── ansible.tar.gz
│   ├── ansible-file
│   ├── packs
│   │   ├── ansible_core
│   │   └── test
│   │       ├── actions
│   │       │   ├── 3.create_ansible_inventory.yaml    #此文件说明   
│   │       │   ├── shell
│   │       │   │   └── 3.create_ansible_inventory.sh    #此文件说明
│   │       │   └── workflows
│   │       ├── rules
│   │       ├── icon.png
│   │       └── pack.yaml
│   └── python-tests-file
└── README.md
```
build-stackstorm-image/file/packs/test/actions/3.create_ansible_inventory.yaml文件为模块文件，对比见图6
```shell
---
name: 3.create_ansible_inventory    #模块名称，与文件名相同
runner_type: "local-shell-script"    #模块类型，此类型支持在指定主机中执行shell脚本
description: "创建ansible的in。。。word。"    #模块说明
enabled: true
entry_point: 'shell/3.create_ansible_inventory.sh'    #调用shell脚本位置
parameters:    #输入框
  sudo:    #设置以管理员身份运行
    default: true
    immutable: true
  node01:    #输入框名称
    type: string    #输入内容类型
    required: true   #输入框是否比填
    description: '填写格。。。56）'    #输入框说明文字
    default: 'node01 ansible_host=192.168.1.1 ansible_port=22 ansible_user=root ansible_password=123456'   #如果不输入的默认值
    position: 1   #输入框内填写后的默认变量是$1,供entry_point: 'shell/3.create_ansible_inventory.sh'调用
  node02:
    type: string
    required: true
    description: '填写格式:节点名称 ansible_host=ip地址 ansible_port=ssh端口 ansible_user=用户名 ansible_password=密码,不填则为空。（例如：node02 ansible_host=192.168.1.2 ansible_port=22 ansible_user=root ansible_password=123456）'
    default: '#'
    position: 2
  node03:
    type: string
    required: true
    description: '填写格式:节点名称 ansible_host=ip地址 ansible_port=ssh端口 ansible_user=用户名 ansible_password=密码,不填则为空。（例如：node03 ansible_host=192.168.1.3 ansible_port=22 ansible_user=root ansible_password=123456）'
    default: '#'
    position: 3
  node04:
    type: string
    required: true
    description: '填写格式:节点名称 ansible_host=ip地址 ansible_port=ssh端口 ansible_user=用户名 ansible_password=密码,不填则为空。（例如：node04 ansible_host=192.168.1.4 ansible_port=22 ansible_user=root ansible_password=123456）'
    default: '#'
    position: 4

```

（图6）
![Image text](https://raw.githubusercontent.com/liyuleizhang/img/main/stackstorm/WX20210423-101848.png)

build-stackstorm-image/file/packs/test/actions/shell/3.create_ansible_inventory.sh脚本文件
这个就是普通的shell脚本
```shell
#!/usr/bin/env bash

node01=$1
node02=$2
node03=$3
node04=$4

cat > /etc/ansible/stage/test/inventory <<- EOF
${node01}
${node02}
${node03}
${node04}
EOF

cat /etc/ansible/stage/test/inventory
```

actions/3.create_ansible_inventory.yaml和actions/shell/3.create_ansible_inventory.sh对应图如图7

（图7）
![Image text](https://raw.githubusercontent.com/liyuleizhang/img/main/stackstorm/WX20210423-103258.png)

##### 2.4.3.3 例3
build-stackstorm-image/file/packs/test/actions/4.testing_ansible_inventory.yaml
build-stackstorm-image/file/packs/test/actions/workflows/4.testing_ansible_inventory.yaml 
```shell
.
├── Dockerfile
├── file
│   ├── ansible.tar.gz
│   ├── ansible-file
│   ├── packs
│   │   ├── ansible_core
│   │   └── test
│   │       ├── actions
│   │       │   ├── 4.testing_ansible_inventory.yaml    #此文件说明   
│   │       │   ├── shell
│   │       │   └── workflows
│   │       │       └── 4.testing_ansible_inventory.yaml    #此文件说明
│   │       ├── rules
│   │       ├── icon.png
│   │       └── pack.yaml
│   └── python-tests-file
└── README.md
```
build-stackstorm-image/file/packs/test/actions/4.testing_ansible_inventory.yaml文件为模块文件，对比见图8
```shell
---
name: 4.testing_ansible_inventory    #模块名称，与文件名相同
description: 查看创建的ansible_inventory文件内容，并测试是否能正常连通，ansible的ping命令    #模块说明
runner_type: orquesta    #模块类型，orquesta为调用yaml或json文件
entry_point: workflows/4.testing_ansible_inventory.yaml    #调用的文件位置
enabled: true
parameters:    #输入框
  filepath:    #输入框名称
    description: "inventory文件的绝对路径"    #输入框说明文字
    default: "/etc/ansible/stage/test/inventory"    #默认带入值
    type: string   #输入框内填写的文字类型
    required: true   #输入框是否比填
    position: 0    #输入框内填写后的默认变量是$0
```

（图8）
![Image text](https://raw.githubusercontent.com/liyuleizhang/img/main/stackstorm/WX20210423-120527.png)

build-stackstorm-image/file/packs/test/actions/workflows/4.testing_ansible_inventory.yaml脚本文件
```shell
version: 1.0   #版本
description: 查看指定inventory文件，并测试是否能正常连通，ansible的ping命令   #本脚本说明
input:    #调用build-stackstorm-image/file/packs/test/actions/4.testing_ansible_inventory.yaml下的输入框内容
- filepath    #输入框名称
tasks:    #脚本
  cat_ansible_inventory:    #第一个脚本名称
    action: core.local_sudo cmd='cat {{ ctx("filepath") }}'    #调用core下的local_sudo模块下的cmd输入框输入''内的内容，"{{ ctx("##") }}"为调用的变量
    next:    #判断
    - when: "{{ succeeded() }}"    #如果执行完本脚本返回为succeeded完成
      do:    #则执行下面的内容
      - ping_ansible_inventory    #执行名称为ping_ansible_inventory的脚本
    - when: "{{ failed() }}"    #如果执行完本脚本返回为failed未完成
      do:    #则执行下面的内容
      - fail    #停止运行
  ping_ansible_inventory:    #第二个脚本名称
    action: ansible.command inventory_file='{{ ctx("filepath") }}' hosts='all' module_name='ping'   #调用ansible下的command模块下的inventory_file输入框输入''内的内容，"{{ ctx("##") }}"为调用的变量，hosts输入框内的内容指定为all，module_name输入框内的内容指定为ping
```

actions/4.testing_ansible_inventory.yaml和actions/workflows/4.testing_ansible_inventory.yaml文件关系图如图9

（图9）
![Image text](https://raw.githubusercontent.com/liyuleizhang/img/main/stackstorm/WX20210423-113006.png)

实际例3编写的两个脚本的功能可以在core模块下的local_sudo中的cmd中输入如下内容，执行后再在ansible模块下的command中的inventory_file、hosts、module_name输入如下内容执行后和例3结果相同，如图10
```shell
core模块下的local_sudo中的cmd中输入如下内容
cat /etc/ansible/stage/test/inventory

ansible模块下的command中的inventory_file输入如下内容
/etc/ansible/stage/test/inventory
ansible模块下的command中的hosts输入如下内容
all
ansible模块下的command中的module_name输入如下内容
ping
```
（图10）
![Image text](https://raw.githubusercontent.com/liyuleizhang/img/main/stackstorm/WX20210423-114131.png)

##### 2.4.3.4 例4
build-stackstorm-image/file/packs/test/actions/5.install_docker_ce.yaml

build-stackstorm-image/file/packs/test/actions/workflows/5.install_docker_ce.yaml
```shell
.
├── Dockerfile
├── file
│   ├── ansible.tar.gz
│   ├── ansible-file
│   ├── packs
│   │   ├── ansible_core
│   │   └── test
│   │       ├── actions
│   │       │   ├── 5.install_docker_ce.yaml    #此文件说明   
│   │       │   ├── shell
│   │       │   └── workflows
│   │       │       └── 5.install_docker_ce.yaml    #此文件说明
│   │       ├── rules
│   │       ├── icon.png
│   │       └── pack.yaml
│   └── python-tests-file
└── README.md
```
build-stackstorm-image/file/packs/test/actions/5.install_docker_ce.yaml文件为模块文件，对比见图11
```shell
---
name: 5.install_docker_ce   #模块名称，与文件名相同
description: 用ansible在指定宿主机内安装docker-ce最新版本和docker-compose，需要目标主机连外网    #模块说明
runner_type: orquesta    #模块类型，orquesta为调用yaml或json文件
entry_point: workflows/5.install_docker_ce.yaml    #调用的文件位置
enabled: true
parameters:    #输入框
  docker_compose_download_url:    #输入框名称
    description: "docker_compose网络下载url，不填使用默认地址"    #输入框说明文字
    default: "http://liyulei.f3322.net:8081/repository/miscs/docker/docker-compose"    #默认带入值
    type: string    #输入框内填写的文字类型
    required: true   #输入框是否比填
    position: 0    #输入框内填写后的默认变量是$0
```

（图11）
![Image text](https://raw.githubusercontent.com/liyuleizhang/img/main/stackstorm/WX20210425-111148.png)

build-stackstorm-image/file/packs/test/actions/workflows/5.install_docker_ce.yaml脚本文件
```shell
version: 1.0   #版本
description: 用ansible在指定宿主机内安装docker-ce最新版本和docker-compose，需要目标主机连外网   #本脚本说明
input:    #调用build-stackstorm-image/file/packs/test/actions/5.install_docker_ce.yaml下的输入框内容
- docker_compose_download_url    #输入框名称
tasks:    #脚本
  install_docker_ce:    #第一个脚本名称
    action: ansible.playbook    #调用ansible下的playbook模块
    input:    #在分行写的格式下需要调用输入框内容，则在调用输入框内容上层填写input
      playbook: /etc/ansible/playbooks/test/install_docker_ce.yml    #在ansible.playbook下的playbook空内填入的值
      inventory_file: /etc/ansible/stage/test/inventory   #在ansible.playbook下的inventory_file空内填入的值
      extra_vars:   #在ansible.playbook下的extra_vars空内填入的值，如果值比较多，则按照此格式填写
        - docker_compose_download_url="{{ ctx("docker_compose_download_url") }}"    #设置的变量（名称=值），这里调用actions/5.install_docker_ce.yaml文件的docker_compose_download_url输入框
```

actions/5.install_docker_ce.yaml和actions/workflows/5.install_docker_ce.yaml文件关系图如图9

（图12）
![Image text](https://raw.githubusercontent.com/liyuleizhang/img/main/stackstorm/WX20210425-114056.png)

实际例4编写的两个脚本的功能可以在ansible模块下的playbook中的playbook、inventory_file、extra_vars中输入如下内容执行后和例4结果相同，如图13
```shell
ansible模块下的playbook中的playbook输入如下内容
/etc/ansible/playbooks/test/install_docker_ce.yml
ansible模块下的playbook中的inventory_file输入如下内容
/etc/ansible/stage/test/inventory
ansible模块下的playbook中的extra_vars输入如下内容
docker_compose_download_url=http://*******
```
（图13）
![Image text](https://raw.githubusercontent.com/liyuleizhang/img/main/stackstorm/WX20210425-114853.png)

#### 2.4.4 rules规则文件
rules根据规则启动actions脚本文件
文件路径build-stackstorm-image/file/packs/包名称/rules/
web页面位置

![Image text](https://raw.githubusercontent.com/liyuleizhang/img/main/stackstorm/WX20210426-113154.png)
##### 2.4.4.1 例1
build-stackstorm-image/file/packs/test/rules/1.timing_task.yaml

```shell
.
├── Dockerfile
├── file
│   ├── ansible.tar.gz
│   ├── ansible-file
│   ├── packs
│   │   ├── ansible_core
│   │   └── test
│   │       ├── actions
│   │       ├── rules
│   │       │   └── 1.timing_task.yaml    #此文件说明
│   │       ├── icon.png
│   │       └── pack.yaml
│   └── python-tests-file
└── README.md
```
build-stackstorm-image/file/packs/test/rules/1.timing_task.yaml规则脚本，对比见图14
```shell
---
name: 1.timing_task    #名称
description: 每日早8点定时执行test模块下6.test_hello任务       #本脚本说明
enabled: false    #是否开启脚本
trigger:    #使用的触发器
  type: core.st2.CronTimer    #触发器名称
  parameters:    #输入栏，year年、month月、day日、hour小时24进制、minute分、second秒
    second: "0"
    minute: "0"
    hour: "8"
action:    #执行的任务
  ref: test.6.test_hello
    parameters:    #输入框
        name: Yo    #name输入框内容输入Yo
```
说明当触发器core.st2.CronTimer时间到每天8点时，执行test.6.test_hello任务

（图14）
![Image text](https://raw.githubusercontent.com/liyuleizhang/img/main/stackstorm/WX20210426-122021.png)

也可在web页面建立规则，在RULES页面单击做下角的加号，如图15

（图15）
![Image text](https://raw.githubusercontent.com/liyuleizhang/img/main/stackstorm/WX20210426-125112.png)

填入相应内容，单击CREATE创建，与配置文件关系图如下，如16

（图16）
![Image text](https://raw.githubusercontent.com/liyuleizhang/img/main/stackstorm/WX20210426-124923.png)

创建完成如图17
![Image text](https://raw.githubusercontent.com/liyuleizhang/img/main/stackstorm/WX20210426-125443.png)


