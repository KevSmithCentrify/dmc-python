#!/bin/bash

tput clear

PAS_USER=ec2-user
REMOTE_ADDR=lnxaws001
REMOTE_IP=192.168.2.80
REMOTE_APPLICATION="scp"
REMOTE_PAS_RESOURCE_NAME="lnxaws001"
TAG=`date +'%d%m%y@%H%M%S'`
SCP_FILE_DIR=/tmp
SCP_FILE_SRC=$SCP_FILE_DIR/redbank.data
SCP_FILE_DST=/tmp/redbank.data.$TAG
CHECKOUTMINS=1

#echo "{diags} Elevating svcwebadm account to run Centrfy /usr/sbin/cgetaccount as root"

echo -e "{diags} Checking out $PAS_USER vaulted credential for server $REMOTE_ADDR from Centrify Privileged Access Service\n"
PASSWORD=$(/usr/sbin/cgetaccount -t $CHECKOUTMINS -s "$REMOTE_PAS_RESOURCE_NAME/$PAS_USER")

if [ -z "${PASSWORD}" ];
then
        echo -e "${PASSWORD}"
        exit 1
fi

echo "{diags} onetime credential obtained "${PASSWORD}
echo -e "\n{diags} Pulling code from $PAS_USER@$REMOTE_ADDR($REMOTE_IP):$SCP_FILE_SRC"
echo "{diags} Press <ENTER> to continue"
read IGNORE

SCP_HOST=$REMOTE_IP
SCP_USER=$PAS_USER
SCP_PASSWORD=$PASSWORD

rm -f "$SCP_FILE_DST"

if ! /usr/local/bin/sshpass -d 300 scp -o StrictHostKeyChecking=no $SCP_USER@$SCP_HOST:"$SCP_FILE_SRC" "$SCP_FILE_DST" 300<<<"$SCP_PASSWORD" > /tmp/.xfer.$$ 2>&1;
then
        echo -e "{error} scp failed"
        cat /tmp/.xfer.$$
        rm -f /tmp/.xfer.$$
        exit 1
fi

XFER=$(ls $SCP_FILE_DST)
echo -e "{diags} Code release: $XFER created"
