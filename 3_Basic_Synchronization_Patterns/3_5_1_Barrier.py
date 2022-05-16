#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2022 rzavalet <rzavalet@thinkbook>
#
# Distributed under terms of the MIT license.

"""
This is a solution to the barrier problem
"""
from threading import *

def rendezvous(tid):
    print(f'Thread {tid} arrived')

def critical_point(tid):
    print(f'Thread {tid} entered critical point')

def myfunc(num_threads, tid, mutex, barrier, counter):
    
    rendezvous(tid)

    mutex.acquire()
    counter[0] = counter[0] + 1
    print(f'Counter = {counter[0]}')
    if counter[0] == num_threads:
        barrier.release()
    mutex.release()

    # This pattern is called a 'turnstile'
    barrier.acquire()
    barrier.release()

    critical_point(tid)

if __name__ == '__main__':
    num_threads = 10
    thread_list = []
    mutex = Semaphore(1)
    barrier = Semaphore(0)
    counter = [0]

    for i in range(num_threads):
        thr = Thread(target=myfunc, args=(num_threads,i,mutex,barrier,counter))
        thread_list.append(thr)
        thr.start()

    for thr in thread_list:
        thr.join()
