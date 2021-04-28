# coding: utf-8
import pytest
import requests


@pytest.mark.parametrize('container_name', [
    'hubble-broker-api',
    'hubble-broker-dataset',
    'hubble-broker-parents',
    'hubble-tokenserver',
    'hubble-broker-sandbox',
    'hubble-broker-file',
])
def test_container_running(host, container_name):
    c = host.docker(container_name)
    # 判断容器状态是否为running
    assert c.is_running
    # 判断容器健康状态是否为healthy
    assert c.inspect()['State']['Health']['Status'] == 'healthy'


@pytest.mark.parametrize('port', [9991, 9996, 16112, 16211, 16212, 16213])
def test_port(host, port):
    # 判断端口是否处于监听状态
    assert host.socket('tcp://%d' % port).is_listening or host.socket('tcp://:::%d' % port).is_listening
