from heppy.framework.analyzer import Analyzer
from heppy.particles.tlv.resonance import Resonance


class ZedBuilder(Analyzer):
    '''
    from analyzers.ZedBuilder import ZedBuilder
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

    '''


    def process(self, event):
        gen_particles_stable_and_neutrinos = getattr(event, self.cfg_ana.gen_particles_stable_and_neutrinos)
        gen_particles_stable = getattr(event, self.cfg_ana.gen_particles_stable)
        rec_particles = getattr(event, self.cfg_ana.rec_particles)
        jets = getattr(event, self.cfg_ana.jets)
        papas_PFreconstruction_particles_list = getattr(event, self.cfg_ana.papas_PFreconstruction_particles_list)
        pdgid = self.cfg_ana.pdgid

        total_zed = Resonance(gen_particles_stable_and_neutrinos, pdgid)
        zed_gen_stable = Resonance(gen_particles_stable, pdgid)
        rec_zed = Resonance(rec_particles, pdgid)
        jets_zed = Resonance(jets, pdgid)
        second_rec_zed = Resonance(papas_PFreconstruction_particles_list, pdgid)

        setattr(event, self.cfg_ana.output1, total_zed)
        setattr(event, self.cfg_ana.output2, zed_gen_stable)
        setattr(event, self.cfg_ana.output3, rec_zed)
        setattr(event, self.cfg_ana.output4, jets_zed)
        setattr(event, self.cfg_ana.output5, second_rec_zed)
