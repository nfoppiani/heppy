import math
from scipy import constants
from ROOT import TVector3, TLorentzVector
import scipy.optimize
from numpy import sign
debug = False


class straight_line:
    # origin and direction are TVector3 objects
    def __init__(self, origin, direction):
        self.origin = origin
        self.direction = direction.Unit()

    def point_at_parameter(self, par):
        return self.origin + par * self.direction

    # point is a TVector3 object, returns a TVector3 starting from the point and going to the line
    def distance_from_point(self, point):
        # result is in the form w = origin + alpha*direction - point
        alpha = self.direction.Dot( ( point - self.origin ) )
        w =  self.point_at_parameter(alpha) - point
        return w


def velocity_at_time(helix, time):
    v_x = helix.v_over_omega.Y() * math.sin(helix.omega*time) * helix.omega \
        + helix.v_over_omega.X() * math.cos(helix.omega*time) * helix.omega
    v_y = - helix.v_over_omega.X() * math.sin(helix.omega*time) * helix.omega \
        + helix.v_over_omega.Y() * math.cos(helix.omega*time) * helix.omega
    v_z = helix.vz()
    return TVector3(v_x, v_y, v_z)

def compute_IP_wrt_direction(helix, primary_vertex, jet_direction):
    # primary_vertex and jet_direction are TVector3 objects

    helix.primary_vertex = primary_vertex
    helix.jet_direction = jet_direction
    # primary_vertex = v, jet_direction = j
    helix.jet_line = straight_line(helix.primary_vertex, helix.jet_direction)

    # D_j
    def jet_track_distance(time):
        helix_point = helix.point_at_time(time)
        jet_track_vector = helix.jet_line.distance_from_point(helix_point)
        return jet_track_vector.Mag()

    helix.min_approach = scipy.optimize.minimize_scalar(jet_track_distance, bracket = None, bounds = [-1e-11, 1e-11], args=(), method='bounded', tol=None, options={'disp': 0, 'maxiter': 1e5, 'xatol': 1e-20} )
    helix.min_approach_time = helix.min_approach.x

    if debug:
        print("time_min_approach")
        print helix.min_approach_time
        print

    # S_t
    helix.point_min_approach = helix.point_at_time(helix.min_approach_time)
    helix.velocity_min_approach = velocity_at_time(helix, helix.min_approach_time)
    helix.linearized_track = straight_line(helix.point_min_approach, helix.velocity_min_approach)

    if debug:
        print("point_min_approach")
        helix.point_min_approach.Dump()
        print
        print("velocity_min_approach")
        helix.velocity_min_approach.Dump()
        print
        print "distance between point min approach and jet dir"
        print jet_track_distance(helix.min_approach_time)
        print
    # S_j
    helix.jet_point_min_approach = helix.point_min_approach + helix.jet_line.distance_from_point(helix.point_min_approach)

    # if debug:
    #     print("helix.jet_line.distance_from_point(point_min_approach)")
    #     helix.jet_line.distance_from_point(point_min_approach).Dump()
    #     print
    #     print("jet_point_min_approach")
    #     jet_point_min_approach.Dump()
    #     print

    # D_j = S_t - S_j
    helix.min_dist_to_jet = helix.point_min_approach - helix.jet_point_min_approach
    # D
    helix.vector_impact_parameter = helix.linearized_track.distance_from_point(helix.primary_vertex)
    helix.s_j_minus_v_wrt_jet_dir = helix.jet_direction.Dot( helix.jet_point_min_approach - helix.primary_vertex )
    helix.sign_impact_parameter = sign( helix.s_j_minus_v_wrt_jet_dir )
    helix.s_j_wrt_pr_vtx = (helix.jet_point_min_approach - helix.primary_vertex).Mag() * helix.sign_impact_parameter
    # if debug:
    #     print("jet_point_min_approach - primary_vertex")
    #     (jet_point_min_approach - primary_vertex).Dump()
    #     print
    helix.impact_parameter = helix.vector_impact_parameter.Mag() * helix.sign_impact_parameter



def compute_IP(helix, primary_vertex, jet_direction):
    # primary_vertex and jet_direction are TVector3 objects

    helix.primary_vertex = primary_vertex
    helix.jet_direction = jet_direction.Unit()
    # primary_vertex = v, jet_direction = j

    def pr_vertex_track_distance(time):
        helix_point = helix.point_at_time(time)
        pr_vertex_track_vector = helix_point - helix.primary_vertex
        return pr_vertex_track_vector.Mag()

    helix.min_approach = scipy.optimize.minimize_scalar(pr_vertex_track_distance, bracket = None, bounds = [-1e-11, 1e-11], args=(), method='bounded', tol=None, options={'disp': 0, 'maxiter': 1e5, 'xatol': 1e-20} )
    helix.min_approach_time = helix.min_approach.x

    # D
    helix.vector_impact_parameter = helix.point_at_time(helix.min_approach_time) - helix.primary_vertex
    helix.ip_proj_jet_axis = helix.jet_direction.Dot( helix.vector_impact_parameter )
    helix.sign_impact_parameter = sign( helix.ip_proj_jet_axis )
    helix.impact_parameter = helix.vector_impact_parameter.Mag() * helix.sign_impact_parameter

# vertex displayer
from ROOT import TCanvas, TGraph, TEllipse, TLine
class vertex_displayer:

    def __init__(self, name, title, lenght, time_min, time_max, helix ):

        self.helix = helix

        self.c_transverse = TCanvas("c_tr_"+name, title)

        self.gr_transverse = TGraph()
        self.gr_transverse.SetNameTitle("g_tr_"+name, title)
        self.gr_transverse.SetPoint(0,0.,0.)
        self.gr_transverse.SetPoint(1,0.,lenght)
        self.gr_transverse.SetPoint(2,0.,-lenght)
        self.gr_transverse.SetPoint(3,lenght,0.)
        self.gr_transverse.SetPoint(4,-lenght,0.)
        self.gr_transverse.SetMarkerStyle(22)
        self.gr_transverse.SetMarkerColor(3)
        self.gr_transverse.GetXaxis().SetTitle("X axis")
        self.gr_transverse.GetYaxis().SetTitle("Y axis")

        # Drawing track
        # origin
        self.gr_transverse.SetPoint(5, helix.origin.X(), helix.origin.Y())
        # point_min = helix.point_at_time(time_min)
        # point_max = helix.point_at_time(time_max)
        # self.gr_transverse.SetPoint(6, point_min.X(), point_min.Y())
        # self.gr_transverse.SetPoint(7, point_max.X(), point_max.Y())

        # self.gr_transverse.SetPoint(6, helix.center_xy.X(), helix.center_xy.Y())
        # rho_min, z_min, phi_min = helix.polar_at_time(time_min)
        # rho_max, z_max, phi_max = helix.polar_at_time(time_max)
        # self.ell_transverse = TEllipse(helix.center_xy.X(), helix.center_xy.Y(), helix.rho, helix.rho,
        # 0, 360, 0)
        # #self.ell_transverse = TEllipse(helix.center_xy.X(), helix.center_xy.Y(), helix.rho, helix.rho, phi_min* 180 / math.pi, phi_max* 180 / math.pi, 0)
        # self.ell_transverse.SetLineColor(4)
        # self.ell_transverse.SetFillStyle(0)

        self.ell_transverse = TGraph()
        self.ell_transverse.SetNameTitle("g_ellipse_"+name, title)
        self.ell_transverse.SetMarkerStyle(7)
        self.ell_transverse.SetMarkerColor(1)
        n_points = 100
        for i in range(n_points):
            time_coord = time_min + i*(time_max-time_min)/n_points
            point = helix.point_at_time(time_coord)
            self.ell_transverse.SetPoint(i, point.X(), point.Y())

        # Linearized_track
        lin_track_x1 = self.helix.linearized_track.origin.X() - lenght * self.helix.linearized_track.direction.X()
        lin_track_x2 = self.helix.linearized_track.origin.X() + lenght * self.helix.linearized_track.direction.X()
        lin_track_y1 = self.helix.linearized_track.origin.Y() - lenght * self.helix.linearized_track.direction.Y()
        lin_track_y2 = self.helix.linearized_track.origin.Y() + lenght * self.helix.linearized_track.direction.Y()

        self.lin_track = TLine(lin_track_x1, lin_track_y1, lin_track_x2, lin_track_y2)
        self.lin_track.SetLineColor(2)
        self.lin_track.SetLineStyle(9)
        self.lin_track.SetLineWidth(2)

        # Jet_dir
        jet_dir_x1 = self.helix.primary_vertex.X() - lenght * self.helix.jet_direction.X()
        jet_dir_x2 = self.helix.primary_vertex.X() + lenght * self.helix.jet_direction.X()
        jet_dir_y1 = self.helix.primary_vertex.Y() - lenght * self.helix.jet_direction.Y()
        jet_dir_y2 = self.helix.primary_vertex.Y() + lenght * self.helix.jet_direction.Y()

        self.jet_dir = TLine(jet_dir_x1, jet_dir_y1, jet_dir_x2, jet_dir_y2)
        self.jet_dir.SetLineColor(6)
        self.jet_dir.SetLineStyle(1)
        self.jet_dir.SetLineWidth(1)

        # D_j: vector from S_j to S_t

        jet_track_distance_x1 = self.helix.jet_point_min_approach.X()
        jet_track_distance_y1 = self.helix.jet_point_min_approach.Y()
        jet_track_distance_x2 = self.helix.point_min_approach.X()
        jet_track_distance_y2 = self.helix.point_min_approach.Y()

        self.jet_track_distance = TLine(jet_track_distance_x1, jet_track_distance_y1, jet_track_distance_x2, jet_track_distance_y2)
        self.jet_track_distance.SetLineColor(3)
        self.jet_track_distance.SetLineStyle(3)
        self.jet_track_distance.SetLineWidth(4)

        # D

        impact_parameter_x1 = self.helix.primary_vertex.X()
        impact_parameter_y1 = self.helix.primary_vertex.Y()
        impact_parameter_x2 = self.helix.vector_impact_parameter.X()
        impact_parameter_y2 = self.helix.vector_impact_parameter.Y()

        self.impact_parameter = TLine(impact_parameter_x1, impact_parameter_y1, impact_parameter_x2, impact_parameter_y2)
        self.impact_parameter.SetLineColor(4)
        self.impact_parameter.SetLineStyle(6)
        self.impact_parameter.SetLineWidth(4)


    def draw(self):
        self.c_transverse.cd()
        self.c_transverse.SetGrid()
        self.gr_transverse.Draw("AP")
        self.ell_transverse.Draw("same LP")
        self.jet_dir.Draw("same")
        self.lin_track.Draw("same")
        self.jet_track_distance.Draw("same")
        self.impact_parameter.Draw("same")
