# coding: utf-8
import pytest
import requests


@pytest.mark.parametrize('container_name', [
    'one-task-scheduler',
    'one-logging-api',
    'one-route',
    'one-infrastructure-api',
    'one-config',
    'portal',
    'keycloak',
    'onex-mysql-router',
    'one-registry',
    'one-ui-all-in-one',
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


@pytest.mark.parametrize('port', [80, 82, 8080, 8081, 8082, 8083, 8084, 8888, 18087])
def test_port(host, port):
    # 判断端口是否处于监听状态
    assert host.socket('tcp://%d' % port).is_listening or host.socket('tcp://:::%d' % port).is_listening
