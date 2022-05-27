#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2022 rzavalet <rzavalet@thinkbook>
#
# Distributed under terms of the MIT license.

"""
This code demostrates the concept of barrier objects
"""

from threading import *

class Barrier:
    def __init__(self,n):
        self.n = n
        self.count = 0
        self.mutex = Semaphore(1)
        self.turnstile1 = Semaphore(0)
        self.turnstile2 = Semaphore(0)

    def phase1(self):
        self.mutex.acquire()
        self.count += 1
        if self.count == self.n:
            for i in range(self.n):
                self.turnstile1.release()
        self.mutex.release()

        self.turnstile1.acquire()

    def phase2(self):
        self.mutex.acquire()
        self.count -= 1
        if self.count == 0:
            for i in range(self.n):
                self.turnstile2.release()
        self.mutex.release()

        self.turnstile2.acquire()

    def wait(self):
        self.phase1()
        self.phase2()

def rendezvous(tid, i):
    print(f'Thread {tid} passed rendezvous {i}')

def myfunc(tid, b):
    for i in range(5):
        rendezvous(tid, i*2)
        b.phase1()
        rendezvous(tid, i*2 + 1)
        b.phase2()


if __name__ == '__main__':
    num_threads = 5
    b = Barrier(num_threads)
    thread_list = []

    for i in range(num_threads):
        thr = Thread(target = myfunc, args = (i,b,))
        thread_list.append(thr)
        thr.start()

    for thr in thread_list:
        thr.join()
        


