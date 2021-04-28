# coding: utf-8
import pytest


@pytest.mark.parametrize('container_name', ['zoo'])
def test_container_running(host, container_name):
    c = host.docker(container_name)
    # 判断容器状态是否为 running
    assert c.is_running
    # 判断容器健康状态是否为 healthy
    assert c.inspect()['State']['Health']['Status'] == 'healthy'


# @pytest.mark.parametrize('port', [3888])
# def test_service(host, port):
#     ip = host.ansible("setup")['ansible_facts']['ansible_default_ipv4']['address']
#     assert host.socket("tcp://%s:%d" % (ip, port)).is_listening
