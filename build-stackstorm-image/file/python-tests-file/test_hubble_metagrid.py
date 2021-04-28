# coding: utf-8
import pytest
import requests


@pytest.mark.parametrize('container_name', [
    'metagrid-mysql-router',
    'hubble-ui',
    'hubble-metagrid-api',
    'hubble-dataquality-runner',
    'hubble-statistics',
])
def test_container_running(host, container_name):
    # 非高可用部署方式，不检查mysql-router状态
    onex_vip = host.ansible.get_variables().get('ONEX_VIP')
    if onex_vip or container_name.find('mysql-router') == -1:
        c = host.docker(container_name)
        # 判断容器状态是否为running
        assert c.is_running
        # 判断容器健康状态是否为healthy
        assert c.inspect()['State']['Health']['Status'] == 'healthy'


@pytest.mark.parametrize('port', [80, 6452, 16009, 16666, 16789])
def test_port(host, port):
    # 非高可用部署方式，不检查mysql-router状态
    onex_vip = host.ansible.get_variables().get('ONEX_VIP')
    if onex_vip or port != 6452:
        # 判断端口是否处于监听状态
        assert host.socket('tcp://%d' % port).is_listening or host.socket('tcp://:::%d' % port).is_listening
