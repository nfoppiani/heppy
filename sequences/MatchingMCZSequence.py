import heppy.framework.config as cfg

from heppy.analyzers.MCHistory import MCHistory
mc_history = cfg.Analyzer(
    MCHistory
)

#forse va fatto solo sui carichi?

from heppy.analyzers.Matcher import Matcher
rec_matching = cfg.Analyzer(
    Matcher,
    match_particles = 'rec_particles',
    particles = 'gen_particles_stable',
    delta_r = 0.01
)

gen_matching = cfg.Analyzer(
    Matcher,
    match_particles = 'gen_particles_stable',
    particles = 'rec_particles',
    delta_r = 0.01
)

from heppy.analyzers.ShowParticles import ShowParticles
show_particles = cfg.Analyzer(
    ShowParticles,
    gen_particles = 'gen_particles',
    rec_particles = 'rec_particles',
)

from heppy.analyzers.ShowMatching import ShowMatching
show_matching = cfg.Analyzer(
    ShowMatching,
    rec_particles = 'rec_particles',
    gen_particles_stable = 'gen_particles_stable',
)

from heppy.analyzers.ZDecayDetermination import ZDecayDetermination
zed_decay_determination = cfg.Analyzer(
    ZDecayDetermination,
    gen_particles = 'gen_particles',
    output = 'quark_type'
)

from heppy.analyzers.ShowVertices import ShowVertices
show_vertices = cfg.Analyzer(
    ShowVertices,
    rec_particles = 'rec_particles',
)

from heppy.analyzers.ChargeAndNeutralEnergy import ChargeAndNeutralEnergy
charge_neutral_energy = cfg.Analyzer(
    ChargeAndNeutralEnergy,
    rec_particles = 'rec_particles',
    gen_particles_stable = 'gen_particles_stable',
)


matching_mc_sequence = [
    mc_history,
    rec_matching,
    gen_matching,
    # show_particles,
    # show_matching,
    zed_decay_determination,
    # show_vertices,
    charge_neutral_energy
]
