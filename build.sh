#!/bin/bash
set -e
set -o pipefail

instruction()
{
  echo -e "usage: ./build.sh command <params> "
  echo -e 
  echo -e "Available commands:"
  echo -e
  echo -e "build"
  echo -e
  echo -e "release"
  echo -e
}

# Parse options in format --arg value.
POSITIONAL=()
while [[ $# -gt 0 ]]
do
  key="$1"

  case $key in
      *)    # unknown option
        POSITIONAL+=("$1") # save it in an array for later
        shift # past argument
      ;;
  esac
done
set -- "${POSITIONAL[@]}" # restore positional parameters

# There only one positional arg that is the command:
COMMAND=$1
if [ $# -eq 0 ]; then
  instruction
  exit 1
fi

# Run commands
case $COMMAND in

  build)
    nbdev_build_lib
  ;;

  pair-notebooks)
    jupytext --set-formats ipynb,py:light src/*.ipynb
  ;;
    
  sync-notebooks)
    jupytext --sync src/*.py
  ;;
  

  run)
    if [ $ETL_NAME ]; then
      ETL_NAME_ARG="--name $ETL_NAME"
    fi
    
    nbdev_build_lib
    python -m {lib_name} $ETL_NAME_ARG
  ;;

  release)
    AWS_ACCOUNT=$(aws sts get-caller-identity --query "Account" --output text)
    CODEARTIFACT_DOMAIN=taidy
    CODEARTIFACT_REPOSITORY=taidy
    

    # clean mbit_etl folder
    rm -rf {lib_name}

    nbdev_build_lib
  

    rm -rf dist
    python setup.py sdist bdist_wheel

    export TWINE_USERNAME=aws
    export TWINE_PASSWORD=`aws codeartifact get-authorization-token --domain ${CODEARTIFACT_DOMAIN} --domain-owner ${AWS_ACCOUNT} --query authorizationToken --output text`
    export TWINE_REPOSITORY_URL=https://${CODEARTIFACT_DOMAIN}-${AWS_ACCOUNT}.d.codeartifact.eu-west-1.amazonaws.com/pypi/${CODEARTIFACT_REPOSITORY}/

    twine upload --repository codeartifact dist/*
  ;;

  *)
    echo -e "Unrecognized Command $COMMAND"
    echo -e
    instruction
    exit 1
  ;;
esac
