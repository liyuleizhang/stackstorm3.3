# coding: utf-8
import pytest


# @pytest.mark.os
# @pytest.mark.origin_os
# @pytest.mark.parametrize('version', ['CentOS Linux release 7.7'])
# def test_os_release(host, version):
#     # 判断操作系统版本
#     assert host.file('/etc/redhat-release').contains(version)


@pytest.mark.os
@pytest.mark.origin_os
@pytest.mark.parametrize('version', ['3.10'])
def test_kernel_version(host, version):
    cmd = host.run('uname -sr')
    # 判断内核版本
    assert version in cmd.stdout
    assert cmd.rc == 0


@pytest.mark.origin_os
@pytest.mark.parametrize('name', ['sshd'])
def test_origin_services_running_and_enabled(host, name):
    service = host.service(name)
    # 判断systemd sercie状态是否为running
    assert service.is_running
    # 判断systemd service是否为开机自启动
    assert service.is_enabled


@pytest.mark.os
@pytest.mark.parametrize('name', ['docker'])
def test_services_running_and_enabled(host, name):
    service = host.service(name)
    # 判断systemd sercie状态是否为running
    assert service.is_running
    # 判断systemd service是否为开机自启动
    assert service.is_enabled


@pytest.mark.os
@pytest.mark.parametrize('version', ['1.25'])
def test_docker_compose_version(host, version):
    cmd = host.run('docker-compose version')
    # 判断docker-compose版本
    assert version in cmd.stdout
    assert cmd.rc == 0


@pytest.mark.os
@pytest.mark.parametrize('name', ['firewalld'])
def test_services_stopped_and_disabled(host, name):
    service = host.service(name)
    # 判断systemd sercie状态是否为停止
    assert not service.is_running
    # 判断systemd service是否为开机不自启动
    assert not service.is_enabled


@pytest.mark.os
@pytest.mark.parametrize('remote_host', ['registry'])
def test_connection(host, remote_host):
    remote = host.addr(remote_host)
    # 判断节点是否能够节点指定地址
    assert remote.is_resolvable
    # 判断节点是否能否访问指定地址
    assert remote.is_reachable
