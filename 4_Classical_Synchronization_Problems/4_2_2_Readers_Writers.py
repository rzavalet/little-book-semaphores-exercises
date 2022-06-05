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

def writer(tid, mutex, roomEmpty, table):
    while True:
        roomEmpty.acquire()

        table[randint(0,4)] += 1
        print(f"Writer {tid}: ", table)

        roomEmpty.release()
        time.sleep(1)

def reader(tid, mutex, roomEmpty, readers, table):
    while True:
        mutex.acquire()
        readers[0] += 1
        if readers[0] == 1:
            roomEmpty.acquire()
        mutex.release()

        print(f"Reader {tid}: ", table)

        mutex.acquire()
        readers[0] -= 1
        if readers[0] == 0:
            roomEmpty.release()
        mutex.release()
        time.sleep(1)

if __name__ == '__main__':

    num_writers = 1
    num_readers = 5
    thread_list = []
    table = [1, 2, 3, 4, 5]
    mutex = Semaphore(1)
    roomEmpty = Semaphore(1)
    readers = [0]

    for i in range(num_writers):
        thr = Thread(target = writer, args = (i, mutex, roomEmpty, table, ))
        thread_list.append(thr)
        thr.start()


    for i in range(num_readers):
        thr = Thread(target = reader, args = (i, mutex, roomEmpty, readers, table, ))
        thread_list.append(thr)
        thr.start()


    for thr in thread_list:
        thr.join()


