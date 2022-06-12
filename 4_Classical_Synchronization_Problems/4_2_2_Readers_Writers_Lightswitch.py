#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2022 rzavalet <rzavalet@thinkbook>
#
# Distributed under terms of the MIT license.

"""
This program demostrates a solution to the readers-writers problem.
"""
from threading import *
from random import *
import time

class LightSwitch:
    def __init__(self):
        self.counter = 0
        self.mutex = Semaphore(1)

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

def writer(tid, roomEmpty, table):
    while True:
        roomEmpty.acquire()

        table[randint(0,4)] += 1
        print(f"Writer {tid}: ", table)

        roomEmpty.release()
        time.sleep(1)

def reader(tid, lightswitch, roomEmpty, table):
    while True:
        lightswitch.lock(roomEmpty)
        print(f"Reader {tid}: ", table)
        lightswitch.unlock(roomEmpty)
        time.sleep(1)

if __name__ == '__main__':

    num_writers = 1
    num_readers = 5
    thread_list = []
    table = [1, 2, 3, 4, 5]
    roomEmpty = Semaphore(1)
    lightswitch = LightSwitch()

    for i in range(num_writers):
        thr = Thread(target = writer, args = (i, roomEmpty, table, ))
        thread_list.append(thr)
        thr.start()


    for i in range(num_readers):
        thr = Thread(target = reader, args = (i, lightswitch, roomEmpty, table, ))
        thread_list.append(thr)
        thr.start()


    for thr in thread_list:
        thr.join()


