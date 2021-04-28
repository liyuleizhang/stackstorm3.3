# coding: utf-8
import pytest
import requests


@pytest.mark.parametrize('container_name', [
    'data-exchange',
])
def test_container_running(host, container_name):
    c = host.docker(container_name)
    # 判断容器状态是否为running
    assert c.is_running
    # 判断容器健康状态是否为healthy
    assert c.inspect()['State']['Health']['Status'] == 'healthy'


@pytest.mark.parametrize('port', [8721])
def test_port(host, port):
    # 判断端口是否处于监听状态
    assert host.socket('tcp://%d' % port).is_listening or host.socket('tcp://:::%d' % port).is_listening
