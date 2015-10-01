#!/bin/bash

set -e
if [[ `git config --get remote.origin.url` = "$GIT_URL" ]]; then
  git fetch origin $GIT_BRANCH >/dev/null
  git reset --hard FETCH_HEAD >/dev/null
else
  rm -rf ./*
  git clone $GIT_URL . >/dev/null
  git checkout $GIT_BRANCH >/dev/null
fi
git rev-parse HEAD

rm -f /source/$WAR_PATH 

mvn -DskipTests=true clean package 1>&2 && cp `find target -name '*.war'` /source/$WAR_PATH

python -mSimpleHTTPServer 80