#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2022 rzavalet <rzavalet@thinkbook>
#
# Distributed under terms of the MIT license.

"""
This is a code to demonstrate the reusable barrier.
"""

from threading import *

def rendezvous(num, tid):
    print(f'[R {num}] Thread {tid} arrived')

def critical_point(num, tid):
    print(f'[CP {num}] Thread {tid} entered critical point')

def myfunc(num_threads, tid, mutex, barrier1, barrier2, counter):
    for i in range(5):
        rendezvous(i, tid)

        mutex.acquire()
        counter[0] += 1
        if counter[0] == num_threads:
            barrier2.acquire()
            barrier1.release()
        mutex.release()

        barrier1.acquire()
        barrier1.release()

        critical_point(i, tid)

        mutex.acquire()
        counter[0] -= 1
        if counter[0] == 0:
            barrier1.acquire()
            barrier2.release()
        mutex.release()

        barrier2.acquire()
        barrier2.release()

if __name__ == '__main__':
    num_threads = 10
    thread_list = []
    mutex = Semaphore(1)
    barrier1 = Semaphore(0)
    barrier2 = Semaphore(1)
    counter = [0]

    for i in range(num_threads):
        thr = Thread(target = myfunc, args = (num_threads, i, mutex, barrier1, barrier2, counter))
        thread_list.append(thr)
        thr.start()

    for thr in thread_list:
        thr.join()
