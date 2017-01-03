import heppy.framework.config as cfg

def jet_Z_sequence(number_jets):
    from heppy.analyzers.fcc.JetClusterizer import JetClusterizer
    gen_jets = cfg.Analyzer(
        JetClusterizer,
        output = 'gen_jets',
        particles = 'gen_particles_stable',
        fastjet_args = dict( njets = 2)
    )
    jets = cfg.Analyzer(
        JetClusterizer,
        output = 'jets',
        particles = 'rec_particles',
        fastjet_args = dict( njets = 2)
    )

    from heppy.analyzers.MCZQuarksMatching import MCZQuarksMatching
    mc_Z_quarks = cfg.Analyzer(
      MCZQuarksMatching,
      output = 'mc_Z_quarks',
      jets = 'jets',
      gen_jets = 'gen_jets',
    )


    from heppy.analyzers.ZedBuilder import ZedBuilder
    zed = cfg.Analyzer(
        ZedBuilder,
        output1 = 'total_zed',
        output2 = 'zed_gen_stable',
        output3 = 'rec_zed',
        output4 = 'jets_zed',
        output5 = 'second_rec_zed',
        gen_particles_stable_and_neutrinos = 'gen_particles_stable_and_neutrinos',
        gen_particles_stable = 'gen_particles_stable',
        rec_particles = 'rec_particles',
        jets = 'jets',
        papas_PFreconstruction_particles_list = 'papas_PFreconstruction_particles_list',
        pdgid = 23
    )

    return [
        gen_jets,
        jets,
        mc_Z_quarks,
        zed
    ]
