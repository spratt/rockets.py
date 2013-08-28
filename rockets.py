#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

# constants
Ag = 9.81 # acceleration due to gravity
Vs = 4500 # stable orbital speed

# parse command-line arguments
import argparse

parser = argparse.ArgumentParser(
    description='Compare various rocket configurations')
parser.add_argument('--engines', default='engines.csv', nargs='?',
                   help='the csv of engine data')
parser.add_argument('--fuel_tanks', default='fuel_tanks.csv', nargs='?',
                   help='the csv of fuel tank data')
parser.add_argument('--mass', type=float, default=0.8, nargs='?',
                   help='the mass (in metric tons) of the payload')
parser.add_argument('--cost', type=int, default=600, nargs='?',
                   help='the cost (in ¤) of the payload')

args = parser.parse_args()

# read from csv files
import csv
with open(args.engines,'rb') as engines_file:
    engines = [row for row in csv.DictReader(engines_file)]

with open(args.fuel_tanks,'rb') as tanks_file:
    tanks = [row for row in csv.DictReader(tanks_file)]

# generate every pair of a single engine and tank (a config)
configs = [(x,y) for x in engines for y in tanks]

# filter configs by ability to liftoff
def thrust(config):
    """ calculate the thrust of an engine in kilonewtons """
    return float(config[0]['thrust']) * 1000

def dry_mass(config):
    """ calculate the mass (without fuel) of a config in metric tons """
    return args.mass + float(config[0]['mass']) + float(config[1]['mass'])

def fuel_mass(config):
    """ calculate the fuel mass of a config in metric tons """
    return float(config[1]['fuel'])

def mass(config):
    """ calculate the mass of a config in metric tons """
    return dry_mass(config) + fuel_mass(config)

def Fg(config):
    """ calculate the weight of a config in kilonewtons """
    return mass(config)*Ag

configs = filter(lambda x: thrust(x) > Fg(x), configs)

# sort configs by specific impulse
configs = sorted(configs, key=lambda x: x[0]['impulse'])

# filter configs by ability to reach orbital speed
import math

def Isp(config):
    """ calculate the specific impulse of a config """
    return float(config[0]['impulse'])

def FtM(config):
    """ calculate the fuel mass to total mass ratio of a config """
    return fuel_mass(config) / mass(config)

def Ve(config):
    """ calculate the exhaust velocity of a config """
    return Isp(config) * Ag

def needed_FtM(config):
    """ calculate the needed fuel mass to total mass ratio of a config """
    return 1 - math.exp(-Vs/Ve(config))

configs = filter(lambda x: FtM(x) > needed_FtM(x), configs)

# print the remaining configs with their associated cost
def cost(config):
    """ calculate the cost of a config """
    return args.cost + int(config[0]['cost']) + int(config[1]['cost'])

configs = sorted(configs, key=lambda x: cost(x))

print "cost: engine + fuel tank"
for config in configs:
    print cost(config), '¤:', config[0]['name'], '+', config[1]['name']
