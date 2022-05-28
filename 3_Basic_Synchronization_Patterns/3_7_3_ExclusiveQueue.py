#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2022 rzavalet <rzavalet@thinkbook>
#
# Distributed under terms of the MIT license.

"""
This code demonstrates how to use semaphores to simulate an Exclusive Queue
"""
from threading import *
import time

def leaders(counters, mutex, tid, leaderQueue, followerQueue):
    while True:
        mutex.acquire()
        if counters[1] > 0:
            counters[1] -= 1
            followerQueue.release()
        else:
            counters[0] += 1
            mutex.release()
            leaderQueue.acquire()

        print(f"Leader {tid} is dancing")
        time.sleep(1)

        mutex.release()

def followers(counters, mutex, tid, leaderQueue, followerQueue):
    while True:
        mutex.acquire()
        if counters[0] > 0:
            counters[0] -= 1
            leaderQueue.release()
        else:
            counters[1] += 1
            mutex.release()
            followerQueue.acquire()

        print(f"Follower {tid} is dancing")
        time.sleep(1)

if __name__ == '__main__':
    counters = [0, 0]
    mutex = Semaphore(1)
    leaderQueue = Semaphore(0)
    followerQueue = Semaphore(0)

    num_pairs = 3
    threads_list = []

    for i in range(num_pairs):
        thr = Thread(target = leaders, args = (counters, mutex, i, leaderQueue, followerQueue,))
        threads_list.append(thr)
        thr.start()

    for i in range(num_pairs):
        thr = Thread(target = followers, args = (counters, mutex, i, leaderQueue, followerQueue,))
        threads_list.append(thr)
        thr.start()

    for i in threads_list:
        thr.join()


