#!/bin/bash

# scripts to build fresh stack based on tags
# and applying feature branch migrations

# fresh build via tags, frontend/backend with cleared db
git checkout 4.5.0
cd ../ansible-hub-ui/
git checkout 4.5.0
cd ../galaxy_ng/
./compose build
make docker/resetdb
make docker/loaddata
./compose up


# # apply feature branches
# git checkout remove_fk_in_rbac_migration
# cd ../ansible-hub-ui/
# git checkout upstream/feature/rbac-roles
# cd ../galaxy_ng/
# ./compose build
# make docker/migrate
# ./compose up
