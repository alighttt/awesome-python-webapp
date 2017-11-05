#!/usr/bin/python
# -*- coding:utf-8 -*-

import logging

def foo(s):
    return 10 / int(s)

def bar(s):
    return foo(s) * 2

def main():
    bar('0')

main()
print 'end'
