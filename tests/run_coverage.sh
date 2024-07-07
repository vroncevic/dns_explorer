#!/bin/bash
#
# @brief   dns_explorer
# @version v1.0.1
# @date    Sat Jun 29 01:47:55 AM CEST 2024
# @company None, free software to use 2024
# @author  Vladimir Roncevic <elektron.ronca@gmail.com>
#

rm -rf htmlcov dns_explorer_coverage.xml dns_explorer_coverage.json .coverage
ats_coverage_run.py -n dns_explorer -p ../README.md
python3 -m coverage run -m --source=../dns_explorer unittest discover -s ./ -p '*_test.py' -vvv
python3 -m coverage html -d htmlcov
python3 -m coverage xml -o dns_explorer_coverage.xml 
python3 -m coverage json -o dns_explorer_coverage.json
python3 -m coverage report --format=markdown -m
