import heppy.framework.config as cfg

from analyzers.ShowParticles import ShowParticles
show_particles = cfg.Analyzer(
    ShowParticles,
    gen_particles = 'gen_particles',
)

from analyzers.CutGeneratorLevel import CutGeneratorLevel
cut_generator_level = cfg.Analyzer(
    CutGeneratorLevel
)

from analyzers.TreeZqqGenLevel import TreeZqqGenLevel
tree_gen_level = cfg.Analyzer(
    TreeZqqGenLevel
)

cut_gen_level_sequence = [
    # show_particles,
    cut_generator_level,
    tree_gen_level,
]
