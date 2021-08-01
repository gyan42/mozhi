#!/usr/bin/env bash
set -e
export PYTHONPATH=$(pwd):$PYTHONPATH
export PYTHONPATH=$(pwd)/api:$PYTHONPATH
if [ "$DEBUG" = true ] ; then
    echo 'Debugging - ON'
    uvicorn main_calamari:app --host 0.0.0.0 --port 8089 --reload --app-dir=api
else
    echo 'Debugging - OFF'
    uvicorn main_calamari:app --host 0.0.0.0 --port 8089 --app-dir=api
fi
