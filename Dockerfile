FROM mcr.microsoft.com/azure-cli
WORKDIR /home/operations
ENV ANSIBLE_HOST_KEY_CHECKING False
RUN apk update && apk add unzip ansible wget jq
RUN wget https://releases.hashicorp.com/terraform/0.11.13/terraform_0.11.13_linux_amd64.zip && unzip \
    terraform_0.11.13_linux_amd64.zip && mv terraform /usr/local/bin/ && rm -rf terraform_0.11.13_linux_amd64.zip
RUN mkdir ssh
COPY . .
RUN cd terraform; terraform init
RUN cd /home/operations/orchestrator; pip install -r requirements.txt
ENTRYPOINT [ "/bin/sh" ]