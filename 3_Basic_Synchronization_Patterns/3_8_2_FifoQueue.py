#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2022 rzavalet <rzavalet@thinkbook>
#
# Distributed under terms of the MIT license.

"""
This program implements a FIFO queue using semaphores.
I need to revisit this one. Not sure if I understood it correctly.
"""
from threading import *
from collections import deque
import time


class Fifo:
    def __init__(self):
        self.queue = deque()
        self.mutex = Semaphore(1)

    def wait(self, mySem):
        self.mutex.acquire()
        self.queue.append(mySem)
        self.mutex.release()

        mySem.acquire()
    
    def signal(self):
        self.mutex.acquire()
        sem = self.queue.popleft()
        self.mutex.release()

        sem.release()

    def count(self):
        self.mutex.acquire()
        num = len(self.queue)
        self.mutex.release()

        return num


def leaders(tid, mutex, counters, followerQueue, leaderQueue, mySem):
    while True:
        mutex.acquire()

        if counters[1] > 0:
            counters[1] -= 1
            followerQueue.signal()
        else:
            counters[0] += 1
            mutex.release()
            leaderQueue.wait(mySem)

        print(f"Leader {tid} is dancing");
        time.sleep(1)

        mutex.release()

def followers(tid, mutex, counters, followerQueue, leaderQueue, mySem):
    while True:
        mutex.acquire()

        if counters[0] > 0:
            counters[0] -= 1
            leaderQueue.signal()
        else:
            counters[1] += 1
            mutex.release()
            followerQueue.wait(mySem)

        print(f"Follower {tid} is dancing");
        time.sleep(1)


if __name__ == '__main__':
    mutex = Semaphore(1)
    counters = [0, 0]
    followerQueue = Fifo()
    leaderQueue = Fifo()

    num_threads = 2
    thread_list = []

    for i in range(num_threads):
        mySem = Semaphore(1)
        thr = Thread(target = leaders, args = (i, mutex, counters, followerQueue, leaderQueue, mySem,))
        thread_list.append(thr)
        thr.start()

    for i in range(num_threads):
        mySem = Semaphore(1)
        thr = Thread(target = followers, args = (i, mutex, counters, followerQueue, leaderQueue, mySem,))
        thread_list.append(thr)
        thr.start()

    for thr in thread_list:
        thr.join()
