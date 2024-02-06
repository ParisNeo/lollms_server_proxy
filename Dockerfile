FROM python:3.11

# install necessary tools into the base image and download git repository
RUN apt update && apt install -y git apache2 && git clone https://github.com/ParisNeo/lollms_server_proxy.git

# change working directory to cloned git repository
WORKDIR lollms_server_proxy

# install all requirements
RUN pip3 install -e .

# copy config.ini and authorized_users.txt into project working directory
COPY config.ini .
COPY authorized_users.txt .

# start the proxy server as entrypoint
ENTRYPOINT ["lollms_server_proxy"]

# set command line parameters
CMD ["--config", "./config.ini", "--users_list", "./authorized_users.txt", "--port", "8080"]
