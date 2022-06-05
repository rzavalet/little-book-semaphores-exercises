#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2022 rzavalet <rzavalet@thinkbook>
#
# Distributed under terms of the MIT license.

"""
This is the improved solution to the producer-consumer problem. In this one, we
avoid a context switch in the consumer when counter becomes > 0, but still can
get the lock (e.g. another producer acquired it first)
"""
from threading import *
from random import *
from collections import deque
import time

def producer(mutex,events_queue,counter):
    while True:
        event = randint(0, 1000)

        mutex.acquire()
        events_queue.append(event)
        print(f"Appending event {event}")
        mutex.release()
        counter.release()
        time.sleep(1)

def consumer(mutex,events_queue, counter):
    while True:
        counter.acquire()

        mutex.acquire()
        event = events_queue.popleft()
        print(f'Poping event {event}')
        mutex.release()
        time.sleep(1)



if __name__ == '__main__':
    mutex = Semaphore(1)
    items = Semaphore(0)

    num_producers = 5
    num_consumers = 5
    thread_list = []
    events_queue = deque()
    seed(1)

    for i in range(num_producers):
        thr = Thread(target = producer, args = (mutex, events_queue, items,))
        thread_list.append(thr)
        thr.start()

    for i in range(num_consumers):
        thr = Thread(target = consumer, args = (mutex, events_queue, items,))
        thread_list.append(thr)
        thr.start()

    for i in thread_list:
        thr.join()

