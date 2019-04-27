FROM hashicorp/terraform:0.11.13
WORKDIR /home/operations
COPY . .
ENTRYPOINT [ "/bin/sh" ]