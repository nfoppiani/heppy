import heppy.framework.config as cfg


from analyzers.ImpactParameterSimple import ImpactParameterSimple
from analyzers.ZqqIPTrackTreeProducer import ZqqIPTrackTreeProducer
from analyzers.ZqqIPJetsTreeProducer import ZqqIPJetsTreeProducer
from analyzers.ZqqIPJetsWithMCTreeProducer import ZqqIPJetsWithMCTreeProducer
from analyzers.ZqqIPEventsTreeProducer import ZqqIPEventsTreeProducer

# ILD detector
def track_selection_function(track):
    return track.q() != 0 and \
    abs(track.path.smeared_impact_parameter) < 2.5e-3 and \
    track.path.ip_resolution < 7.5e-4 and \
    track.e() > 0.4 # and \
    # track.path.min_dist_to_jet.Mag() < 7e-4 and \
    # track.path.min_dist_to_jet_significance < 10 and \
    # track.path.jet_point_min_approach.Mag() < 1e-2

import math
def ild_resolution(ptc):
    momentum = ptc.p3().Mag()
    theta = ptc.p4().Theta()
    # return math.sqrt(5.**2 + 10**2/ (momentum**2) )*1e-6
    return math.sqrt(5.**2 + 10.**2/ (momentum**2 * math.sin(theta)**3 ) )*1e-6

ip_simple_ild = cfg.Analyzer(
    ImpactParameterSimple,
    jets = 'jets',
    resolution = ild_resolution,
    track_selection = track_selection_function
)

tracks_tree_ild = cfg.Analyzer(
    ZqqIPTrackTreeProducer,
    jets = 'jets',
    track_selection = track_selection_function
)

def charged(track):
    return track.q() != 0
tracks_tree_ild_no_selection = cfg.Analyzer(
    ZqqIPTrackTreeProducer,
    jets = 'jets',
    track_selection = charged
)

jets_tree_ild = cfg.Analyzer(
    ZqqIPJetsTreeProducer,
    jets = 'jets',
)

mc_quarks_tree_ild = cfg.Analyzer(
    ZqqIPJetsWithMCTreeProducer,
    mc_Z_quarks = 'mc_Z_quarks',
)

events_tree_ild = cfg.Analyzer(
    ZqqIPEventsTreeProducer,
    jets = 'jets',
    total_zed = 'total_zed',
    zed_gen_stable = 'zed_gen_stable',
    rec_zed = 'rec_zed',
    jets_zed = 'jets_zed',
)

ild_tree_sequence = [
    # ip_simple_ild,
    # tracks_tree_ild,
    # tracks_tree_ild_no_selection,
    # jets_tree_ild,
    mc_quarks_tree_ild,
    events_tree_ild
]
