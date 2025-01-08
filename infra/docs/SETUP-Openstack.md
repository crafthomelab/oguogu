## 오픈스택 설치 순서

### 언어 설정
````
# /etc/enviornment
LANG=en_US.utf-8
LC_ALL=en_US.utf-8
````

### 방화벽 끄기
오픈스택 내 자체 방화벽을 활용하기 위함입니다. 끄지 않은 경우, 충돌로 인해 정상적으로 동작하지 않는 사례가 많이 보고되었다고 함
````bash
sudo systemctl status firewalld
sudo systemctl stop firewalld
sudo systemctl disable firewalld
````

### 네트워크 매니저 끄기
OpenStack은 자체적인 네트워크 관리 도구인 Neutron을 활용해 네트워크 제어. 충돌 방지를 위함
````bash
sudo systemctl stop NetworkManager
sudo systemctl disable NetworkManager
````

그리고 network-scripts로 변경합니다. 

````bash
sudo dnf install network-scripts --enablerepo=devel
sudo systemctl enable network
sudo systemctl start network
````

추가로 네트워크 설정을 위해, 이더넷 디바이스 이름 확인을 아래를 통해 확인합니다.

````bash
ip address show # get the name of Ethernet device  (enp2s0로 되어 있음)
````

아래 경로로 이동해서 파일을 수정합니다.
````bash
# /etc/sysconfig/network-scripts/ifcfg-enp2s0

TYPE=Ethernet
BOOTPROTO=none
NAME=enp2s0
DEVICE=enp2s0 # 이더넷 디바이스 이름 조회
ONBOOT=yes
IPADDR=192.168.1.100    # 원하는 IP 주소로 변경
PREFIX=24                       # 서브넷 마스크에 해당하는 프리픽스 길이
GATEWAY=192.168.1.1     # 게이트웨이 주소 (여기서 중요한건 내부망 게이트웨이로 박아야 함. ISP의 게이트웨이로 박으면 안됨)
DNS1=8.8.8.8                   # DNS 서버 주소
````

network-scripts를 재시동합니다.

````bash
sudo systemctl restart network
````

외부 접근 가능한지 ping으로 확인합니다.

````bash
ping 8.8.8.8
````

### SELINUX 끄기 

SELinux(Security-Enhanced Linux)는 시스템 보안을 강화하기 위한 강력한 접근 제어 메커니즘입니다. 그러나 OpenStack과 같은 복잡한 소프트웨어 스택을 설치하고 구성할 때, SELinux의 보안 정책이 일부 서비스나 기능의 동작을 방해하거나 예기치 않은 문제를 일으킬 수 있습니다.

````bash
# /etc/selinux/config
SELINUX=disabled
````

이후 reboot를 진행합니다. 

````bash
reboot
````

정상적으로 되었다면

````
getenforce
````
하면 disabled 나와야합니다. 

### 오픈스택 설치하기

모든 노드 별로 아래 명령어를 실행합니다. 

````
sudo dnf install -y centos-release-openstack-dalmatian
sudo dnf install -y dnf-utils
sudo dnf config-manager —set-enabled centos-openstack-dalmatian
sudo dnf update -y

# rocky linux에서는 powertools 대체제
sudo dnf config-manager --enable crb 
sudo dnf install -y python3-pyxattr

# PACKSTACK 설치하기
sudo dnf install -y openstack-packstack
````

팩스택 설정 파일을 생성합니다. 이것은 노드 중 하나에서만 실행하면 됩니다.
````
packstack --gen-answer-file=answer.txt
````

여기서 수정해주어야 하는 것들은 아래와 같습니다. 

````
CONFIG_CEILOMETER_INSTALL=n
CONFIG_AODH_INSTALL=n

# 컨트롤러 노드 구성
CONFIG_CONTROLLER_HOST=컨트롤러_노드_IP
CONFIG_COMPUTE_HOSTS=컴퓨트_노드1_IP,컴퓨트_노드2_IP
CONFIG_NETWORK_HOSTS=네트워크_노드_IP

#openvswitch 사용을 위한 소프트웨어 설치
CONFIG_NEUTRON_ML2_MECHANISM_DRIVERS=openvswitch

# L2는 가상의 스위치
CONFIG_NEUTRON_L2_AGENT=openvswitch

# VXLAN와 FLAT은 각각 내외부 네트워크
CONFIG_NEUTRON_ML2_TYPE_DRIVERS=vxlan,flat

# tenant, 가입자들이 이용할 네트워크 정의
CONFIG_NEUTRON_ML2_TENANT_NETWORK_TYPES=vxlan

# flat을 설정할 때 외부 인터페이스
CONFIG_NEUTRON_OVS_BRIDGE_MAPPINGS=extnet:br-ex

# enp2s0은 진짜 랜카드. br-ex(가상의 랜카드)가 enp2s0 인터페이스 랜카드의 ip를 뺏어가서 처리. 
# 실제 랜카드는 전기신호만 오가는 존재가 됨
# floating IP가 외부와 연결되기 위해서 br-ex가 IP를 가져가게 되는 것.
CONFIG_NEUTRON_OVS_BRIDGE_IFACES=br-ex:enp2s0 
CONFIG_PROVISION_DEMO=n
````

이거 후에 아래를 호출해주면 전부다 설치됩니다.

````
packstack --answer-file=answer.txt
````

네트워크 만들기

````
openstack network create external_network --provider-network-type flat --provider-physical-network extnet --external
````