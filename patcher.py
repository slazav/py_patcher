#!/usr/bin/python3


##################################################
## Parse options

import argparse

parser = argparse.ArgumentParser(
  prog='patcher.py',
  description='Use a pattern file to patch a binary file.'
  +' Search/replace patterns are read from <patt_file>.'
  +' If <in_file> is provided, then all patterns are searched in it.'
  +' Results with pattern names are printed.'
  +' If <out_file> is provided, then last match is applied and'
  +' patched file saved.'
  +' Use -p option to select a specific pattern name.'
  +' There is no guarantee that patched file will work.',
  epilog='slazav, 12.2024')

parser.add_argument('-p', '--pattern', action='store',
  metavar='name', help='use only specified pattern')

parser.add_argument('-f', '--force', action='store_true',
  help='proceed if unable to calculate or find checksum of original file')

parser.add_argument('-n', '--nocs', action='store_true',
  help='check and update garmin-specific checksum')

parser.add_argument('patt_file', help='file with search/replace patterns')
parser.add_argument('in_file',  nargs='?', default='', help='search patterns in this file')
parser.add_argument('out_file', nargs='?', default='', help='if provided patch')

args = parser.parse_args()

##################################################
## Read pattern file

# It's a Windows-style config file. Only sections SearchPatterns
# and ReplacePatterns are read. Patterns are taken from every
# <key>=<value> line in these sections and put into patt dictionary
# with <key> taken from file. Keys for search and replace patters
# should match.

import re
patt = {}

with open(args.patt_file, 'r') as pf:
  section = ''; # current section
  comment = ''; # store only one previous line of comments

  for l in pf:
    l = re.sub(r';.*$', '', l).strip(); # remove comments and cr-nl

    # sections
    sect_match = re.match(r"^\[([a-z]+)\]", l, re.IGNORECASE)
    if sect_match:
      section=sect_match.group(1);
      continue

    var_match = re.match(r"([a-z0-9]+)=(.*)$", l, re.IGNORECASE)
    if not var_match: continue
    key = var_match.group(1)
    val = var_match.group(2).strip()

    if section == 'SearchPatterns':
      if not key in patt: patt[key] = {}
      patt[key]["spatt"] = val

    if section == 'ReplacePatterns':
      if not key in patt: patt[key] = {}
      patt[key]["rpatt"] = val


if args.pattern and args.pattern not in patt:
  print(args.pattern, ': pattern not found')
  exit(1)

##################################################
## Read binary file and convert it to HEX

if not args.in_file: exit(0)

print('## Reading file:', args.in_file)
with open(args.in_file, mode="rb") as f:
  data_bin=f.read()
  data=data_bin.hex(' ')

##################################################
# calculate and verify checksum

# the function will be used later for setting checksum
CS_POS=10
CS_OFF=1
def calc_cs(data):
  cs=CS_OFF
  N=len(data)
  for i in range(N):
    if i!=N-CS_POS: cs = (cs + data[i]) & 0xFF
  return 0xFF-cs

if not args.nocs:
  cs  = calc_cs(data_bin)
  cs0 = data_bin[len(data_bin)-CS_POS]
  if cs != cs0:
    print("checksum is WRONG:", cs, cs0)
    if not args.force: exit(1)
  else:
    print("checksum is OK")

##################################################
## Search every pattern in the data.
## Use python regex!

print('## Searching patterns (name -- result)')
lastmatch=''
for key in patt:

  # select pattern
  if args.pattern and args.pattern != key: continue

  # missing search patterns
  if "spatt" not in patt[key]:
    print(key, ': no search pattern')
    continue

  # missing replace puttern
  if "rpatt" not in patt[key]:
    print(key, ': no replace pattern')
    continue

  # fix replace pattern
  patt[key]["rpatt"] = re.sub(r'\$', r'\\', patt[key]["rpatt"]);

  # detect duplicated patterns
  copy=None
  for k1 in patt:
    if k1 == key: break
    if patt[k1]["spatt"] == patt[key]["spatt"] and\
       patt[k1]["rpatt"] == patt[key]["rpatt"]:
      copy = k1
      break
  if copy:
    print(key, '-- copy of', copy)
    continue

  # search
  match = re.search(patt[key]["spatt"], data, re.IGNORECASE)

  if match:
    print(key, '-- MATCH: ', match.start(), '...', match.end())
    lastmatch=key
  else:
    print(key, '-- no match')
    continue

######################################
## do patching
if args.out_file and lastmatch:

  key=lastmatch
  print('## Do patching with', key, ', writing file:', args.out_file)

  data1 = bytes.fromhex(\
    re.sub(patt[key]["spatt"], patt[key]["rpatt"], data, re.IGNORECASE))

  fo = open(args.out_file, mode="wb")
  fo.write(data1)

  if not args.nocs:
    fo.seek(len(data1)-CS_POS)
    fo.write(calc_cs(data1).to_bytes(1))
  fo.close
