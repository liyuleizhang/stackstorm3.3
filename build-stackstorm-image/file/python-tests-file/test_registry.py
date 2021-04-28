# coding: utf-8
import pytest
import requests


@pytest.mark.parametrize('path', ['/data', '/data/blobs'])
def test_nexus_data_exists(host, path):
    # 判断文件是否存在
    assert host.file(path).exists


@pytest.mark.parametrize('container_name', ['nexus'])
def test_container_running(host, container_name):
    c = host.docker(container_name)
    # 判断容器状态是否为 running
    assert c.is_running
    # 判断容器健康状态是否为 healthy
    assert c.inspect()['State']['Health']['Status'] == 'healthy'


@pytest.mark.parametrize('port', [80, 8001, 8002, 8081])
def test_service(host, port):
    ipv4_address = host.ansible.get_variables()['ansible_host']
    resp = requests.get('http://%s:%d' % (ipv4_address, port))
    # 判断页面返回HTTP状态码是否在200, 400, 401, 403之中
    assert resp.status_code in [200, 400, 401, 403]
