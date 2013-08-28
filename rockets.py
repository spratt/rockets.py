#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
import argparse

parser = argparse.ArgumentParser(
    description='Compare various rocket configurations')
parser.add_argument('--engines', default='engines.csv', nargs='?',
                   help='the csv of engine data')
parser.add_argument('--fuel_tanks', default='fuel_tanks.csv', nargs='?',
                   help='the csv of fuel tank data')
parser.add_argument('--payload', type=float, default=0.8, nargs='?',
                   help='the mass (in metric tons) of the payload')
parser.add_argument('--cost', type=int, default=600, nargs='?',
                   help='the cost (in ¤) of the payload')

args = parser.parse_args()
print args.engines, args.fuel_tanks, args.payload, args.cost
