# coding: utf-8
import pytest
import requests


@pytest.mark.parametrize('container_name', [
    'stargate-mysql-router',
    # 'hubble-neo4j',
    'hubble-dataquality',
    'hubble-ureport',
    'hubble-logstash',
    'hubble-elasticsearch',
    # 'hubble-jobtracker',
    'hubble-datasync',
    'hubble-nifi',
])
def test_container_running(host, container_name):
    # 非高可用部署方式，不检查mysql-router状态
    onex_vip = host.ansible.get_variables().get('ONEX_VIP')
    if onex_vip or container_name.find('mysql-router') == -1:
        c = host.docker(container_name)
        assert c.is_running
        assert c.inspect()['State']['Health']['Status'] == 'healthy'


@pytest.mark.parametrize('port', [5678, 9200, 16083, 16111, 16667])
def test_service(host, port):
    assert host.socket('tcp://%d' % port).is_listening or host.socket('tcp://:::%d' % port).is_listening
