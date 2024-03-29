#!/bin/bash

set -e

find ${HOME}/training_input -type dir | grep -E "(gerald.nemec|kenneth.lay|sara.shackleton|jeff.skilling|jeff.dasovich)" | xargs python generate_snow_input.py --tf_idf --named_entities --training_file train.snow --emails_file emails.snow --id_mappings_file id_mappings.snow --email_dirs
labels=$(cat train.snow | ./utils/list_labels)
~/Snow_v3.2/snow -train -I train.snow -F net.snow -W:${labels}
~/Snow_v3.2/snow -test -I train.snow -F net.snow
