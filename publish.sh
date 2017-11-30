#!/usr/bin/env bash
set -euf -o pipefail

echo "==================== UPLOADING TO PYPITEST (https://testpypi.python.org/pypi) ===================="
python setup.py sdist upload -r pypitest

#echo "==================== UPLOADING TO PYPI (https://pypi.python.org/pypi) ============================"
#python setup.py sdist upload -r pypi

echo "~ * ~ * ~  D O N E  ~ * ~ * ~"
