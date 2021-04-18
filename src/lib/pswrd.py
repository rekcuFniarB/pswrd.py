##    Pswrd.py
##    Copyright (C) 2020  rekcuFniarB <retratserif@gmail.com>
##
##    This program is free software: you can redistribute it and/or modify
##    it under the terms of the GNU General Public License as published by
##    the Free Software Foundation, either version 3 of the License, or
##    (at your option) any later version.
##
##    This program is distributed in the hope that it will be useful,
##    but WITHOUT ANY WARRANTY; without even the implied warranty of
##    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##    GNU General Public License for more details.
##
##    You should have received a copy of the GNU General Public License
##    along with this program.  If not, see <https://www.gnu.org/licenses/>.


from hashlib import md5
from base64 import b64encode

def gen(input, alnum=False):
    '''Gen password string from bytes input.
    alnum: bool, remove non alphanumeric values '''
    result = b64encode(md5(input).digest()[0:15])
    result = sanitize(result, alnum)
    return result

def gen_from_list(values, compat=False, alnum=False):
    vals = []
    for val in values:
        if val:
            vals.append(val)
    if compat:
        vals = ''.join(vals)
    else:
        vals = '\t'.join(vals)
    ## turn to bytes
    vals = vals.encode('utf-8')
    return gen(vals, alnum)

def gen_from_file(filename, salt=b'', alnum=False):
    if type(salt) is not bytes:
        salt = salt.encode('utf-8')
    md5hash = md5(salt)
    try:
        with open(filename, 'rb') as f:
            end = False
            while not end:
                chunk = f.read(1024 * 1024)
                if (chunk):
                    md5hash.update(chunk)
                else:
                    end = True
    except:
        return 'NULL'
    
    result = b64encode(md5hash.digest()[0:15])
    result = sanitize(result, alnum)
    
    return result

def sanitize(value, alnum=False):
    value = value.replace(b'/', b'_')
    
    for _ in [b' ', b'\n']:
        value = value.replace(_, b'')
    
    if alnum:
        for _ in [b'+', b'.', b'-', b'_', b'=']:
            value = value.replace(_, b'')
    return value

def hide_part(value):
    length = len(value) - 3
    visible_part = value[0:3]
    return b'%s%s' % (visible_part, b'*' * length)
