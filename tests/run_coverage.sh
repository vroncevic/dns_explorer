#!/bin/bash
#
# @brief   dns_explorer
# @version v1.0.1
# @date    Sat Jun 29 01:47:55 AM CEST 2024
# @company None, free software to use 2024
# @author  Vladimir Roncevic <elektron.ronca@gmail.com>
#

python3 -m coverage run -m --source=../dns_explorer unittest discover -s ./ -p '*_test.py' -vvv
python3 -m coverage html
