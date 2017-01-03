from heppy.framework.analyzer import Analyzer
from heppy.statistics.tree import Tree
from ROOT import TFile
from heppy.analyzers.ntuple_mod import *

n_jet = 2


class ZqqIPJetsTreeProducer(Analyzer):

    def beginLoop(self, setup):
        super(ZqqIPJetsTreeProducer, self).beginLoop(setup)
        self.rootfile = TFile('/'.join([self.dirName,
                                        'tree.root']),
                              'recreate')
        self.tree = Tree( 'events', '')

        var(self.tree, 'quark_type')

        bookMyJet(self.tree, 'jet')

        pName = "jet"
        var(self.tree, '{pName}_n_charged'.format(pName = pName))
        var(self.tree, '{pName}_m_inv_charged'.format(pName = pName))
        var(self.tree, '{pName}_angle_wrt_jet_dir_charged'.format(pName = pName))

        var(self.tree, '{pName}_n_signif_larger3'.format(pName = pName))
        var(self.tree, '{pName}_m_inv_signif_larger3'.format(pName = pName))
        var(self.tree, '{pName}_angle_wrt_jet_dir_larger3'.format(pName = pName))

    def process(self, event):
        self.tree.reset()

        if hasattr(event, 'quark_type'):
            fill(self.tree, 'quark_type', event.quark_type)

        jets = getattr(event, self.cfg_ana.jets)
        for ijet, jet in enumerate(jets):
            if ijet == n_jet:
                break
            fillMyJet(self.tree, 'jet', jet)

            pName = "jet"
            fill(self.tree, '{pName}_n_charged'.format(pName = pName), jet.n_charged)
            fill(self.tree, '{pName}_m_inv_charged'.format(pName = pName), jet.m_inv_charged)
            fill(self.tree, '{pName}_angle_wrt_jet_dir_charged'.format(pName = pName), jet.angle_wrt_jet_dir_charged)

            fill(self.tree, '{pName}_n_signif_larger3'.format(pName = pName), jet.n_signif_larger3)
            fill(self.tree, '{pName}_m_inv_signif_larger3'.format(pName = pName), jet.m_inv_signif_larger3)
            fill(self.tree, '{pName}_angle_wrt_jet_dir_larger3'.format(pName = pName), jet.angle_wrt_jet_dir_larger3)


            self.tree.tree.Fill()

    def write(self, setup):
        self.rootfile.Write()
        self.rootfile.Close()
