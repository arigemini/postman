#!/bin/bash

set -e

find /Users/arindam/training_input -type dir | grep -E "(gerald|kenneth|sara|jeff)" | xargs python generate_snow_input.py --training_file train.snow --emails_file emails.snow --id_mappings_file id_mappings.snow --email_dirs
labels=$(cat train.snow | ./etc/list_labels)
~/Snow_v3.2/snow -train -I train.snow -F net.snow -W:${labels}
~/Snow_v3.2/snow -test -I train.snow -F net.snow
echo -e "\nRUN: cat train.snow | python utils/check_line.py id_mappings.snow emails.snow"
