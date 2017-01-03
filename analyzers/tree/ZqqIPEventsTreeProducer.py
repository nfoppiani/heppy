from heppy.framework.analyzer import Analyzer
from heppy.statistics.tree import Tree
from ROOT import TFile
from heppy.analyzers.ntuple_mod import *

n_jet = 2


class ZqqIPEventsTreeProducer(Analyzer):

    def beginLoop(self, setup):
        super(ZqqIPEventsTreeProducer, self).beginLoop(setup)
        self.rootfile = TFile('/'.join([self.dirName,
                                        'tree.root']),
                              'recreate')
        self.tree = Tree( 'events', '')

        var(self.tree, 'quark_type')
        for ijet in range(n_jet):
            bookMyJet(self.tree, 'jet{}'.format(ijet+1))


        bookMyP4(self.tree, 'total_zed')
        bookMyP4(self.tree, 'zed_gen_stable')
        bookMyP4(self.tree, 'rec_zed')
        bookMyP4(self.tree, 'jets_zed')
        bookMyP4(self.tree, 'second_rec_zed')

        var(self.tree, 'gen_energy')
        var(self.tree, 'gen_charged')
        var(self.tree, 'gen_photon')
        var(self.tree, 'gen_neutral')

        var(self.tree, 'rec_energy')
        var(self.tree, 'rec_charged')
        var(self.tree, 'rec_photon')
        var(self.tree, 'rec_neutral')

        var(self.tree, 'delta_energy')
        var(self.tree, 'delta_charged')
        var(self.tree, 'delta_photon')
        var(self.tree, 'delta_neutral')

        var(self.tree, 'n_gen')
        var(self.tree, 'n_gen_charged')
        var(self.tree, 'n_gen_photon')
        var(self.tree, 'n_gen_neutral')

        var(self.tree, 'n_rec')
        var(self.tree, 'n_rec_charged')
        var(self.tree, 'n_rec_photon')
        var(self.tree, 'n_rec_neutral')

    def process(self, event):
        self.tree.reset()

        if hasattr(event, 'quark_type'):
            fill(self.tree, 'quark_type', event.quark_type)

        jets = getattr(event, self.cfg_ana.jets)
        for ijet, jet in enumerate(jets):
            if ijet == n_jet:
                break
            fillMyJet(self.tree, 'jet{}'.format(ijet+1), jet)


        total_zed = getattr(event, self.cfg_ana.total_zed)
        zed_gen_stable = getattr(event, self.cfg_ana.zed_gen_stable)
        rec_zed = getattr(event, self.cfg_ana.rec_zed)
        jets_zed = getattr(event, self.cfg_ana.jets_zed)
        second_rec_zed = getattr(event, self.cfg_ana.second_rec_zed)

        fillMyP4(self.tree, 'total_zed', total_zed)
        fillMyP4(self.tree, 'zed_gen_stable', zed_gen_stable)
        fillMyP4(self.tree, 'rec_zed', rec_zed)
        fillMyP4(self.tree, 'jets_zed', jets_zed)
        fillMyP4(self.tree, 'second_rec_zed', second_rec_zed)

        if hasattr(event, 'gen_energy'):

            fill(self.tree, 'gen_energy', event.gen_energy)
            fill(self.tree, 'gen_charged', event.gen_charged)
            fill(self.tree, 'gen_photon', event.gen_photon)
            fill(self.tree, 'gen_neutral', event.gen_neutral)

            fill(self.tree, 'rec_energy', event.rec_energy)
            fill(self.tree, 'rec_charged', event.rec_charged)
            fill(self.tree, 'rec_photon', event.rec_photon)
            fill(self.tree, 'rec_neutral', event.rec_neutral)

            fill(self.tree, 'delta_energy', event.delta_energy)
            fill(self.tree, 'delta_charged', event.delta_charged)
            fill(self.tree, 'delta_photon', event.delta_photon)
            fill(self.tree, 'delta_neutral', event.delta_neutral)

            fill(self.tree, 'n_gen', event.n_gen)
            fill(self.tree, 'n_gen_charged', event.n_gen_charged)
            fill(self.tree, 'n_gen_photon', event.n_gen_photon)
            fill(self.tree, 'n_gen_neutral', event.n_gen_neutral)

            fill(self.tree, 'n_rec', event.n_rec)
            fill(self.tree, 'n_rec_charged', event.n_rec_charged)
            fill(self.tree, 'n_rec_photon', event.n_rec_photon)
            fill(self.tree, 'n_rec_neutral', event.n_rec_neutral)

        self.tree.tree.Fill()

    def write(self, setup):
        self.rootfile.Write()
        self.rootfile.Close()
