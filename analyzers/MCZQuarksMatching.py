from heppy.framework.analyzer import Analyzer
from heppy.utils.delta_alpha import delta_alpha
from heppy.utils.second_smallest_number import second_smallest_number

class MCZQuarksMatching(Analyzer):
    '''
    from heppy.analyzers.MCZQuarksMatching import MCZQuarksMatching
    mc_Z_quarks = cfg.Analyzer(
      MCZQuarksMatching,
      output = 'mc_Z_quarks',
      jets = 'jets',
      gen_jets = 'gen_jets',
    )
    '''

    def process(self, event):
        gen_particles = event.gen_particles

        mc_Z_quarks = []

        for gen_ptc in gen_particles:
            if len(mc_Z_quarks) == 2:
                break
            if gen_ptc.pdgid() == 23 or abs(gen_ptc.pdgid()) == 11 :
                continue
            elif abs(gen_ptc.pdgid()) in [1, 2, 3, 4, 5] and gen_ptc.status() == 23:
                mc_Z_quarks.append(gen_ptc)

        if mc_Z_quarks[0].pdgid() * mc_Z_quarks[1].pdgid() >=0:
            import pdb; pdb.set_trace()

        rec_jets = getattr(event, self.cfg_ana.jets)
        gen_jets = getattr(event, self.cfg_ana.gen_jets)

        for quark in mc_Z_quarks:
            quark.delta_alpha_wrtGenJets = []
            quark.delta_alpha_wrtRecJets = []
            for gen_jet in gen_jets:
                quark.delta_alpha_wrtGenJets.append(delta_alpha(quark, gen_jet))
            for rec_jet in rec_jets:
                quark.delta_alpha_wrtRecJets.append(delta_alpha(quark, rec_jet))

        #gen-jet
        index_nearest_gen_jet1 = mc_Z_quarks[0].delta_alpha_wrtGenJets.index(min(mc_Z_quarks[0].delta_alpha_wrtGenJets))
        index_nearest_gen_jet2 = mc_Z_quarks[1].delta_alpha_wrtGenJets.index(min(mc_Z_quarks[1].delta_alpha_wrtGenJets))


        if index_nearest_gen_jet1 == index_nearest_gen_jet2:

            if min(mc_Z_quarks[0].delta_alpha_wrtGenJets) <= min(mc_Z_quarks[1].delta_alpha_wrtGenJets):
                index_nearest_gen_jet2 = second_smallest_number(mc_Z_quarks[1].delta_alpha_wrtGenJets)[1]

            elif min(mc_Z_quarks[0].delta_alpha_wrtGenJets) > min(mc_Z_quarks[1].delta_alpha_wrtGenJets):
                index_nearest_gen_jet1 = second_smallest_number(mc_Z_quarks[0].delta_alpha_wrtGenJets)[1]


        mc_Z_quarks[0].index_nearest_gen_jet = index_nearest_gen_jet1
        mc_Z_quarks[0].nearest_gen_jet = gen_jets[index_nearest_gen_jet1]
        mc_Z_quarks[0].delta_alpha_wrt_nearest_gen_jet = mc_Z_quarks[0].delta_alpha_wrtGenJets[index_nearest_gen_jet1]
        mc_Z_quarks[1].index_nearest_gen_jet = index_nearest_gen_jet2
        mc_Z_quarks[1].nearest_gen_jet = gen_jets[index_nearest_gen_jet2]
        mc_Z_quarks[1].delta_alpha_wrt_nearest_gen_jet = mc_Z_quarks[1].delta_alpha_wrtGenJets[index_nearest_gen_jet2]

        for i, jet in enumerate(gen_jets):
            if i == index_nearest_gen_jet1:
                jet.mc_quark_gen_index = 1
                jet.mc_quark = mc_Z_quarks[0]
            elif i == index_nearest_gen_jet2:
                jet.mc_quark_gen_index = 2
                jet.mc_quark = mc_Z_quarks[1]
            else:
                jet.mc_quark_gen_index = 0
                jet.mc_quark = None

        #rec-jet
        index_nearest_rec_jet1 = mc_Z_quarks[0].delta_alpha_wrtRecJets.index(min(mc_Z_quarks[0].delta_alpha_wrtRecJets))
        index_nearest_rec_jet2 = mc_Z_quarks[1].delta_alpha_wrtRecJets.index(min(mc_Z_quarks[1].delta_alpha_wrtRecJets))


        if index_nearest_rec_jet1 == index_nearest_rec_jet2:

            if min(mc_Z_quarks[0].delta_alpha_wrtRecJets) <= min(mc_Z_quarks[1].delta_alpha_wrtRecJets):
                index_nearest_rec_jet2 = second_smallest_number(mc_Z_quarks[1].delta_alpha_wrtRecJets)[1]

            elif min(mc_Z_quarks[0].delta_alpha_wrtRecJets) > min(mc_Z_quarks[1].delta_alpha_wrtRecJets):
                index_nearest_rec_jet1 = second_smallest_number(mc_Z_quarks[0].delta_alpha_wrtRecJets)[1]


        mc_Z_quarks[0].index_nearest_rec_jet = index_nearest_rec_jet1
        mc_Z_quarks[0].nearest_rec_jet = rec_jets[index_nearest_rec_jet1]
        mc_Z_quarks[0].delta_alpha_wrt_nearest_rec_jet = mc_Z_quarks[0].delta_alpha_wrtRecJets[index_nearest_rec_jet1]
        mc_Z_quarks[1].index_nearest_rec_jet = index_nearest_rec_jet2
        mc_Z_quarks[1].nearest_rec_jet = rec_jets[index_nearest_rec_jet2]
        mc_Z_quarks[1].delta_alpha_wrt_nearest_rec_jet = mc_Z_quarks[1].delta_alpha_wrtRecJets[index_nearest_rec_jet2]

        for i, jet in enumerate(rec_jets):
            if i == index_nearest_rec_jet1:
                jet.mc_quark_rec_index = 1
                jet.mc_quark = mc_Z_quarks[0]
            elif i == index_nearest_rec_jet2:
                jet.mc_quark_rec_index = 2
                jet.mc_quark = mc_Z_quarks[1]
            else:
                jet.mc_quark_rec_index = 0
                jet.mc_quark = None


        mc_Z_quarks[0].delta_alpha_gen_rec_jet = delta_alpha( mc_Z_quarks[0].nearest_rec_jet, mc_Z_quarks[0].nearest_gen_jet)
        mc_Z_quarks[1].delta_alpha_gen_rec_jet = delta_alpha( mc_Z_quarks[1].nearest_rec_jet, mc_Z_quarks[1].nearest_gen_jet)

        setattr(event, self.cfg_ana.output, mc_Z_quarks)
