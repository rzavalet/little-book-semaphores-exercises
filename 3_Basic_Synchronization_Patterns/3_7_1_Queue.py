#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2022 rzavalet <rzavalet@thinkbook>
#
# Distributed under terms of the MIT license.

"""
This code demonstrates how to use semaphores to simulate a Queue
"""
from threading import *
import time

def leaders(tid, leaderQueue, followerQueue):
    while True:
        leaderQueue.release()
        followerQueue.acquire()
        print(f"Leader {tid} is dancing")
        time.sleep(1)

def followers(tid, leaderQueue, followerQueue):
    while True:
        followerQueue.release()
        leaderQueue.acquire()
        print(f"Follower {tid} is dancing")
        time.sleep(1)

if __name__ == '__main__':
    leaderQueue = Semaphore(0)
    followerQueue = Semaphore(0)

    threads_list = []

    for i in range(3):
        thr = Thread(target = leaders, args = (i, leaderQueue, followerQueue,))
        threads_list.append(thr)
        thr.start()

    for i in range(3):
        thr = Thread(target = followers, args = (i, leaderQueue, followerQueue,))
        threads_list.append(thr)
        thr.start()

    for i in threads_list:
        thr.join()


