OS_ACTUAL=$(uname)-$(whoami)
OS_TOBE=Linux-ubuntu
echo OS_ACTUAL is $OS_ACTUAL and should be $OS_TOBE
[ "$OS_ACTUAL" != "$OS_TOBE" ] && exit 105
echo good - OS_ACTUAL is as expected

if [ 1 -eq 1 ]
then
        echo step 1 - begin - update all packages
        sudo apt-get update
        echo step 1 - end
fi
if [ 2 -eq 2 ]
then
        echo step 2 - begin - install and start the docker service
        sudo apt-get install docker.io -y
        echo step 2 - end
fi
if [ 3 -eq 3 ]
then
        echo step 3 - begin - docker test run: we generate a mini awk program and we run it using the awk inside busybox
        AWKZ=/tmp/minitest.awk
        echo 'BEGIN{print "hi from awk"}' > $AWKZ
        sudo docker run -v /tmp:/tmp999 busybox awk -f /tmp999/minitest.awk
        echo step 3 - end
fi
if [ 4 -eq 4 ]
then
        echo step 4 - begin - install python pip and then aws cli
        sudo apt-get -y install python3-pip        
        pip -V
        # ko: python3 -m pip install awscliv2
        # ko: sudo apt install python-awscliv2
        # hint: https://stackoverflow.com/questions/75608323/how-do-i-solve-error-externally-managed-environment-every-time-i-use-pip-3
        # sudo apt -y install pipx
        # ko: pipx install awscliv2
        # ko: pipx install python3-awscliv2
        # just follow: https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html
        # not needed ... sudo apt install -y unzip curl
        
fi
        

