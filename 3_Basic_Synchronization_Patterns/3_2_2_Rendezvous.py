#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2022 rzavalet <rzavalet@thinkbook>
#
# Distributed under terms of the MIT license.

"""
This is a good solution to the Rendezvous problem.
It only requires one preemption of one of the threads.
"""

from threading import *


def f1(tid, a1Arrived, b1Arrived):
    print(f'Thr {tid}: a1')
    a1Arrived.release()
    b1Arrived.acquire()
    print(f'Thr {tid}: a2')

def f2(tid, a1Arribed, b1Arrived):
    print(f'Thr {tid}: b1')
    b1Arrived.release()
    a1Arrived.acquire()
    print(f'Thr {tid}: b2')

if __name__ == '__main__':

    a1Arrived = Semaphore(0)
    b1Arrived = Semaphore(0)

    thrA = Thread(target=f1, args=(0, a1Arrived, b1Arrived))
    thrB = Thread(target=f2, args=(1, a1Arrived, b1Arrived))

    thrB.start()
    thrA.start()

    thrA.join()
    thrB.join()


