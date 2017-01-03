'''
'''

import os
import copy
import heppy.framework.config as cfg

import logging
logging.shutdown()
reload(logging)
logging.basicConfig(level=logging.WARNING)

import random
random.seed(0xdeadbeef)

comp_qq = cfg.Component(
    'qq_ILD_spIP',
    files = [
        'pythia_gen/ee_Z_had_91gev.root'
    ]
)

selectedComponents = [comp_qq]

number_jets = 2

from heppy.analyzers.fcc.Reader import Reader
source = cfg.Analyzer(
    Reader,
    mode = 'ee',
    gen_particles = 'GenParticle',
    gen_vertices = 'GenVertex'
)

from sequences.PapasSequence_ILD import papas_sequence, detector, papas

from sequences.MatchingMCSequence import matching_mc_sequence

from sequences.JetsZSequence import jet_Z_sequence

from sequences.ILDTreeSequence_spIP import ild_tree_sequence

sequence = cfg.Sequence( [source] )
sequence.extend(papas_sequence)
sequence.extend(matching_mc_sequence)
sequence.extend(jet_Z_sequence(number_jets))
sequence.extend(ild_tree_sequence)


from ROOT import gSystem
gSystem.Load("libdatamodelDict")
from EventStore import EventStore as Events

config = cfg.Config(
    components = selectedComponents,
    sequence = sequence,
    services = [],
    events_class = Events
)
