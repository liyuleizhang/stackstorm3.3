# coding: utf-8
import pytest
import requests


@pytest.mark.parametrize('container_name', ['rabbitmq'])
def test_container_running(host, container_name):
    c = host.docker(container_name)
    # 判断容器状态是否为 running
    assert c.is_running
    # 判断容器健康状态是否为 healthy
    assert c.inspect()['State']['Health']['Status'] == 'healthy'


@pytest.mark.parametrize('port', [15672])
def test_rabbitmq_service(host, port):
    # 判断端口是否处于监听状态
    assert host.socket('tcp://%d' % port).is_listening

    ansible_host = host.ansible.get_variables()['ansible_host']
    resp = requests.get('http://%s:%d' % (ansible_host, port))
    # 判断目标页面返回的状态码是否为200
    assert resp.status_code == 200
