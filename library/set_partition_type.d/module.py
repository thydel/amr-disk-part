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
            partition = dict(required=True, aliases=['part']),
            type = dict(required=False, default='LVM'),
	),
        supports_check_mode=True
    )

    sysid = {'Linux': '83', 'LVM' : '8e' }
    name = dict(zip(sysid.values(), sysid))

    new_name = module.params.get('type')
    if not new_name in sysid:
        module.fail_json(msg='Unknown type name {}'.format(new_name))
    new_sysid = sysid[new_name]

    disk = '/dev/disk/' + module.params.get('disk')

    if not os.path.exists(disk):
        module.fail_json(msg="Device {} not found".format(disk))

    disk_realpath = os.path.realpath(disk)

    if not os.path.exists(disk_realpath):
        module.fail_json(msg="Real path device {} not found".format(disk_realpath))

    sep = ''
    if (disk[-1].isdigit()):
        sep = 'p'
    
    part = disk + sep + str(module.params.get('part'))
    part_realpath = disk_realpath + str(module.params.get('part'))

    if not os.path.exists(part_realpath):
        module.fail_json(msg="Real path partition device {} not found".format(part_realpath))

    cmd = 'sfdisk -d {} | grep {} | cut -d: -f2 | cut -d, -f3 | cut -d= -f2'.format(disk, part)
    rc, out, err = module.run_command(cmd, check_rc=True, use_unsafe_shell=True)

    old_sysid = out.strip()
    
    if not old_sysid in name:
        module.fail_json(msg='Unknown type sysid {} actually on partition {}'.format(old_sysid, part))

    old_name = name[old_sysid]

    if old_sysid == new_sysid:
        module.exit_json(changed=False, realpath=part_realpath, old_type=old_name)

    if module.check_mode:
        module.exit_json(changed=True, realpath=part_realpath, old_type=old_name)

    cmd = "sfdisk -d {} | sed -e '\;{};s/Id={}/Id={}/' | sfdisk {}".format(disk, part, old_sysid, new_sysid, disk)
    rc, out, err = module.run_command(cmd, check_rc=True, use_unsafe_shell=True)

    module.exit_json(changed=True, realpath=part_realpath, old_type=old_name)

# this is magic, see lib/ansible/module_common.py
#<<INCLUDE_ANSIBLE_MODULE_COMMON>>

main()
