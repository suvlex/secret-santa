#!/usr/bin/env bash

./manage.py dumpdata --indent=4 core.team > core/fixtures/teams.json
