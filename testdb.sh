#!/bin/bash

sudo -u postgres psql << EOF
ALTER USER oikos CREATEDB;
EOF