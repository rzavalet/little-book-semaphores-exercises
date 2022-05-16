#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2022 rzavalet <rzavalet@thinkbook>
#
# Distributed under terms of the MIT license.

"""
This is a solution to the Mutual Exclusion problem
using semaphores
"""
from threading import *

def increase_count(x, s1):
    i = 10000
    while i > 0:
        s1.acquire()
        x[0] = x[0] + 1
        print(f'New count: {x[0]}')
        s1.release()
        i = i - 1


if __name__ == '__main__':
    x = [0]

    s1 = Semaphore(1)
    thr1 = Thread(target=increase_count, args=(x,s1));
    thr2 = Thread(target=increase_count, args=(x,s1));

    thr1.start()
    thr2.start()

    thr1.join()
    thr2.join()

