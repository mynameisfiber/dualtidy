#!/usr/bin/env python2
# -*- coding: utf-8 -*-
#
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.
#

import gtk
import gobject
import subprocess

ACPI_CMD = 'acpitool -b'.split(' ')
TIMEOUT = 5000

class Battery:
    def __init__(self, num=0):
        self.num = num
        self.icon = gtk.StatusIcon()
        self.update_icon()
        gobject.timeout_add(TIMEOUT, self.update_icon)

    def get_battery_info(self):
        try:
            text = subprocess.check_output(ACPI_CMD).split('\n')
            text_battery = text[self.num]
            text_all = text[-2]
        except IndexError:
            return {'state':"Unknown", 'percentage':0, 'tooltip':"Battery not found"}
        try:
            data = text_battery.split(":", 1)[1].split(',')
            state = data[0].strip()
            percentage = float(data[1].strip(' %'))
            tooltip = "{}\n{}".format(text_battery, text_all)
            return {"state":state, "percentage":percentage, 'tooltip':tooltip}
        except Exception, e:
            print "Parse failed: ", e
            return {"state":"Unknown", "percentage":0, "tooltip":"Could not parse: {}".format(text)}

    def get_icon_name(self, state, percentage):
        if state == 'Discharging' or state == 'Unknown':
            if percentage < 10:
                return 'battery-empty-symbolic'
            elif percentage < 20:
                return 'battery-caution-symbolic'
            elif percentage < 40:
                return 'battery-low-symbolic'
            elif percentage < 60:
                return 'battery-good-symbolic'
            else:
                return 'battery-full-symbolic'

        elif state == 'Charging':
            if percentage >= 90:
                return 'battery-full-charging-symbolic'
            elif percentage >= 60:
                return 'battery-good-charging-symbolic'
            elif percentage >= 40:
                return 'battery-low-charging-symbolic'
            elif percentage >= 20:
                return 'battery-caution-charging-symbolic'
            else:
                return 'battery-empty-charging-symbolic'

        elif state == 'Charged':
            return 'battery-full-charged-symbolic'

        elif state == 'Full':
            return 'battery-full-symbolic'

        else:
            return 'battery-missing-symbolic'

    def update_icon(self):
        info = self.get_battery_info()
        icon_name = self.get_icon_name(info['state'], info['percentage'])
        self.icon.set_from_icon_name(icon_name)
        self.icon.set_tooltip_text(info['tooltip'])
        return True

if __name__ == "__main__":
    try:
        num_batteries = len(subprocess.check_output(ACPI_CMD).split('\n')) - 2
        for i in xrange(num_batteries):
            Battery(num = i)
        gtk.main()
    except KeyboardInterrupt:
        pass
