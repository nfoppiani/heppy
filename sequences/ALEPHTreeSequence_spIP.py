"TODO: review, it does not work at the moment"

import heppy.framework.config as cfg


from analyzers.ImpactParameterSimple import ImpactParameterSimple
from analyzers.ZqqIPTrackTreeProducer import ZqqIPTrackTreeProducer
from analyzers.ZqqIPJetsTreeProducer import ZqqIPJetsTreeProducer
from analyzers.ZqqIPJetsWithMCTreeProducer import ZqqIPJetsWithMCTreeProducer
from analyzers.ZqqIPEventsTreeProducer import ZqqIPEventsTreeProducer

#ALEPH detector
def track_selection_function(track):
    return track.q() != 0 and \
    abs(track.path.smeared_impact_parameter) < 1e-2 and \
    track.path.ip_resolution < 7.5e-4 and \
    track.e() > 0.4 # and \
    # track.path.min_dist_to_jet.Mag() < 7e-4 and \
    # track.path.min_dist_to_jet_significance < 10 and \
    # track.path.jet_point_min_approach.Mag() < 1e-2

import math
def aleph_resolution(ptc):
    momentum = ptc.p3().Mag()
    return math.sqrt(25.**2 + 95.**2/ (momentum**2) )*1e-6

ip_simple_aleph = cfg.Analyzer(
    ImpactParameterSimple,
    jets = 'jets',
    method = 'simple',
    resolution = aleph_resolution,
    track_selection = track_selection_function
)

tracks_tree_aleph = cfg.Analyzer(
    ZqqIPTrackTreeProducer,
    jets = 'jets',
    track_selection = track_selection_function
)

def charged(track):
    return track.q() != 0
tracks_tree_aleph_no_selection = cfg.Analyzer(
    ZqqIPTrackTreeProducer,
    jets = 'jets',
    track_selection = charged
)

jets_tree_aleph = cfg.Analyzer(
    ZqqIPJetsTreeProducer,
    jets = 'jets',
)

mc_quarks_tree_aleph = cfg.Analyzer(
    ZqqIPJetsWithMCTreeProducer,
    mc_Z_quarks = 'mc_Z_quarks',
)

events_tree_aleph = cfg.Analyzer(
    ZqqIPEventsTreeProducer,
    jets = 'jets',
    # zed = 'zed'
    total_zed = 'total_zed',
    zed_gen_stable = 'zed_gen_stable',
    rec_zed = 'rec_zed',
    jets_zed = 'jets_zed',
    second_rec_zed = 'second_rec_zed',
    gen_energy = 'gen_energy',
    gen_charged = 'gen_charged',
    gen_photon = 'gen_photon',
    gen_neutral = 'gen_neutral',
    rec_energy = 'rec_energy',
    rec_charged = 'rec_charged',
    rec_photon = 'rec_photon',
    rec_neutral = 'rec_neutral',
)

aleph_tree_sequence = [
    ip_simple_aleph,
    tracks_tree_aleph,
    tracks_tree_aleph_no_selection,
    jets_tree_aleph,
    mc_quarks_tree_aleph,
    events_tree_aleph
]
