export PATH=$PATH:/usr/local/bin

yum -y install python3-pip git python3 gcc
pip3 install centrify.dmc
curl -o /tmp/gh_1.6.2_linux_386.rpm -L https://github.com/cli/cli/releases/download/v1.6.2/gh_1.6.2_linux_386.rpm && cd /tmp
rpm -i gh_1.6.2_linux_386.rpm
cd /usr/local/bin

gh auth login
gh repo clone KevSmithCentrify/dmc-python

cd /tmp
curl -o sshpass-1.08.tar.gz -L https://sourceforge.net/projects/sshpass/files/sshpass/1.08/sshpass-1.08.tar.gz/download
tar zxvf sshpass-1.08.tar.gz
cd sshpass-1.08
./configure
make install

cd /usr/local/bin
curl -o ccli.gz -L https://github.com/centrify/centrifycli/releases/download/v1.0.6.0/ccli-v1.0.6.0-linux.gz
gunzip  ccli.gz

curl -o jq -L https://github.com/stedolan/jq/releases/download/jq-1.6/jq-linux64

chmod 750 ccli && chmod 755 jq

ccli -url https://ztp.my-kibble.centrify.com saveConfig
ccli /sysinfo/version
#ccli /Redrock/query -s -m -ms sql -j "{ 'SCRIPT': 'SELECT ID,FQDN,NAME from Server where NAME like \'%i-%\'' }" | jq -r '.Result.Results[] .Row | .Name + ":" + .FQDN'

cd /usr/local/bin/dmc-python
curl -o cgetsecret.py -L https://raw.githubusercontent.com/KevSmithCentrify/dmc-python/master/cgetsecret.py
chmod 750 /usr/local/bin/dmc-python/cgetsecret.py

curl -o pullwebcode.sh -L https://raw.githubusercontent.com/KevSmithCentrify/dmc-python/master/pullwebcode.sh
chmod 750 /usr/local/bin/dmc-python/pullwebcode.sh
