#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from FINDER_torch import FINDER

def main():
    dqn = FINDER()
    dqn.Train()


if __name__=="__main__":
    main()
