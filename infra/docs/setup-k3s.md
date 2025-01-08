## K3S 설치

### 1. K3S 설치



### 2. 주요 HELM 설치

#### 2.1. Sealed Secrets: secret.yaml을 암호화해주는 도구. 

암호화된 채로 k8s에 적용하면, k8s 내에서 복호화해서 이용하기 때문에, 암호화된 sealed secrets을 버전 관리에서 활용할 수 있음.

````shell
helm install sealed-secrets -n kube-system sealed-secrets/sealed-secrets
````

````shell
KUBESEAL_VERSION='0.23.0' # Set this to, for example, KUBESEAL_VERSION='0.23.0'
curl -OL "https://github.com/bitnami-labs/sealed-secrets/releases/download/v${KUBESEAL_VERSION:?}/kubeseal-${KUBESEAL_VERSION:?}-linux-amd64.tar.gz"
tar -xvzf kubeseal-${KUBESEAL_VERSION:?}-linux-amd64.tar.gz kubeseal
sudo install -m 755 kubeseal /usr/local/bin/kubeseal
````