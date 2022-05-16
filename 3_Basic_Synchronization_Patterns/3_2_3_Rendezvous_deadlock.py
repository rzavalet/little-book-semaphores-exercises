#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2022 rzavalet <rzavalet@thinkbook>
#
# Distributed under terms of the MIT license.

"""
This solution to Rendezvous will not work, because both threads
will keep waiting for the other one to signal it to proceed.
"""

from threading import *


def f1(tid, a1Arrived, b1Arrived):
    print(f'Thr {tid}: a1')
    b1Arrived.acquire()
    a1Arrived.release()
    print(f'Thr {tid}: a2')

def f2(tid, a1Arribed, b1Arrived):
    print(f'Thr {tid}: b1')
    a1Arrived.acquire()
    b1Arrived.release()
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


