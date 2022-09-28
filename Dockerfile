FROM python:latest
ENV PATH="${PATH}:/usr/local/bin"

WORKDIR /app

RUN mkdir -p /root/.aws && \
    apt-get update && \
    apt-get install -y curl unzip less && \
    curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" && \
    unzip -u awscliv2.zip && ./aws/install && \
    pip install boto3 pyyaml argparse && \
    rm -rf awscliv2.zip && rm -rf ./aws/install && \
    apt clean && \
    rm -rf /var/cache/apt/* && \
    rm -rf /var/lib/apt/lists/*
