from heppy.framework.analyzer import Analyzer
from heppy.utils.deltar import deltaR

class ShowMatching(Analyzer):
    '''WRITEEEE

    from analyzers.ShowMatching import ShowMatching
    show_matching = cfg.Analyzer(
        ShowMatching,
        rec_particles = 'rec_particles',
        gen_particles_stable = 'gen_particles_stable',
    )

    '''

    def process(self, event):
        gen_particles_stable = getattr(event, self.cfg_ana.gen_particles_stable)
        rec_particles = getattr(event, self.cfg_ana.rec_particles)

        print
        print
        print
        print "GEN PARTICLES"

        for i, gen_ptc in enumerate(gen_particles_stable):
            print
            print "particle ", i
            print gen_ptc
            print "match: ", gen_ptc.match
            if gen_ptc.match != None:
                print "dr= ", deltaR(gen_ptc.theta(), gen_ptc.phi(), gen_ptc.match.theta(), gen_ptc.match.phi())
                print "match of the match: ", gen_ptc.match.match
                if gen_ptc.match.match == gen_ptc:
                    print "match of the match OK"
                else:
                    print "match of the match NOT OK"
            print
        print
        print
        print
        print "REC PARTICLES"

        for i, rec_ptc in enumerate(rec_particles):
            print
            print "particle ", i
            print rec_ptc
            print "match: ", rec_ptc.match
            if rec_ptc.match != None:
                print "dr= ", deltaR(rec_ptc.theta(), rec_ptc.phi(), rec_ptc.match.theta(), rec_ptc.match.phi())
                print "match of the match: ", rec_ptc.match.match
                if rec_ptc.match.match == rec_ptc:
                    print "match of the match OK"
                else:
                    print "match of the match NOT OK"
            print
