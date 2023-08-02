#!/usr/bin/env bash

./manage.py dumpdata --indent=4 core.member > core/fixtures/members.json
