#!/bin/bash
KEY_FILE="backup/apache-selfsigned.key"
CRT_FILE="backup/apache-selfsigned.crt"
CSR_FILE="/tmp/apache-selfsigned.csr"
CN="localhost"

openssl genrsa -des3 -out $KEY_FILE -passout pass:1234 2048
openssl req -new -key $KEY_FILE -passin pass:1234 -out $CSR_FILE -subj "/C=PL/ST=Pomerenian Voivodeship/L=Gdansk/O=Lampex-Pol sp. z.o.o/OU=Dzial Internetowy/CN=$CN/emailAddress=biz_lampexpol\@outlook.com"
openssl rsa -in $KEY_FILE -passin pass:1234 -out $KEY_FILE
openssl x509 -req -in $CSR_FILE -signkey $KEY_FILE -out $CRT_FILE -days 3650 -sha256 -extfile v3.ext
