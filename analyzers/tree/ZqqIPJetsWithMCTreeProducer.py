from heppy.framework.analyzer import Analyzer
from heppy.statistics.tree import Tree
from ROOT import TFile
from heppy.analyzers.ntuple_mod import *


class ZqqIPJetsWithMCTreeProducer(Analyzer):

    def beginLoop(self, setup):
        super(ZqqIPJetsWithMCTreeProducer, self).beginLoop(setup)
        self.rootfile = TFile('/'.join([self.dirName,
                                        'tree.root']),
                              'recreate')
        self.tree = Tree( 'events', '')

        var(self.tree, 'quark_type')


        bookMyP4(self.tree, 'mc_quark')
        bookMyJet(self.tree, 'mc_quark_nearest_gen_jet' )
        var(self.tree, 'mc_quark_index_nearest_gen_jet' )
        var(self.tree, 'mc_quark_delta_alpha_wrt_nearest_gen_jet' )

        bookMyJet(self.tree, 'mc_quark_nearest_rec_jet' )
        var(self.tree, 'mc_quark_index_nearest_rec_jet' )
        var(self.tree, 'mc_quark_delta_alpha_wrt_nearest_rec_jet' )

        var(self.tree, 'delta_alpha_gen_rec_jet' )

    def process(self, event):
        self.tree.reset()

        if hasattr(event, 'quark_type'):
            fill(self.tree, 'quark_type', event.quark_type)

        mc_Z_quarks = event.mc_Z_quarks
        for quark in mc_Z_quarks:
            fillMyP4(self.tree, 'mc_quark', quark)
            fillMyJet(self.tree, 'mc_quark_nearest_gen_jet', quark.nearest_gen_jet)
            fill(self.tree, 'mc_quark_index_nearest_gen_jet', quark.index_nearest_gen_jet)
            fill(self.tree, 'mc_quark_delta_alpha_wrt_nearest_gen_jet', quark.delta_alpha_wrt_nearest_gen_jet)

            fillMyJet(self.tree, 'mc_quark_nearest_rec_jet', quark.nearest_rec_jet)
            fill(self.tree, 'mc_quark_index_nearest_rec_jet', quark.index_nearest_rec_jet)
            fill(self.tree, 'mc_quark_delta_alpha_wrt_nearest_rec_jet', quark.delta_alpha_wrt_nearest_rec_jet)

            fill(self.tree, 'delta_alpha_gen_rec_jet',quark.delta_alpha_gen_rec_jet )

            self.tree.tree.Fill()

    def write(self, setup):
        self.rootfile.Write()
        self.rootfile.Close()
