FROM ubuntu:18.04
WORKDIR /home/operations
ENV ANSIBLE_HOST_KEY_CHECKING False
RUN apt-get update && apt-get install -y unzip software-properties-common wget jq python3 python3-pip
RUN apt-add-repository --yes --update ppa:ansible/ansible && apt-get install -y ansible
RUN wget https://releases.hashicorp.com/terraform/0.11.13/terraform_0.11.13_linux_amd64.zip && unzip \
    terraform_0.11.13_linux_amd64.zip && mv terraform /usr/local/bin/ && rm -rf terraform_0.11.13_linux_amd64.zip
COPY . .
RUN cd terraform; terraform init
RUN cd /home/operations/orchestrator; pip3 install -r requirements.txt
ENTRYPOINT [ "/bin/bash" , "entrypoint.sh"]