from ROOT import TLorentzVector, TVector3

def pt_wrt_axis(axis, particles):
    # axis must be a TVector3 object
    total_momentum = TLorentzVector(0, 0, 0, 0)

    for particle in particles:
        total_momentum += particle.p4()

    return total_momentum.Perp(axis)
