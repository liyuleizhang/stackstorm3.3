# coding: utf-8
import pytest
import requests


@pytest.mark.parametrize('container_name', [
    'whui-all-in-one',
    'statistics-ui',
    'whitehole-statistics',
    'wso2-service-broker',
    'whitehole-event',
    'whitehole-business',
    'statistics-api',
    'whitehole-flow',
    'whitehole-mysql-router',
])
def test_container_running(host, container_name):
    # 非高可用部署方式，不检查mysql-router状态
    onex_vip = host.ansible.get_variables().get('ONEX_VIP')
    if onex_vip or container_name.find('mysql-router') == -1:
        c = host.docker(container_name)
        # 判断容器状态是否为 running
        assert c.is_running
        # 判断容器健康状态是否为 healthy
        assert c.inspect()['State']['Health']['Status'] == 'healthy'


@pytest.mark.parametrize('port', [81, 86, 8086, 8087, 8088, 8089, 8090, 8092])
def test_service(host, port):
    # 判断端口是否处于监听状态
    assert host.socket('tcp://%d' % port).is_listening or host.socket('tcp://:::%d' % port).is_listening
