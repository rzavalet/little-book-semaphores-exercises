#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2022 rzavalet <rzavalet@thinkbook>
#
# Distributed under terms of the MIT license.

"""
In this program we show a producer-consumer using a buffer with a bounded size.
"""
from threading import *
from random import *
from collections import deque
import time

def producer(tid, mutex,events_queue,counter, haveSpace):
    while True:
        event = randint(0, 1000)
        haveSpace.acquire()

        mutex.acquire()
        events_queue.append(event)
        print(f"Producer {tid}: Appending event {event} (usage:{len(events_queue)})")
        mutex.release()
        counter.release()
        time.sleep(1)

def consumer(tid, mutex,events_queue, counter, haveSpace):
    while True:
        counter.acquire()

        mutex.acquire()
        event = events_queue.popleft()
        print(f'Consumer {tid}: Poping event {event}')
        mutex.release()

        haveSpace.release()
        time.sleep(5)



if __name__ == '__main__':
    mutex = Semaphore(1)
    items = Semaphore(0)
    max_length = 4
    haveSpace = Semaphore(max_length)

    num_producers = 5
    num_consumers = 5
    thread_list = []
    events_queue = deque()
    seed(1)

    for i in range(num_producers):
        thr = Thread(target = producer, args = (i, mutex, events_queue, items, haveSpace, ))
        thread_list.append(thr)
        thr.start()

    for i in range(num_consumers):
        thr = Thread(target = consumer, args = (i, mutex, events_queue, items, haveSpace, ))
        thread_list.append(thr)
        thr.start()

    for i in thread_list:
        thr.join()

