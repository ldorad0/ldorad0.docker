# syntax=docker/dockerfile:1
FROM --platform=linux/amd64 python:3.10.6
ENV DEBIAN_FRONTEND=noninteractive
ENV SETUP_HOME=/setup

RUN apt -y update

RUN echo "===> Installing sudo to emulate normal OS behavior..."  &&\
rm -f /etc/sudoers && apt -y install sudo

RUN echo "===> Adjusting sudoers rules ..."  &&\
echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers.d/default

RUN echo "===> Installing system packages ..."  &&\
apt -y install \
curl \
wget \
gettext-base \
unzip \
grep \
gcc \
jq \
dos2unix \
iputils-ping \
sshpass \
openssh-client \
openssh-server \
rsync \
bash \
mkisofs \
dnsutils \
html2text \
git \
smbclient \
socat \
screen \
wget \
unzip \
sudo \
gnupg \
vim \
ca-certificates \
gnupg \
less \
screen \
apt-transport-https \
iproute2 \
kmod \
python3-libvirt \
pkg-config \
libvirt-dev \
lsof \
net-tools \
zsh

ARG DOCKER_VER=24.0
ARG BUILDX_VER=v0.10.5
RUN echo "===> Installing docker ..."  &&\
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add - &&\
echo "deb [arch=amd64] https://download.docker.com/linux/ubuntu focal stable" > /etc/apt/sources.list.d/docker.list &&\
apt-get update &&\
apt-get install -y docker-ce &&\
apt-get purge -y docker-ce-rootless-extras docker-scan-plugin &&\
apt-get autoremove -y &&\
rm -rf /var/lib/apt/lists/* &&\
curl -fsSL -o /tmp/docker-buildx "https://github.com/docker/buildx/releases/download/${BUILDX_VER}/buildx-${BUILDX_VER}.linux-amd64" &&\
chmod +x /tmp/docker-buildx &&\
mv /tmp/docker-buildx /usr/libexec/docker/cli-plugins/docker-buildx

RUN pip3 install --upgrade pip setuptools wheel

ENV CRYPTOGRAPHY_DONT_BUILD_RUST=1

WORKDIR $SETUP_HOME

ENV USER=devops
ENV GROUP=devops
ENV USERHOME=/home/$USER
# HISTDIR: directory where we store $HISTFILE
ENV USER_PYTHON_LOCAL=/opt/python/.local
ENV OPT_PYTHON=/opt/python/site-packages
ENV OPT_PYTHON_BIN=${OPT_PYTHON}/bin
ENV PATH="${OPT_PYTHON_BIN}:${PATH}"
ARG UID=5000
ARG GID=5000
ENV UID=$UID
ENV GID=$GID

RUN pip install pyyaml==5.4.1 --no-cache-dir --no-build-isolation

ADD requirements.txt .

RUN echo "===> Installing Ansible and Related Packages ..."  &&\
pip3 install \
-r requirements.txt

ADD requirements.extras.txt .

RUN echo "===> Installing extra python packages ..."  &&\
pip3 install \
-U -r requirements.extras.txt

RUN chmod -R 777 /usr/local/lib/python3.10/site-packages

RUN echo "===> Creating service user ..."  &&\
useradd -m -s /bin/zsh -G sudo,docker --uid "$UID" "$USER"

RUN chown -R $USER:$GROUP /opt

# Test sudo
RUN sudo ls

RUN ln -s $(which python3) /usr/bin/python

# awscli
ENV AWSCLI_VERSION=2.7.16
RUN curl -ksL https://awscli.amazonaws.com/awscli-exe-linux-x86_64-${AWSCLI_VERSION}.zip -o awscliv2.zip \
    && unzip awscliv2.zip \
    && aws/install \
    && rm -rf \
        awscliv2.zip \
        aws \
        /usr/local/aws-cli/v2/current/dist/aws_completer \
        /usr/local/aws-cli/v2/current/dist/awscli/data/ac.index \
        /usr/local/aws-cli/v2/current/dist/awscli/examples

RUN find /usr/local/aws-cli/v2/current/dist/awscli/botocore/data -name examples-1.json -delete

# aws iam authenticator
# https://docs.aws.amazon.com/eks/latest/userguide/install-aws-iam-authenticator.html https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ECS_CLI_installation.html
RUN curl -ksS -o /usr/bin/aws-iam-authenticator https://amazon-eks.s3.us-west-2.amazonaws.com/1.16.8/2020-04-16/bin/linux/amd64/aws-iam-authenticator \
    && curl -ksS -o /usr/bin/ecs-cli https://s3.amazonaws.com/amazon-ecs-cli/ecs-cli-linux-amd64-latest \
    && curl -ksS -L https://github.com/weaveworks/eksctl/releases/latest/download/eksctl_Linux_amd64.tar.gz | sudo tar xz -C /usr/bin \
    && sudo chmod +x /usr/bin/aws-iam-authenticator /usr/bin/ecs-cli /usr/bin/eksctl

# aws session manager plugin
RUN curl -O "https://s3.amazonaws.com/session-manager-downloads/plugin/latest/ubuntu_64bit/session-manager-plugin.deb" &&\
sudo dpkg -i session-manager-plugin.deb

## kubectl
## https://kubernetes.io/releases/
ENV KUBECTL_VERSION=v1.23.0
RUN curl -kLO https://storage.googleapis.com/kubernetes-release/release/$KUBECTL_VERSION/bin/linux/amd64/kubectl
RUN chmod +x kubectl && mv kubectl /bin/kubectl

## kind
ENV KIND_VERSION=v0.14.0
RUN set -exu \
  && curl -kfLo ./kind-linux-amd64 "https://github.com/kubernetes-sigs/kind/releases/download/${KIND_VERSION}/kind-linux-amd64" \
  && chmod +x ./kind-linux-amd64 \
  && mv ./kind-linux-amd64 /usr/local/bin/kind

## helm
## https://kubernetes.io/releases/
ENV HELM_VERSION=v3.9.2
RUN curl -kfsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/master/scripts/get-helm-3 \
    && chmod +x get_helm.sh && DESIRED_VERSION=$HELM_VERSION ./get_helm.sh

## terraform
ENV TERRAFORM_VERSION=1.3.7
RUN curl -O https://releases.hashicorp.com/terraform/${TERRAFORM_VERSION}/terraform_${TERRAFORM_VERSION}_linux_amd64.zip && \
    unzip terraform_${TERRAFORM_VERSION}_linux_amd64.zip -d /usr/bin
# ARG TERRAFORM_PROVIDER_VERSION=0.6.2
# ARG TERRAFORM_PROVIDER_RELEASE=0.6.2+git.1585292411.8cbe9ad0
# RUN mkdir -p ~/.terraform.d/plugins/linux_amd64 &&\
#     curl -L -o terraform-provider-libvirt.tar.gz \
#     https://github.com/dmacvicar/terraform-provider-libvirt/releases/download/v${TERRAFORM_PROVIDER_VERSION}/terraform-provider-libvirt-${TERRAFORM_PROVIDER_RELEASE}.Ubuntu_18.04.amd64.tar.gz &&\
#     tar zxvf terraform-provider-libvirt.tar.gz &&\
#     mv terraform-provider-libvirt ~/.terraform.d/plugins/linux_amd64/ &&\
#     rm -rf terraform*

## packer
ENV PACKER_VERSION=1.1.0
RUN echo 'Installing packer ...' \
&& curl -O -L https://releases.hashicorp.com/packer/${PACKER_VERSION}/packer_${PACKER_VERSION}_linux_amd64.zip \
&& unzip packer_${PACKER_VERSION}_linux_amd64.zip -d /usr/bin

## go ## golang
RUN git -c http.sslVerify=false clone https://github.com/syndbg/goenv.git $HOME/.goenv
ENV GOENV_DISABLE_GOPATH=1
ENV GOPATH="/go"
ARG GO_VERSION=1.19.1
ENV GO_VERSION=${GO_VERSION}
RUN wget -P /tmp "https://dl.google.com/go/go${GO_VERSION}.linux-amd64.tar.gz"
RUN tar -C /usr/local -xzf "/tmp/go${GO_VERSION}.linux-amd64.tar.gz"
RUN rm "/tmp/go${GO_VERSION}.linux-amd64.tar.gz"
RUN mkdir -p "$GOPATH/src" "$GOPATH/bin" && chmod -R 777 "$GOPATH"

RUN apt update

# Bitwarden cli
RUN apt install -y libsecret-1-0
# RUN export VER=$(curl -H "Accept: application/vnd.github+json" https://api.github.com/repos/bitwarden/clients/releases | jq  -r 'sort_by(.published_at) | reverse | .[].name | select( index("CLI") )' | sed 's:.*CLI v::' | head -n 1) && \
ENV BW_VER=2023.4.0
RUN curl -LO "https://github.com/bitwarden/clients/releases/download/cli-v${BW_VER}/bw-linux-${BW_VER}.zip"
RUN unzip bw*.zip &&\
chmod +x ./bw &&\
sudo mv bw /usr/local/bin

ENV VERSION=v1.5.3
RUN curl -LO https://github.com/rancher/rke/releases/download/$VERSION/rke_linux-amd64 &&\
chmod +x ./rke_linux-amd64 &&\
sudo mv ./rke_linux-amd64 /usr/local/bin/rke

# cloud-nuke (temp disable upgrading again)
ENV CLOUD_NUKE_VERSION 0.29.4
ENV CLOUD_NUKE_URL https://github.com/gruntwork-io/cloud-nuke/releases/download/v${CLOUD_NUKE_VERSION}
ENV CLOUD_NUKE_FILENAME cloud-nuke_linux_amd64
ENV CLOUD_NUKE_SHA256 3e86b655591571e1ebcb8faea3897fbc2136215b1620376e04dbb7d267fe2180

RUN wget $CLOUD_NUKE_URL/$CLOUD_NUKE_FILENAME \
  && echo "$CLOUD_NUKE_SHA256  ./$CLOUD_NUKE_FILENAME" | sha256sum -c - \
  && chmod +x ./${CLOUD_NUKE_FILENAME} \
  && sudo mv ./${CLOUD_NUKE_FILENAME} /usr/local/bin/cloud-nuke

RUN echo "===> Adding ssh keys for service user"  &&\
sudo su - $USER -c "mkdir -p $USERHOME/.ssh"

RUN echo "===> Cleaning up ..."  &&\
rm -rf $SETUP_HOME && apt-get clean

# Graphiz
RUN apt install -y graphviz

# Set the container user
USER $USER

# Set the working directory
WORKDIR $USERHOME

RUN mkdir ~/.kube

# ansible collections

RUN ansible-galaxy collection install \
amazon.aws \
ansible.posix \
ansible.windows \
chocolatey.chocolatey \
ansible.netcommon \
community.aws \
community.general \
community.docker \
community.libvirt \
community.windows \
infoblox.nios_modules \
kubernetes.core \
ovirt.ovirt \
recordsansible.ara

# node version manager
ENV NVM_VERSION=v0.39.5
RUN curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/${NVM_VERSION}/install.sh | bash

RUN echo "===> Adding bash profile, et al, for service user"
COPY --chown=$USER:$GROUP .bash_profile $USERHOME
COPY --chown=$USER:$GROUP .bashrc $USERHOME
COPY --chown=$USER:$GROUP .inputrc $USERHOME

RUN echo "===> Adding ssh keys, et al, for service user"
COPY --chown=$USER:$GROUP authorized_keys* $USERHOME/.ssh
COPY --chown=$USER:$GROUP known_hosts $USERHOME/.ssh
COPY --chown=$USER:$GROUP id_rsa* $USERHOME/.ssh/
COPY --chown=$USER:$GROUP ssh.config $USERHOME/.ssh/config

RUN echo "===> Adjusting permissions for ssh keys"
RUN <<EOF /bin/bash
  chmod 700 $USERHOME/.ssh
  if [[ -f .ssh/authorized_keys ]];then
  chmod 644 $USERHOME/.ssh/authorized_keys
  fi &&\
  if [[ -f $USERHOME/.ssh/known_hosts ]];then
  chmod 644 $USERHOME/.ssh/known_hosts
  fi &&\
  if [[ -f $USERHOME/.ssh/config ]];then
  chmod 644 $USERHOME/.ssh/config
  fi &&\
  if [[ -f $USERHOME/.ssh/id_rsa ]];then
  chmod 600 $USERHOME/.ssh/id_rsa
  fi &&\
  if [[ -f $USERHOME/.ssh/id_rsa.pub ]];then
  chmod 644 $USERHOME/.ssh/id_rsa.pub
  fi
EOF

# Add more support files
RUN sudo mkdir /etc/ansible
ADD ansible.cfg /etc/ansible/

RUN echo "===> Adding default aws cli config file"
ADD .aws/config $USERHOME/.aws/config

RUN sudo chown -R $USER:$GROUP $USERHOME/.aws

# SSH login fix. Otherwise user is kicked off after login
RUN sudo mkdir /var/run/sshd &&\
sudo sed 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' -i /etc/pam.d/sshd

#allow services to start automatically from this point
#https://askubuntu.com/questions/365911/why-the-services-do-not-start-at-installation
RUN printf '#!/bin/sh\nexit 0\n' | sudo tee /usr/sbin/policy-rc.d

# Install OH MY ZSH
RUN sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
# Tell oh-my-zsh to ignore untracked git files
# see https://stackoverflow.com/questions/12765344/oh-my-zsh-slow-but-only-for-certain-git-repo
# see https://github.com/ohmyzsh/ohmyzsh/issues/5327
RUN git config --global --add oh-my-zsh.hide-dirty 1

COPY --chown=$USER:$GROUP .zshrc $USERHOME

ADD entrypoint.sh /usr/local/bin

ENV DOCKER_HOST_PORT=2375
ENV DOCKER_HOST=127.0.0.1:$DOCKER_HOST_PORT
RUN sudo chmod +x /usr/local/bin/entrypoint.sh

EXPOSE 22
EXPOSE 5555

ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
