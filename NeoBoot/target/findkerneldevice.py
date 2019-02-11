#!/usr/bin/python

import os
import sys
import collections
import struct
import sys
import uuid

# http://en.wikipedia.org/wiki/GUID_Partition_Table#Partition_table_header_.28LBA_1.29
GPT_HEADER_FORMAT = """
8s signature
4s revision
L header_size
L crc32
4x _
Q current_lba
Q backup_lba
Q first_usable_lba
Q last_usable_lba
16s disk_guid
Q part_entry_start_lba
L num_part_entries
L part_entry_size
L crc32_part_array
"""

# http://en.wikipedia.org/wiki/GUID_Partition_Table#Partition_entries_.28LBA_2.E2.80.9333.29
GPT_PARTITION_FORMAT = """
16s type
16s unique
Q first_lba
Q last_lba
Q flags
72s name
"""

import os
import sys
import collections
import struct
import uuid
GPT_HEADER_FORMAT = '\n8s signature\n4s revision\nL header_size\nL crc32\n4x _\nQ current_lba\nQ backup_lba\nQ first_usable_lba\nQ last_usable_lba\n16s disk_guid\nQ part_entry_start_lba\nL num_part_entries\nL part_entry_size\nL crc32_part_array\n'
GPT_PARTITION_FORMAT = '\n16s type\n16s unique\nQ first_lba\nQ last_lba\nQ flags\n72s name\n'

def _make_fmt(name, format, extras = []):
    type_and_name = [ l.split(None, 1) for l in format.strip().splitlines() ]
    fmt = ''.join((t for t, n in type_and_name))
    fmt = '<' + fmt
    tupletype = collections.namedtuple(name, [ n for t, n in type_and_name if n != '_' ] + extras)
    return (fmt, tupletype)


class GPTError(Exception):
    pass


def read_header(fp, lba_size = 512):
    fp.seek(1 * lba_size)
    fmt, GPTHeader = _make_fmt('GPTHeader', GPT_HEADER_FORMAT)
    data = fp.read(struct.calcsize(fmt))
    header = GPTHeader._make(struct.unpack(fmt, data))
    if header.signature != 'EFI PART':
        raise GPTError('Bad signature: %r' % header.signature)
    if header.revision != '\x00\x00\x01\x00':
        raise GPTError('Bad revision: %r' % header.revision)
    if header.header_size < 92:
        raise GPTError('Bad header size: %r' % header.header_size)
    header = header._replace(disk_guid=str(uuid.UUID(bytes_le=header.disk_guid)))
    return header


def read_partitions(fp, header, lba_size = 512):
    fp.seek(header.part_entry_start_lba * lba_size)
    fmt, GPTPartition = _make_fmt('GPTPartition', GPT_PARTITION_FORMAT, extras=['index'])
    for idx in xrange(1, 1 + header.num_part_entries):
        data = fp.read(header.part_entry_size)
        if len(data) < struct.calcsize(fmt):
            raise GPTError('Short partition entry')
        part = GPTPartition._make(struct.unpack(fmt, data) + (idx,))
        if part.type == '\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00':
            continue
        part = part._replace(type=str(uuid.UUID(bytes_le=part.type)), unique=str(uuid.UUID(bytes_le=part.unique)), name=part.name.decode('utf-16').split('\x00', 1)[0])
        yield part


def find_kernel_device_udevadm(kernelpartition):
    try:
        for partition in os.listdir('/sys/block/mmcblk0'):
            if partition.startswith('mmcblk0p'):
                if kernelpartition == name:
                    return '/dev/' + partition

        return ''
    except:
        return ''


def find_kernel_device_gpt(kernelpartition):
    device = '/dev/mmcblk0'
    try:
        import re
        device = re.search('/dev/mmcblk(\\d+)', open('/proc/cmdline').read()).group(0)
    except:
        pass

    try:
        p = 1
        header = read_header(open(device, 'r'))
        for part in read_partitions(open(device, 'r'), header):
            if kernelpartition == part.name:
                return device + 'p' + str(p)
            p += 1

        return ''
    except:
        return ''


try:
    kerneldev = open('/sys/firmware/devicetree/base/chosen/kerneldev', 'r').readline().split('.')
    if 'emmcflash0' in kerneldev[0]:
        kerneldevice = find_kernel_device_udevadm(kerneldev[1].strip('\x00'))
        if kerneldevice == '':
            kerneldevice = find_kernel_device_gpt(kerneldev[1].strip('\x00'))
        if kerneldevice != '':
            os.symlink(kerneldevice, '/dev/kernel')
except:
    pass