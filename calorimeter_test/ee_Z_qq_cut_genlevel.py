'''
'''

import os
import copy
import heppy.framework.config as cfg

from heppy.framework.event import Event
Event.print_patterns=['sum*']

import logging
logging.shutdown()
reload(logging)
logging.basicConfig(level=logging.WARNING)

import random
random.seed(0xdeadbeef)

from heppy.configuration import Collider
Collider.BEAMS = 'ee'
Collider.SQRTS = 91.


comp_qq = cfg.Component(
    'qq_ILD_cut_genlevel',
    files = [
        'pythia_gen/ee_Z_had_91gev.root'
    ]
)

selectedComponents = [comp_qq]

number_jets = 2

from heppy.analyzers.fcc.Reader import Reader
source = cfg.Analyzer(
    Reader,
    gen_particles = 'GenParticle',
    gen_vertices = 'GenVertex'
)

from heppy.analyzers.Selector import Selector
gen_particles_stable = cfg.Analyzer(
    Selector,
    output = 'gen_particles_stable',
    input_objects = 'gen_particles',
    filter_func = lambda x : x.status()==1 and abs(x.pdgid()) not in [12,14,16] and x.pt()>1e-5
)


from sequences.CutGenLevelSequence import cut_gen_level_sequence

sequence = cfg.Sequence([
    source,
    gen_particles_stable,
    ])

sequence.extend(cut_gen_level_sequence)


from ROOT import gSystem
gSystem.Load("libdatamodelDict")
from EventStore import EventStore as Events

config = cfg.Config(
    components = selectedComponents,
    sequence = sequence,
    services = [],
    events_class = Events
)

if __name__ == '__main__':
    import sys
    from heppy.framework.looper import Looper
    import heppy.statistics.rrandom as random
    from heppy.papas.data.identifier import Identifier
    random.seed(0xdeadbeef)

    def process(iev=None):
        Identifier.reset()
        if iev is None:
            iev = loop.iEvent
        loop.process(iev)
        if display:
            display.draw()

    def next():
        loop.process(loop.iEvent+1)
        if display:
            display.draw()

    iev = None
    usage = '''usage: python analysis_ee_ZH_cfg.py [ievent]

    Provide ievent as an integer, or loop on the first events.
    You can also use this configuration file in this way:

    heppy_loop.py OutDir/ analysis_ee_ZH_cfg.py -f -N 100
    '''
    if len(sys.argv)==2:
        papas.display = True
        try:
            iev = int(sys.argv[1])
        except ValueError:
            print usage
            sys.exit(1)
    elif len(sys.argv)>2:
        print usage
        sys.exit(1)


    loop = Looper( 'looper', config,
                   nEvents=10,
                   nPrint=1,
                   timeReport=True)

    simulation = None
    for ana in loop.analyzers:
        if hasattr(ana, 'display'):
            simulation = ana
    display = getattr(simulation, 'display', None)
    simulator = getattr(simulation, 'simulator', None)
    if simulator:
        detector = simulator.detector
    if iev is not None:
        process(iev)
    else:
        loop.loop()
        loop.write()
