#!/bin/bash
cd /home/ec2-user/production

# TODO use SSM Parameter Store for env variables
sudo cp /home/ec2-user/env/.*.env .

sudo mkdir -p services/auth/keys/
sudo cp /home/ec2-user/keys/* services/auth/keys/
sudo mkdir -p services/content/keys/
sudo cp /home/ec2-user/keys/* services/content/keys/
