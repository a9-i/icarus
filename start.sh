#!/bin/bash
clear

if ! command -v screen docker &> /dev/null
then
  echo 'Error: Please ensure Screen and Docker is installed'
  exit
fi

#docker build --no-cache -t icarus .
docker build -t icarus .

screen docker run -a stdin -a stdout -it \
-p 21:21/tcp \
-p 23:23/tcp \
-p 25:25/tcp \
-p 53:53/tcp \
-p 110:110/tcp \
-p 111:111/tcp \
-p 119:119/tcp \
-p 135:135/tcp \
-p 139:139/tcp \
-p 143:143/tcp \
-p 445:445/tcp \
-p 514:514/tcp \
-p 993:993/tcp \
-p 995:995/tcp \
-p 1025:1025/tcp \
-p 1110:1110/tcp \
-p 1433:1433/tcp \
-p 1434:1434/tcp \
-p 1723:1723/tcp \
-p 2049:2049/tcp \
-p 3306:3306/tcp \
-p 3389:3389/tcp \
-p 5432:5432/tcp \
-p 5900:5900/tcp \
-p 6000:6000/tcp \
-p 5600:5600/udp \
-p 161:161/udp \
icarus