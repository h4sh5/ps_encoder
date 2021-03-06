#!/usr/bin/env python
# -*- coding: utf-8 -*-

#    PSEncoder
#    This version is a modification of darkoperator's ps_encoder.py https://github.com/darkoperator/powershell_scripts/blob/master/ps_encoder.py made by Carlos Perez

#
#    Copyright (C) 2017 Haoxi Tan
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; Applies version 2 of the License.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program; if not, write to the Free Software
#    Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA


import base64
import sys
import re
import os
import getopt


def powershell_encode(data):
    # blank command will store our fixed unicode variable
    blank_command = ""
    powershell_command = ""
    # Remove weird chars that could have been added by ISE
    n = re.compile(u'(\xef|\xbb|\xbf)')
    # loop through each character and insert null byte
    for char in (n.sub("", data)):
        # insert the nullbyte
        blank_command += char + "\x00"
    # assign powershell command as the new one
    powershell_command = blank_command
    # base64 encode the powershell command
    powershell_command = base64.b64encode(powershell_command)
    return powershell_command


def usage():
    print("Usage: {0} <options>\n".format(sys.argv[0]))
    print("Enters interactive mode if no options provided.")
    print("Options:")
    print("   -h, --help                  Show this help message and exit")
    print("   -s, --script      <script>  PowerShell Script.")

    sys.exit(0)


def main():
    try:
        options, args = getopt.getopt(sys.argv[1:], 'hs:', ['help', 'script'])
    except getopt.GetoptError:
        print "Wrong Option Provided!"
        usage()
    if len(sys.argv) == 2:
        usage()

    for opt, arg in options:
        if opt in ('-h', '--help'):
            usage()
        elif opt in ('-s', '--script'):  
            script_file = arg
            if not os.path.isfile(script_file):
                    print "The specified powershell script does not exists"
                    sys.exit(1)
            else:
                ps_script = open(script_file, 'r').read()
                print "powershell -encodedCommand",powershell_encode(ps_script)
                exit()
        
    else:
        while 1:
            try:
                ps_script =  raw_input("ps_encoder$ ")
                # print(powershell_encode(ps_script))
                print "powershell -encodedCommand",powershell_encode(ps_script)
            except KeyboardInterrupt:
                exit("\nUser interrupt.")

if __name__ == "__main__":
    main()
