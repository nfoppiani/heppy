from heppy.framework.analyzer import Analyzer

class ZDecayDetermination(Analyzer):
    '''
    from analyzers.ZDecayDetermination import ZDecayDetermination
    zed_decay_determination = cfg.Analyzer(
        ZDecayDetermination,
        gen_particles = 'gen_particles',
        output = 'quark_type'
    )

    '''

    def process(self, event):
        gen_particles = getattr(event, self.cfg_ana.gen_particles)


        for gen_ptc in gen_particles:
            if gen_ptc.pdgid() == 23 or abs(gen_ptc.pdgid()) == 11 :
                continue
            else:
                setattr(event, self.cfg_ana.output, abs(gen_ptc.pdgid()) )
                break
