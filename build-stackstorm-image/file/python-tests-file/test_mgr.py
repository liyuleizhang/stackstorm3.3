# coding: utf-8
import json
import pytest


@pytest.mark.parametrize('container_name', ['mysql'])
def test_container_running(host, container_name):
    c = host.docker(container_name)
    # 判断容器状态是否为running
    assert c.is_running
    # 判断容器健康状态是否为healthy
    assert c.inspect()['State']['Health']['Status'] == 'healthy'


@pytest.mark.parametrize('port', [3306])
def test_port(host, port):
    # 判断端口是否处于监听状态
    assert host.socket("tcp://0.0.0.0:%d" % port).is_listening


def test_mgr(host):
    cmd = host.run('/usr/bin/mysqlsh --file /opt/chinacloud/mysql_mgr/CheckCluster.js')
    # 判断命令是否成功运行
    assert cmd.succeeded

    stdout = json.loads(cmd.stdout)
    # 判断MGR集群是否为OK状态
    assert stdout['defaultReplicaSet']['status'] in ['OK', 'OK_NO_TOLERANCE']

    for instance in stdout['defaultReplicaSet']['topology'].values():
        # 判断MGR节点是否为ONLINE状态
        assert instance['status'] == 'ONLINE'

