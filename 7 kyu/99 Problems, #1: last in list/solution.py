57d86d3d3c3f961278000005


def last(lst):
    return lst[-1] if lst else None
_____________________________
def last(a):
    if a: return a[-1]
_____________________________
def last(lst):
    if lst:
        return lst[-1]
_____________________________
last = lambda lst: lst[-1] if lst else None
_____________________________
def last(lst):
    return None if len(lst) == 0 else lst[-1]
_____________________________
def last(lst):
    return ([None]+lst)[-1]
_____________________________
def last(lst=[]):
    if lst != []:
        return lst[-1]
    else:
        return None
_____________________________
def last(lst):
    return None if len(lst) == 0 else lst.pop()
_____________________________
last=lambda c:c[-1]if c else None
_____________________________
# -*- coding:utf-8 -*-
# author      : MolfarUA
# description : solutions for codewars.com
# updated at  : 2022-10-23 01:26
# -----------------------------------------------------
# Kata UUID   : 57d86d3d3c3f961278000005
# Title       : 99 Problems, #1: last in list
# Kyu         : 7 kyu
# Kata's Sensi: spencerwi
# Tags        : ['Lists', 'Fundamentals']
# Vote Score  :  15
# TotalStasr  : 461
# Solved      :  1,326 of 2,773
# Language    : Python
# ----------------------------------------------------
def last(lst):
    return None if len(lst) == 0 else lst[-1]
