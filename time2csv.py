#!/usr/bin/python

__author__ = 'ban'
__date__ = '2017-01-05 15:55:00'
__version__ = '0.1'

# -----------------------------------------------------------------------------
# Copyright (c) 2016-2017 Bartosz Antosik (ban) for the research carried
# On Frideric Chopin University of Music in Warsaw, POLAND
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# Sample tags-out file format:
#
# 10.377282	11.242845	prompt #1: kaszel
# 20.195971	21.124770	answer #1: samochód; notes to the prompt/answer
# 24.167584	25.282142	prompt #2: dzwonek
# 25.348084	26.276883	answer #2: dzwonek
# [...]
#
# Output CSV file format:
#
# Id [#];Delay [s];Prompt [txt];Answer [txt];Match [b];Notes [txt]
# 1;9,818689000000001;kaszel;samochód;NO;
# 2;1,1804999999999986;dzwonek;dzwonek;YES;Notes
# [...]
#
# Reported assumptions (TODOs):
#
# - If there are more than 1 prompt for #N - report
# - If there are more than 1 answer for #N - report
# - If there is no answer for #N - report
# - If there is no prompt #N - report
#
# -----------------------------------------------------------------------------

import sys
import ntpath
import re

from collections import OrderedDict

def convertToCsv(outfn, csvfn):

    tags = open(csvfn, 'w', encoding='utf-8')

    # We need BOM to clue Excel to read as UTF-8
    tags.write(u'\ufeff')

    results = OrderedDict()

    with open(outfn, 'r', encoding='utf-8') as f:
        for line in f:
            data = line.split()

            _begin = float(data[0])
            _end = float(data[1])
            _op = data[2]
            _id = data[3][1:-1]

            _text = (' '.join(data[4:])).split(';')

            _word = ''
            _notes = ''

            try:
                if _text[0]:
                    _word = _text[0]
            except:
                _word = '[]'
            try:
                if _text[1]:
                    _notes = _text[1].strip()
            except:
                _notes = ''

            if _op == 'prompt':
                if _id in results:
                    print('Warning: Multiple prompts with ID #', _id, sep='')

                if _id not in results:
                    results[_id] = {
                        'id': _id,
                        'begin': _begin,
                        'prompt': _word,
                        'notes': _notes
                    }

            if _op == 'answer':
                if _id in results:
                    if 'answer' in results[_id]:
                        print('Warning: Multiple answers with ID #', _id, sep='')
                    else:
                        if _word == results[_id]['prompt']:
                            _match = 'YES'
                        else:
                            _match = 'NO'

                        results[_id] = {
                            'id': _id,
                            'begin': results[_id]['begin'],
                            'delay': _begin - results[_id]['begin'],
                            'prompt': results[_id]['prompt'],
                            'answer': _word,
                            'match': _match,
                            'notes': results[_id]['notes'] + _notes
                        }

                if _id not in results:
                    print('Warning: No prompt for answer ID #', _id, sep='')

                    _notes = _notes + ' [no prompt for answer ID #' + _id + ']'

                    results[_id] = {
                        'id': _id,
                        'begin': _begin,
                        'delay': 0,
                        'prompt': '',
                        'answer': _word,
                        'match': '',
                        'notes': _notes.strip()
                    }

    print(
        'Id [#];Delay [ms];Prompt [txt];Answer [txt];Match [bool];Notes [txt]',
        file=tags
    )

#   Sweet! Just throws '3a' to the end.
#
#   for key in sorted(results, key=lambda x: '{0:0>8}'.format(x).lower()):
#       result = results[key]

    for result in results.values():

        _notes = ''
        _match = result.get('match', '')
        if _match == '':
            print('Warning: Answer missing for ID #', result['id'], sep='')
            _notes = '[answer-missing]'

        print(
            '#', result['id'], ';',
            int(result.get('delay', 0) * 1000), ';',
            result['prompt'], ';',
            result.get('answer', ''), ';',
            _match, ';',
            result['notes'] + _notes, file=tags, sep=''
        )

if __name__ == '__main__':

    if len(sys.argv) <= 1:
        print('Usage:', ntpath.basename(sys.argv[0]), 'tags-out-file')
        exit()

    out_file_name = sys.argv[1]
    csv_file_name = out_file_name.replace('.txt', '.csv')

    print('Summary:')
    print('')
    print('Input TAGs file: ', out_file_name)
    print('Output CSV file: ', csv_file_name)

    convertToCsv(out_file_name, csv_file_name)
