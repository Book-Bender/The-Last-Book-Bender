#!/usr/bin/env bash


scriptDir="./InitScripts"

echo "Downloading data."
bash "${scriptDir}/initData.sh"

echo "Preparing Python virtual environments and downloading data"
bash "${scriptDir}/initPython.sh"
