#!/bin/sh

echo "Input Client numbers: "

read client_nums
mkdir "clients"
echo `pwd`

for var in $(seq 1 $client_nums)
do
  mkdir "./clients/client_${var}"
  python client.py ${var} 'logo.png'

done
