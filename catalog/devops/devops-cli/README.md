# Overview

Using the [Dockerfile](Dockerfile) in this directory, you 
can build a self-contained DevOps command-line environment (dubbed `devops-cli`),
replete with many of the tools needed for managing
a modern technology stack.

Of note are the following:
- ansible
- aws cli
- docker-in-docker (DinD)
- python 
- terraform
- zsh

# Building the Image

To be done before you bring up the project or build the image:

- Create a new set of ssh keys: `ssh-keygen -f ./id_rsa -t rsa -N ''`
- Add the newly-generated ssh public key to your [authorized_keys](authorized_keys) file:<br />
  `cat id_rsa.pub >> authorized_keys`
- Create your container's HISTORY file: `touch $HOME/.zsh_history_devops-cli`

## Via docker-compose

Simply run `docker-compose up -d --build`

# Connecting to the devops-cli container

## Via docker exec

Run `docker exec -it devops-cli zsh -l`

## Via SSH

As per the [docker-compose.yaml](docker-compose.yaml) file,
the ssh daemon process on the container is exposed via port `2222`.

To connect via ssh, run: `ssh -i ./id_rsa devops@localhost -p 2222`
