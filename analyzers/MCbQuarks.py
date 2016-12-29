from heppy.framework.analyzer import Analyzer
from utils.delta_alpha import delta_alpha
from utils.second_smallest_number import second_smallest_number

class MCbQuarks(Analyzer):
    '''
    from analyzers.MCbQuarks import MCbQuarks
    mc_b_quarks = cfg.Analyzer(
      MCbQuarks,
      output = 'mc_b_quarks',
      jets = 'jets',
    )
    '''

    def process(self, event):

        gen_particles = event.gen_particles

        tops = []
        for gen_ptc in gen_particles:
            if abs(gen_ptc.pdgid()) == 6:
                tops.append(gen_ptc)

        mc_b_quarks = []

        for top in tops:
            for daughter in top.daughters:
                if abs(daughter.pdgid()) == 5:
                    mc_b_quarks.append(daughter)


        jets = getattr(event, self.cfg_ana.jets)
        for quark in mc_b_quarks:
            quark.delta_alpha_wrtJets = []
            for jet in jets:
                quark.delta_alpha_wrtJets.append(delta_alpha(quark, jet))

        index_nearest_jet1 = mc_b_quarks[0].delta_alpha_wrtJets.index(min(mc_b_quarks[0].delta_alpha_wrtJets))
        index_nearest_jet2 = mc_b_quarks[1].delta_alpha_wrtJets.index(min(mc_b_quarks[1].delta_alpha_wrtJets))


        if index_nearest_jet1 == index_nearest_jet2:
            if min(mc_b_quarks[0].delta_alpha_wrtJets) <= min(mc_b_quarks[1].delta_alpha_wrtJets):
                index_nearest_jet2 = second_smallest_number(mc_b_quarks[1].delta_alpha_wrtJets)[1]

            elif min(mc_b_quarks[0].delta_alpha_wrtJets) > min(mc_b_quarks[1].delta_alpha_wrtJets):
                index_nearest_jet1 = second_smallest_number(mc_b_quarks[0].delta_alpha_wrtJets)[1]


        mc_b_quarks[0].index_nearest_jet = index_nearest_jet1
        mc_b_quarks[0].nearest_jet = jets[index_nearest_jet1]
        mc_b_quarks[0].delta_alpha_wrt_nearest_jet = mc_b_quarks[0].delta_alpha_wrtJets[index_nearest_jet1]
        mc_b_quarks[1].index_nearest_jet = index_nearest_jet2
        mc_b_quarks[1].nearest_jet = jets[index_nearest_jet2]
        mc_b_quarks[1].delta_alpha_wrt_nearest_jet = mc_b_quarks[1].delta_alpha_wrtJets[index_nearest_jet2]

        for i, jet in enumerate(jets):
            if i == index_nearest_jet1:
                jet.mc_b_quark_index = 1
            elif i == index_nearest_jet2:
                jet.mc_b_quark_index = 2
            else:
                jet.mc_b_quark_index = 0

        setattr(event, self.cfg_ana.output, mc_b_quarks)
