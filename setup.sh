apt update
apt install -y openjdk-8-jdk
apt install -y unzip
wget http://mirror.easyname.ch/apache/nifi/1.9.2/nifi-1.9.2-bin.zip
unzip nifi-1.9.2-bin.zip
apt install -y python3-pip
pip3 install --upgrade pip
apt install -y python3-venv
python3 -m venv venv
source venv/bin/activate
pip3 install aif360
./nifi-1.9.2/bin/nifi.sh start

