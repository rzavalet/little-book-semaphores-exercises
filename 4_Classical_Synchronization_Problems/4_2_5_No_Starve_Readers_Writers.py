#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2022 rzavalet <rzavalet@thinkbook>
#
# Distributed under terms of the MIT license.

"""
The solution for the readers writers described in the exercise 4_2_2 has a
weakness: The writers may starve because while one of the threads is performing
the actual read, the writer is waiting for the 'roomEmpty' mutex to be
released. But at that point, other readers may come in, impeding the readers
count to become 0, thus preventing the release of the 'roomEmpty' mutex.

To prevent starvation, we can add another semaphore that acts as a turnstile.
Writers can lock the turnstile, forcing incoming readers to queue behind it.
"""

from threading import *
from random import *
import time

"""
LigthSwitch construct
=======================
The first thread to enter the room will hold a mutex. The last thread to leave
the room will release the mutex.
"""
class LightSwitch:
    def __init__(self):
        self.mutex = Semaphore(1)
        self.counter = 0

    def lock(self, semaphore):
        self.mutex.acquire()
        self.counter += 1
        if self.counter == 1:
            semaphore.acquire()
        self.mutex.release()

    def unlock(self, semaphore):
        self.mutex.acquire()
        self.counter -= 1
        if self.counter == 0:
            semaphore.release()
        self.mutex.release()

"""
Driver function for the writer thread. To avoid starvation, the writer takes a
mutex that acts as a turnstile. And only releases it once it is able to acquire
the roomEmpty mutex.

Other threads will queue at the turnstile. When the writer releases the
turnstile, the scheduler will signal one of the waiting threads. Unfortunately,
we don't have control over that.
"""
def writer(tid, turnstile, roomEmpty, table):
    while True:
        turnstile.acquire()
        roomEmpty.acquire()
        table[randint(0,4)] += 1
        print(f"Writer {tid}: ", table)
        turnstile.release()
        roomEmpty.release()
        time.sleep(1)


"""
Driver function for the reader thread. It has to go through a turnstile, which
may be locked by a writer. That prevents that writers starve.
"""
def reader(tid, lightswitch, turnstile, roomEmpty, table):
    while True:
        turnstile.acquire()
        turnstile.release()

        lightswitch.lock(roomEmpty)
        print(f"Reader {tid}: ", table)
        lightswitch.unlock(roomEmpty)
        time.sleep(1)



if __name__ == '__main__':
    num_writers = 5
    num_readers = 5

    thread_list = []
    table = [1, 2, 3, 4, 5]

    roomEmpty = Semaphore(1)
    turnstile = Semaphore(1)
    lightswitch = LightSwitch()

    for i in range(num_writers):
        thr = Thread(target = writer, args = (i, turnstile, roomEmpty, table,))
        thread_list.append(thr)
        thr.start()

    for i in range(num_readers):
        thr = Thread(target = reader, args = (i, lightswitch, turnstile, roomEmpty, table,))
        thread_list.append(thr)
        thr.start()

    for thr in thread_list:
        thr.join()





