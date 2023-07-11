# Copyright (c) 2013-2014 Lingpeng Kong
# All Rights Reserved.
#
# This file is part of TweeboParser 1.0.
#
# TweeboParser 1.0 is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# TweeboParser 1.0 is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with TweeboParser 1.0.  If not, see <http://www.gnu.org/licenses/>.

import argparse
import codecs
import os
import re
import sys
import io

parser = argparse.ArgumentParser(description='')
parser.add_argument('inputf', type=str, metavar='', help='')

A = parser.parse_args()


def read_corpus(filename):
    f = codecs.open(filename, "r", "utf-8")
    corpus = []
    sentence = []
    for line in f:
        if line.strip() == "":
            corpus.append(sentence)
            sentence = []
            continue
        else:
            line = line.strip()
            cline = line.split(u"\t")
            sentence.append(cline)
    f.close()
    return corpus

def print_sentence(sentence, outputf):
    for line in sentence:
        s = u""                 #unicode for Python2
        for field in line:
            s += field + "\t"   #Python2: unicode + str return unicode
        s = s.strip()           #Python2: Still unicode
        outputf.write(s+"\n")   #Python2: Still unicode
    outputf.write("\n")
    return

def convert_sentence(i,filename, sen):
    new_sen = []
    ind = 1
    working_log_f=open(filename+'_parsing_log3.txt','a')
    working_log_f.write("message number: "+str(i)+"\n")
    working_log_f.close()
    for line in sen:
        working_log_f=open(filename+'_parsing_log3.txt','a')
        working_log_f.write("index: "+str(ind)+"/ line: "+str(line)+'\n')
        working_log_f.close()
        word = line[0]
        if len(line)>1:
            tag = line[1]
        else:
            working_log_f=open(filename+'_error_log3.txt','a')
            working_log_f.write("message number: "+str(i)+"/ index: "+str(ind)+"/ line: "+str(line)+'\n')
            working_log_f.close()
            tag = 'ERROR'
        new_line = [str(ind), word, '_', tag, tag, '_', '0', '_',  '_',   '_']
        new_sen.append(new_line)
        ind += 1
    return new_sen 

if __name__ == '__main__':
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout)
    #sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='UTF-8', line_buffering=True)   #Ref: https://wiki.python.org/moin/PortingToPy3k/BilingualQuickRef#codecs
    corpus = read_corpus(A.inputf)

    conll_format_corpus = []
    for i,sen in enumerate(corpus):
        conll_format_corpus.append(convert_sentence(i,A.inputf,sen))

    for sen in conll_format_corpus:
        print_sentence(sen, sys.stdout)

