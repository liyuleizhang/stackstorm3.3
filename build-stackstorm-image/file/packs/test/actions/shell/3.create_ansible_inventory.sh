#!/usr/bin/env bash

node01=$1
node02=$2
node03=$3
node04=$4

cat > /etc/ansible/stage/test/inventory <<- EOF
${node01}
${node02}
${node03}
${node04}
EOF

cat /etc/ansible/stage/test/inventory
