#!/bin/bash
openssl req -x509 -nodes -newkey rsa:4096 -keyout ca.key -out ca.pem -subj /O=me
openssl req -nodes -newkey rsa:4096 -keyout server.key -out server.csr -subj /CN=auth_grpc
openssl x509 -req -in server.csr -CA ca.pem -CAkey ca.key -set_serial 1 -out server.pem
openssl req -nodes -newkey rsa:4096 -keyout client.key -out client.csr -subj /CN=content
openssl x509 -req -in client.csr -CA ca.pem -CAkey ca.key -set_serial 1 -out client.pem

mkdir -p /home/ec2-user/keys
mv *.key *.pem *.csr /home/ec2-user/keys
