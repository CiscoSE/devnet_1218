#!/usr/bin/env bash


echo "Testing connectivity to vManage"
curl -k -X GET \
  https://198.18.1.10/dataservice/template/policy/definition/control/ \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Basic YWRtaW46YWRtaW4='

source $HOME/devnet_1218/devnet_1218_env/bin/activate
echo "Opening Pycharm"
charm .