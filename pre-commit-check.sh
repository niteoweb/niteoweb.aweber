#!/bin/bash

function handle_exit {
    if [ $? -ne 0 ]; then
        EXITCODE=1
    fi
}

EXITCODE=0

echo '====== Running tests ========='
bin/test --color -s niteoweb.aweber; handle_exit

echo '====== Running ZPTLint ======'
for pt in `find src/niteoweb/aweber/ -name "*.pt"` ; do bin/zptlint $pt; done

echo '====== Running PyFlakes ======'
bin/pyflakes src/niteoweb/aweber; handle_exit
bin/pyflakes setup.py; handle_exit

echo '====== Running pep8 =========='
bin/pep8 --ignore=E501 --count src/niteoweb/aweber; handle_exit
bin/pep8 --ignore=E501 --count setup.py; handle_exit

if [ $EXITCODE -ne 0 ]; then
    exit 1
fi
