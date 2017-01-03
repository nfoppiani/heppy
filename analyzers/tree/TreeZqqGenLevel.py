from heppy.framework.analyzer import Analyzer
from heppy.statistics.tree import Tree
from ROOT import TFile

from utils.my_ntuple import *

class TreeZqqGenLevel(Analyzer):

    def beginLoop(self, setup):
        super(TreeZqqGenLevel, self).beginLoop(setup)
        self.rootfile = TFile('/'.join([self.dirName,
                                        'tree.root']),
                              'recreate')
        self.tree = Tree( 'events', '')

        bookMyP4(self.tree, 'sum_particles_with_cut')
        bookMyP4(self.tree, 'sum_p4_low_thresholds')
        bookMyP4(self.tree, 'sum_p4_low_ecal_high_hcal_thresholds')
        bookMyP4(self.tree, 'sum_p4_high_thresholds')


    def process(self, event):
        self.tree.reset()

        sum_particles_with_cut = event.sum_particles_with_cut
        fillMyP4(self.tree, 'sum_particles_with_cut', sum_particles_with_cut)

        sum_p4_low_thresholds = event.sum_p4_low_thresholds
        fillMyP4(self.tree, 'sum_p4_low_thresholds', sum_p4_low_thresholds)

        sum_p4_low_ecal_high_hcal_thresholds = event.sum_p4_low_ecal_high_hcal_thresholds
        fillMyP4(self.tree, 'sum_p4_low_ecal_high_hcal_thresholds', sum_p4_low_ecal_high_hcal_thresholds)

        sum_p4_high_thresholds = event.sum_p4_high_thresholds
        fillMyP4(self.tree, 'sum_p4_high_thresholds', sum_p4_high_thresholds)

        self.tree.tree.Fill()

    def write(self, setup):
        self.rootfile.Write()
        self.rootfile.Close()
