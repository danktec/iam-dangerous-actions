ARG BUILD_PLATFORM=linux/arm64/v8
FROM --platform=${BUILD_PLATFORM} python:3.12.11-trixie

SHELL ["/bin/bash", "--login", "-c"]

# Install Node & NPM
RUN curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.35.3/install.sh | bash
RUN nvm install v22.18.0
RUN npm install -g npm@11.5.2

# Add files
RUN mkdir -p /root/iam-dangerous-actions/
WORKDIR /root/iam-dangerous-actions/
ADD . .
