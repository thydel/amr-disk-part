#!/usr/bin/python
# -*- coding: utf-8 -*-

# (c) 2014, <t.delamare@epiconcept.fr>
#
# This module is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this software.  If not, see <http://www.gnu.org/licenses/>.

DOCUMENTATION = '''
#include documentation.yml
'''

EXAMPLES = '''
#include examples.yml
'''

def main():
    module = AnsibleModule(
        argument_spec = dict(
            disk = dict(required=True),
	),
        supports_check_mode=True
    )

    path = '/dev/disk/' + module.params.get('disk')
    cmd = ["/usr/bin/env", "lsblk", "-lno", "TYPE", path]
    rc, out, err = module.run_command(cmd, check_rc=True)

    partitioned = False
    if 'part' in out:
        partitioned = True

    module.exit_json(changed=False, partitioned=partitioned)

# this is magic, see lib/ansible/module_common.py
#<<INCLUDE_ANSIBLE_MODULE_COMMON>>

main()
