#!/usr/bin/env python
'''
OWASP ZSC
https://www.owasp.org/index.php/OWASP_ZSC_Tool_Project
https://github.com/zscproject/OWASP-ZSC
http://api.z3r0d4y.com/
https://groups.google.com/d/forum/owasp-zsc [ owasp-zsc[at]googlegroups[dot]com ]
'''
import binascii
import random
import string
from core.compatible import version
_version = version()


def encode(f):
    var_name = ''.join(
        random.choice(string.ascii_lowercase + string.ascii_uppercase)
        for i in range(50))

    if _version is 2:
        rev_data = binascii.b2a_base64(f)[-2::-1]
        data = var_name + ' = "' + str(rev_data) + '"'
    if _version is 3:
        rev_data = binascii.b2a_base64(f.encode('utf8')).decode('utf8')[-2::-1]
        data = var_name + ' = "' + str(rev_data) + '"'
    var_data = ''.join(
        random.choice(string.ascii_lowercase + string.ascii_uppercase)
        for i in range(50))
    func_name = ''.join(
        random.choice(string.ascii_lowercase + string.ascii_uppercase)
        for i in range(50))
    func_argv = ''.join(
        random.choice(string.ascii_lowercase + string.ascii_uppercase)
        for i in range(50))
    f = '''
import binascii
import sys
%s
def %s(%s):
    if sys.version_info.major is 2:
        return str(binascii.a2b_base64(%s[::-1]))
    elif sys.version_info.major is 3:
        return str(binascii.a2b_base64(%s[::-1]).encode('utf8'))[::-1].decode('utf8')
    else:
        sys.exit('Your python version is not supported!')
%s = %s
exec(%s(%s))
''' % (data, func_name, func_argv, func_argv, func_argv, var_data, var_name,
       func_name, var_data)
    return f


def start(content,cli):
    return str(str('\'\'\'\n') + str(content.replace('\'\'\'', '\\\'\\\'\\\''))
               + str('\n\'\'\'') + str(encode(content)) + str('\n'))
