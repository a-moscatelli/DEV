
sudo apt update
sudo apt upgrade -y
#sudo apt install python3
sudo apt install python3-pip -y
#sudo apt install python3 python3-pip -y

#docker:
#sudo apt install ca-certificates curl gnupg lsb-release
sudo apt-get install apt-transport-https ca-certificates curl gnupg lsb-release

sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
#curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt update
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
docker -v
systemctl status docker --no-pager -l


#maybe:
#pip install "dask-cloudprovider[aws]" --upgrade
#pip install "dask[distributed]" --upgrade
#pip install --upgrade awscli
#pip install --upgrade botocore
#pip install --upgrade awscli

#pip install notebook
#sudo apt install jupyter-notebook

#aws configure
