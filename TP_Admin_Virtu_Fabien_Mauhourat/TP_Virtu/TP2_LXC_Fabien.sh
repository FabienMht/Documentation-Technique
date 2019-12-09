#!/usr/bin/env bash
# Fabien MAUHOURAT
LXC_CONTAINER_PATH="/var/lib/lxc"
LXC_NETWORK=""
LXC_NETWORK_CONTAINER="eth0"
LXC_NETWORK_DEFAULT="lxcbr0"
LXC_CONTAINER_NAME=""
LXC_NETWORK_TYPE="veth"

echo "----------- Debut du script -------------"

if [[ "$EUID" -ne 0 ]]; then 
  echo "Become Root !!!!"
  exit 1
fi

while [[ "$1" != "" ]];
do
  case "$1" in
    --name | -n )       LXC_CONTAINER_NAME=$2
                        shift;;
    --network | -net )  LXC_NETWORK_TYPE=$2
                        shift;;
    --interface | -i )  LXC_NETWORK=$2
                        shift;;
    * )                 echo "\n Parametre $1 non disponible !"
                        exit 1
  esac
  shift
done

if [[ $(lxc-info -n $LXC_CONTAINER_NAME 2>/dev/null) ]]; then
  echo "Le container $LXC_CONTAINER_NAME existe deja"
  exit 1
fi

if [[ "$LXC_NETWORK_TYPE" == ""  ]]; then
  echo "Specifier un type de reseau : phys ou veth !"
  exit 1
fi

echo "Création du container"
lxc-create -n $LXC_CONTAINER_NAME -t download -- -d ubuntu -r bionic -a amd64 > /dev/null 2>&1
if [[ $? -gt 0 ]]; then
  echo "Erreur lors de la création du container $LXC_CONTAINER_NAME"
  exit 1
fi

echo -e "lxc.cgroup.cpuset.cpus = 0\nlxc.cgroup.memory.limit_in_bytes = 256000000" >> $LXC_CONTAINER_PATH/$LXC_CONTAINER_NAME/config

if [[ "$LXC_NETWORK_TYPE" == "phys" ]]; then
  if [[ "$LXC_NETWORK" == "" ]]; then
    echo "Specifier une interface !"
    exit 1
  fi
  sed -i "s/eth0/$LXC_NETWORK/g" $LXC_CONTAINER_PATH/$LXC_CONTAINER_NAME/rootfs/etc/netplan/10-lxc.yaml
  LXC_NETWORK_CONTAINER=$LXC_NETWORK
else
  if [[ "$LXC_NETWORK" == "" ]]; then
    LXC_NETWORK=$LXC_NETWORK_DEFAULT
  fi
fi

ip link | grep $LXC_NETWORK > /dev/null
if [[ $? -gt 0 ]]; then
  echo "L interface $LXC_NETWORK n existe pas"
  exit 1
fi

sed -i "/lxc.net.0.type/s/^.*$/lxc.net.0.type = $LXC_NETWORK_TYPE/" $LXC_CONTAINER_PATH/$LXC_CONTAINER_NAME/config
sed -i "/lxc.net.0.link/s/^.*$/lxc.net.0.link = $LXC_NETWORK/" $LXC_CONTAINER_PATH/$LXC_CONTAINER_NAME/config

echo "Démarrage du container"
lxc-start -n $LXC_CONTAINER_NAME
if [[ $? -gt 0 ]]; then
  echo "Erreur lors du démarrage du container $LXC_CONTAINER_NAME"
  exit 1
fi

while :; do
  lxc-attach -n $LXC_CONTAINER_NAME -- /bin/bash -c "ip a | grep $LXC_NETWORK_CONTAINER | grep inet" > /dev/null 2>&1
  if [[ $? -eq 0 ]]; then
    break
  fi
  sleep 1
done

echo "Installation d'apache sur le container"
lxc-attach -n $LXC_CONTAINER_NAME -- /bin/bash -c "apt update && apt -y install apache2 && systemctl start apache2 && systemctl enable apache2" > /dev/null 2>&1
if [[ $? -gt 0 ]]; then
  echo "Erreur lors de l'installation d'apache sur le container $LXC_CONTAINER_NAME"
  exit 1
fi

echo "----------- Script terminé avec succes -----------"
