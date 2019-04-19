#!/usr/bin/env bash


echo "Testing connectivity to vManage"
curl -k -X GET \
  https://198.18.1.10/dataservice/template/policy/definition/control/ \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Basic YWRtaW46YWRtaW4='


echo "Opening Pycharm"
charm .