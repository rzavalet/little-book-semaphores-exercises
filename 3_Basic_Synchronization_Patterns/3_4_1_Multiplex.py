#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2022 rzavalet <rzavalet@thinkbook>
#
# Distributed under terms of the MIT license.

"""
This is a solution to the Multiplex problem
"""
from threading import *
import time

def enter_the_club(tid, s1):
    i = 1000
    while i > 0:
        s1.acquire()
        print(f'Thread {tid} enters the club');
        time.sleep(1)
        print(f'Thread {tid} leaves the club');
        i = i - 1
        s1.release()


if __name__ == '__main__':
    limit = 5
    s1 = Semaphore(limit)

    thr_list = []
    for i in range(10):
        thr = Thread(target=enter_the_club, args=(i, s1,))
        thr_list.append(thr)
        thr.start()


    for thr in thr_list:
        thr.join()

