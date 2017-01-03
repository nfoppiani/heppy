from heppy.framework.analyzer import Analyzer
from heppy.statistics.tree import Tree
from ROOT import TFile
from heppy.analyzers.ntuple_mod import *


class ZqqIPTrackTreeProducer(Analyzer):

    def beginLoop(self, setup):
        super(ZqqIPTrackTreeProducer, self).beginLoop(setup)
        self.rootfile = TFile('/'.join([self.dirName,
                                        'tree.root']),
                              'recreate')
        self.tree = Tree( 'events', '')

        var(self.tree, 'quark_type')

        bookMyParticle(self.tree, 'track')
        var(self.tree, 'ip')
        var(self.tree, 'ip_smeared')
        var(self.tree, 'sigma')
        var(self.tree, 'signif')

        var(self.tree, 'track_probability')

        var(self.tree, 'd_j')
        var(self.tree, 'd_j_signif')
        var(self.tree, 's_j_wrt_pr_vtx')

        var(self.tree, 'ip_proj_jet_axis')

        var(self.tree, 'x_prime')
        var(self.tree, 'y_prime')
        var(self.tree, 'x_prime_smeared')
        var(self.tree, 'y_prime_smeared')


    def process(self, event):
        self.tree.reset()

        if hasattr(event, 'quark_type'):
            fill(self.tree, 'quark_type', event.quark_type)

        jets = getattr(event, self.cfg_ana.jets)
        for jet in jets:
            for id, ptcs in jet.constituents.iteritems():
                for ptc in ptcs :
                    if self.cfg_ana.track_selection(ptc) == False:
                        continue

                    fillMyParticle(self.tree, 'track', ptc)
                    fill(self.tree, 'ip', ptc.path.impact_parameter)
                    fill(self.tree, 'ip_smeared', ptc.path.smeared_impact_parameter)
                    fill(self.tree, 'sigma', ptc.path.ip_resolution)
                    fill(self.tree, 'signif', ptc.path.significance_impact_parameter)
                    fill(self.tree, 'track_probability', ptc.path.track_probability)

                    if hasattr(ptc.path, 'min_dist_to_jet'):
                        fill(self.tree, 'd_j', ptc.path.min_dist_to_jet.Mag())
                        fill(self.tree, 'd_j_signif', ptc.path.min_dist_to_jet_significance)
                        fill(self.tree, 's_j_wrt_pr_vtx', ptc.path.s_j_wrt_pr_vtx )

                    if hasattr(ptc.path, 'ip_proj_jet_axis'):
                        fill(self.tree, 'ip_proj_jet_axis', ptc.path.ip_proj_jet_axis)

                    fill(self.tree, 'x_prime', ptc.path.x_prime)
                    fill(self.tree, 'y_prime', ptc.path.y_prime)
                    fill(self.tree, 'x_prime_smeared', ptc.path.x_prime_smeared)
                    fill(self.tree, 'y_prime_smeared', ptc.path.y_prime_smeared)




                    self.tree.tree.Fill()

    def write(self, setup):
        self.rootfile.Write()
        self.rootfile.Close()
