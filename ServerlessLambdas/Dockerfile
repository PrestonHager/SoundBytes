FROM amazonlinux:2017.03

# Libsodium and Go versions to install
ARG LIBSODIUM_VERSION="libsodium-1.0.18"

# Install prerequesites via yum
RUN yum update -y
RUN yum install -y zip gcc tar git

# Download and build libsodium, including shared object files (.so)
RUN \
  mkdir -p /tmpbuild/libsodium && \
  cd /tmpbuild/libsodium && \
  curl -L https://download.libsodium.org/libsodium/releases/$LIBSODIUM_VERSION.tar.gz -o $LIBSODIUM_VERSION.tar.gz && \
  tar xfvz $LIBSODIUM_VERSION.tar.gz && \
  cd /tmpbuild/libsodium/$LIBSODIUM_VERSION/ && \
  ./configure && \
  make && make check && \
  make install && \
  mv src/libsodium /usr/local/ && \
  rm -Rf /tmpbuild/

# Setup /app working directory
RUN mkdir /app
WORKDIR /app

# Copy libsodium to lib directory for deployment package structure
RUN mkdir lib
RUN cp /usr/local/lib/libsodium.so.23.3.0 lib/
RUN cp /usr/local/lib/libsodium.so.23 lib/
RUN cp /usr/local/lib/libsodium.so lib/

ARG SHARED_BUILD_FOLDER=/build

RUN zip package.zip lib/*
RUN mkdir -p $SHARED_BUILD_FOLDER
RUN cp package.zip $SHARED_BUILD_FOLDER/
