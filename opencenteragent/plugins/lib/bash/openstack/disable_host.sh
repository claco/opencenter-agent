#!/bin/bash
#               OpenCenter(TM) is Copyright 2013 by Rackspace US, Inc.
##############################################################################
#
# OpenCenter is licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.  This
# version of OpenCenter includes Rackspace trademarks and logos, and in
# accordance with Section 6 of the License, the provision of commercial
# support services in conjunction with a version of OpenCenter which includes
# Rackspace trademarks and logos is prohibited.  OpenCenter source code and
# details are available at: # https://github.com/rcbops/opencenter or upon
# written request.
#
# You may obtain a copy of the License at
# http://www.apache.org/licenses/LICENSE-2.0 and a copy, including this
# notice, is available in the LICENSE file accompanying this software.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the # specific language governing permissions and limitations
# under the License.
#
##############################################################################
#

set -o errexit
source "$OPENCENTER_BASH_DIR/opencenter.sh"

if [[ ! -e /root/openrc ]]; then
    echo "/root/openrc does not exist and I cannot continue.  Good bye."
    exit 1
fi

if [[ ! -e /usr/bin/nova-manage ]]; then
    echo "nova-manage has not been installed and I cannot continue without it.  Good bye."
    exit 2
fi

. /root/openrc

nova-manage service disable --service=nova-compute --host=$(hostname -f)

return_fact "maintenance_mode" "true"
