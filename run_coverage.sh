#!/bin/bash
#
# @brief   dns_explorer
# @version 1.0.7
# @date    Sat Aug 07 07:35:10 2026
# @company None, free software to use 2026
# @author  Vladimir Roncevic <elektron.ronca@gmail.com>
#

python3 coverage/ats_coverage.py dns_explorer
pylint dns_explorer > dns_explorer.report
echo "Done"
