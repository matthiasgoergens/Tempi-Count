#!/usr/bin/python

from pprint import *
import graph

def rmChars(s, chars='*\n'):
    return ''.join([c for c in s if c not in chars])

def ignoreCoast (s):
    return s.split('/')[0]


def dictGraph(arcLines):
    d = {}
    for line in arcLines:
        lhs, rhs = line.lower().split('abuts')
        type, raw_fro = lhs.split()
        fro = ignoreCoast(raw_fro)
        tos = map(ignoreCoast, rhs.split())
        
        d[fro] = set(tos).union(d.setdefault(fro, set()))
#        print fro, tos
#    print
    return d

def fastGraph(g):
    dg = graph.digraph()
    for v in g:
        dg.add_node(v)
    for v in g:
        for w in g[v]:
            dg.add_edge(v,w)
    return dg

def calcTempi (graph, home, unit):
    tempi = min ([dg.shortest_path (v)[1][unit] for v in home])
    return tempi

        
def graphFromMap (s):
    return fastGraph(dictGraph ([rmChars(line) for line in s.split('\n')
                             if 'ABUTS' in line.upper()]))

def eval_positions(dg, buildSites, positions):
    for c, units in sorted(positions.items()):
        tempi = {}
        for unit in units:
            tempi[unit] = calcTempi(dg, buildSites[c], unit)
        st = sum(tempi.values())
        print (c + ': %(tempi)i\ttempi/unit: %(tpu).2f\tunits/tempi: %(upt).2f\tunits:%(units)i'
               % {'tempi': st, 'tpu': st/(len(units)+0.0),
                  'upt': (len(units)+0.0) / st, 'units':len(units)})
        for unit in sorted(units):
            print str(unit) + ': ' + str(tempi[unit]) + '\t',            
        print; print

# multiple union of sets
def mUnion(*s):
    if len(s)>0:
        return s[0].union(mUnion(*s[1:]))
    else:
        return set()

def eval_alliance (dg, buildSites, positions, alliance, name = None):
    if name is None:
        name = '-'.join(alliance)
    alliedPos = {name: mUnion(*[positions[ally] for ally in alliance])}
    alliedSites = {name: mUnion(*[buildSites[ally] for ally in alliance])}

    eval_positions(dg, alliedSites, alliedPos)

dg = graphFromMap (file('1900.map','r').read())

buildSites = {'austria': set(['vie','tri','bud']),
              'britain': set(['lon','edi','lvp']),
              'france': set(['bre','par','mar']),
              'germany': set(['mun', 'col', 'ber', 'kie']),
              'italy': set(['mil', 'rom', 'nap']),
              'russia': set(['stp', 'war', 'mos', 'sev', 'sib']),
              'turkey': set(['con', 'ank', 'dam']),}

positions = {'austria': set(['vie','ser','bud']),
             'britain': set(['bre','eng','edi','tys']),
             'france': set(['par', 'mor', 'bur', 'por', 'gib', 'alg']),
             'germany': set(['mun', 'nwy', 'bel', 'boh', 'ukr', 'lon', 'kie', 'nth', 'bal']),
             'italy': set(['swi', 'tyr', 'ven', 'ion', 'cyr', 'mao']),
             'russia': set(['stp', 'lvn', 'mos', 'gal', 'rum']),
             'turkey': set(['mac', 'bul', 'bla', 'arm', 'con'])}


def dtable(dg, buildSites):
    return dict([((country, pos) ,calcTempi (dg, buildSites[country], pos))
                 for pos in sorted(dg.nodes())
                 for country in buildSites])
def dToTable(nodes, countries, dtable):
    line1 = [''] + countries
    lines = [[node]+[dtable[country,node] for country in countries]
             for node in nodes]
    return [line1] + lines
    


t = dtable(dg, buildSites)
#pprint (t)


make_csv = False
if make_csv:
    import csv
    writer = csv.writer(open("some.csv", "wb"))
    writer.writerows(dToTable(sorted(dg.nodes()), sorted(buildSites.keys()), t))
    print 'done'

do_eval_pos = True

if do_eval_pos:
    eval_positions(dg, buildSites, positions)
    eval_alliance(dg, buildSites, positions, ['italy', 'turkey', 'france'])
    eval_alliance(dg, buildSites, positions, ['germany', 'britain', 'austria', 'russia'])

# TODO:
# naval graph for fleets
