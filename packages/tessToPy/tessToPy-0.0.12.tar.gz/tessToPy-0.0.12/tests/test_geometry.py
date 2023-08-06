import unittest
import numpy as np
import copy
import tessToPy.geometry as tg
import tessToPy.tessIO as tio

class TestTessIO(unittest.TestCase):
    def setUp(self):
        self.lines = tio.read_tess('tess_files/n10-id1.tess')
        self.domain_size = np.array([1, 1, 1])
        self.verts = tio.get_verts(self.lines)
        self.edges = tio.get_edges(self.lines, self.verts)
        self.faces = tio.get_faces(self.lines, self.edges)
        self.polyhedrons = tio.get_polyhedrons(self.lines, self.faces)
        tio.get_periodicity(self.lines, self.verts, self.edges, self.faces)

    def test_read_verts(self):
        start_ind = self.lines.index(' **vertex\n')
        num_verts = int(self.lines[start_ind+1])
        line = self.lines[start_ind+2]
        id_ = int(line.split()[0])
        coord = np.array(list(map(float, line.split()[1:-1])))
        new_vert = tg.Vertex(id_, coord)
        self.assertEqual(new_vert.id_, self.verts[id_].id_)
        self.assertIsNone(np.testing.assert_allclose(new_vert.coord,  self.verts[id_].coord))
        self.assertEqual(num_verts, len(self.verts))

    def test_read_edges(self):
        start_ind = start_ind = self.lines.index(' **edge\n')
        num_edges = int(self.lines[start_ind + 1])
        line = self.lines[start_ind + 2]
        id_ = int(line.split()[0])
        edge_verts_id_ = list(map(int, line.split()[1:3]))
        test_edge_verts_id_ = [vert.id_ for vert in self.edges[id_].parts]
        self.assertEqual(edge_verts_id_, test_edge_verts_id_)
        self.assertEqual(num_edges, len(self.edges))

    def test_read_faces(self):
        start_ind = start_ind = self.lines.index(' **face\n')
        num_faces = int(self.lines[start_ind + 1])
        i=0
        vertex_line_ind = start_ind + 2 + i * 4
        edge_line_ind = vertex_line_ind + 1
        face_verts_id_ = [vid_ for vid_ in map(int, self.lines[vertex_line_ind].split()[2:])]
        face_edges_id_ = [eid_ for eid_ in map(int, self.lines[edge_line_ind].split()[1:])]
        id_ = int(self.lines[vertex_line_ind].split()[0])
        test_face_verts_id_ = [vert.id_ for vert in self.faces[id_].verts_in_face()]
        test_face_edges_id_ = [edge.id_ for edge in self.faces[id_].parts]
        self.assertEqual(set(face_verts_id_), set(test_face_verts_id_))
        self.assertEqual(set(face_edges_id_), set(test_face_edges_id_))
        self.assertEqual(num_faces, len(self.faces))

    def test_read_polys(self):
        start_ind = start_ind = self.lines.index(' **polyhedron\n')
        poly = self.polyhedrons[1]
        num_polys = int(self.lines[start_ind + 1])
        i = 0
        polyhedron_line_ind = start_ind + 2 + i
        id_ = int(self.lines[polyhedron_line_ind].split()[0])
        poly_faces = [fid_ for fid_ in map(int, self.lines[polyhedron_line_ind].split()[2:])]
        test_poly_faces = [face.id_ for face in poly.parts]
        self.assertEqual(set(test_poly_faces), set(poly_faces))
        self.assertEqual(id_, poly.id_)
        self.assertEqual(num_polys, len(self.polyhedrons))

    def test_read_periodicity(self):
        periodicity_start_ind = self.lines.index(' **periodicity\n')
        face_start_ind = periodicity_start_ind + self.lines[periodicity_start_ind:].index('  *face\n')
        line = self.lines[face_start_ind + 2]
        id_0 = int(line.split()[0])
        id_1 = int(line.split()[1])
        test_face_slaves = self.faces[id_0].master.id_
        face_slaves = id_1
        self.assertEqual(face_slaves, test_face_slaves)

    def test_read_domain_size(self):
        test_domain_size = tio.get_domain_size(self.lines)
        domain_size = self.domain_size
        self.assertIsNone(np.testing.assert_allclose(test_domain_size, domain_size))



class TestVertex(unittest.TestCase):
    def setUp(self):
        self.coords = np.array([[-0.133851269156, 1.099615654876, 0.112936431341],
                                [0.866148730844, 0.099615654876, 1.112936431341]])
        self.coords = np.array([[-0.133851269156, 1.099615654876, 0.112936431341],
                                [0.866148730844, 0.099615654876, 10.11293643134]])
        self.periodicity = np.array([-1, 1, -1])
        self.domain_size = [1,1,10]
        self.vertices = [tg.Vertex(0, self.coords[0]), tg.Vertex(1, list(self.coords[1]))]
        self.vertices[0].add_slave(self.vertices[1])

    def test_vector_to_master(self):
        offset = self.coords[0]-self.coords[1]
        vector_to_master = self.vertices[1].vector_to_master()
        self.assertIsNone(np.testing.assert_allclose(vector_to_master, offset))

    def test_periodicity_to_master(self):
        periodicity_to_master = self.vertices[1].periodicity_to_master()
        self.assertIsNone(np.testing.assert_equal(periodicity_to_master, self.periodicity))

    def test_no_master(self):
        self.assertRaises(Exception, self.vertices[0].vector_to_master)
        self.assertRaises(Exception, self.vertices[0].periodicity_to_master)


class TestEdge(unittest.TestCase):
    def setUp(self):
        self.lines = tio.read_tess('tess_files/n10-id1.tess')
        self.verts = tio.get_verts(self.lines)
        self.edges = tio.get_edges(self.lines, self.verts)
        self.faces = tio.get_faces(self.lines, self.edges)
        tio.get_periodicity(self.lines, self.verts, self.edges, self.faces)

    def test_xn(self):
        edge = self.edges[1]
        x0 = self.verts[edge.parts[0].id_].coord
        x1 = self.verts[edge.parts[1].id_].coord
        xm = (x0+x1)/2
        self.assertIsNone(np.testing.assert_allclose(edge.x0(), x0))
        self.assertIsNone(np.testing.assert_allclose(edge.x1(), x1))
        self.assertIsNone(np.testing.assert_allclose(edge.xm(), xm))

    def test_vector(self):
        edge = self.edges[1]
        x0 = self.verts[edge.parts[0].id_].coord
        x1 = self.verts[edge.parts[1].id_].coord
        vector = x1-x0
        self.assertIsNone(np.testing.assert_allclose(edge.vector(), vector))

    def test_length(self):
        edge = self.edges[1]
        x0 = self.verts[edge.parts[0].id_].coord
        x1 = self.verts[edge.parts[1].id_].coord
        vector = x1-x0
        length = np.sqrt(vector[0]**2+vector[1]**2+vector[2]**2)
        self.assertEqual(edge.length(), length)

    def test_vector_to_master(self):
        edge_a = self.edges[11]
        edge_b = self.edges[35]
        vector_to_master = edge_a.xm() - edge_b.xm()
        self.assertIsNone(np.testing.assert_allclose(edge_b.vector_to_master(), vector_to_master))

    def test_periodicity_to_master(self):
        edge_a = self.edges[11]
        edge_b = self.edges[35]
        vector_to_master = edge_a.xm() - edge_b.xm()
        periodicity_to_master = np.sign(vector_to_master)
        self.assertIsNone(np.testing.assert_allclose(edge_b.periodicity_to_master(), periodicity_to_master))

    def test_direction_relative_to_master(self):
        edge_b = self.edges[35]
        self.assertEqual(edge_b.direction_relative_to_master(), -1)
        self.assertEqual(edge_b.reverse().direction_relative_to_master(), 1)

    def test_edge_reverse(self):
        edge_a = self.edges[11]
        edge_a_rev = edge_a.reverse()
        self.assertIsNone(np.testing.assert_allclose(edge_a.vector(), -1*edge_a_rev.vector()))

    def test_replace_vertex(self):
        edge_a = self.edges[1]
        org_verts = [vert.id_ for vert in edge_a.parts]
        org_vector = edge_a.vector()
        new_vert = 5
        edge_a.replace_part(self.verts[new_vert], edge_a.parts[0])
        new_verts = org_verts[:]
        new_verts[0] = new_vert
        new_vector = self.verts[new_verts[1]].coord - self.verts[new_verts[0]].coord
        self.assertIsNone(np.testing.assert_allclose(edge_a.vector(), new_vector))
        edge_a.replace_part(self.verts[org_verts[0]], edge_a.parts[0])
        self.assertIsNone(np.testing.assert_allclose(edge_a.vector(), org_vector))

    def test_replace_vertex_reverse(self):
        edge_a = self.edges[1]
        org_verts = [vert.id_ for vert in edge_a.parts]
        edge_a_rev = self.edges[-1]
        new_vert = 5
        edge_a.replace_part(self.verts[new_vert], edge_a.parts[0])
        new_verts = org_verts[:]
        new_verts[0] = new_vert
        new_vector = self.verts[new_verts[1]].coord - self.verts[new_verts[0]].coord
        self.assertIsNone(np.testing.assert_allclose(edge_a_rev.vector(), -1*edge_a.vector()))
        edge_a.replace_part(self.verts[org_verts[0]], edge_a.parts[0])

    def test_master_slave_reverse(self):
        edge_a = self.edges[5]
        slaves = [edge.id_ for edge in edge_a.slaves]
        rev_edge_a = edge_a.reverse()
        rev_slaves = [edge.id_ for edge in rev_edge_a.slaves]
        self.assertEqual(set(slaves), set(rev_slaves))
        self.assertEqual(self.edges[115].master.id_, self.edges[-115].master.id_)

    def test_part_of(self):
        vert = self.verts[2]
        part_of_id = [1,2,11,187]
        test_part_of_id = [edge.id_ for edge in vert.part_of]
        self.assertEqual(part_of_id, test_part_of_id)

class TestFace(unittest.TestCase):
    def setUp(self):
        self.lines = tio.read_tess('tess_files/n10-id1.tess')
        self.verts = tio.get_verts(self.lines)
        self.edges = tio.get_edges(self.lines, self.verts)
        self.faces = tio.get_faces(self.lines, self.edges)
        tio.get_periodicity(self.lines, self.verts, self.edges, self.faces)
    def test_face_eq(self):
        start_ind = start_ind = self.lines.index(' **face\n')
        num_faces = int(self.lines[start_ind + 1])
        i=0
        vertex_line_ind = start_ind + 2 + i * 4
        face_eq_line_ind = vertex_line_ind + 2
        face_eq= np.array([num for num in map(float, self.lines[face_eq_line_ind].split())])
        id_ = int(self.lines[vertex_line_ind].split()[0])
        test_face_eq = self.faces[id_].face_eq()
        self.assertIsNone(np.testing.assert_allclose(test_face_eq, face_eq))

    def test_area(self):
        area = 0.248222484631 #Face 1
        test_area = self.faces[1].area()
        self.assertIsNone(np.testing.assert_allclose(area, test_area))

    def test_face_reverse(self):
        face = self.faces[1]
        edges = face.parts
        edges_rev = [edge.reverse().id_ for edge in edges[::-1]]
        test_face_rev = face.reverse()
        test_edges_rev = [edge.id_ for edge in test_face_rev.parts]
        self.assertEqual(edges_rev, test_edges_rev)
        face_eq = face.face_eq()
        test_face_eq = test_face_rev.face_eq()
        self.assertIsNone(np.testing.assert_allclose(face_eq, -1*test_face_eq))

    def test_edge_replace(self):
        face = self.faces[1]
        org_face_eq = face.face_eq()
        org_edge_id = face.parts[0].id_
        edge_copy = copy.copy(self.edges[org_edge_id])
        edge_copy.id_ = 9999
        edge_copy = edge_copy.reverse()
        face.replace_part(edge_copy, face.parts[0])
        new_face_eq = face.face_eq()
        face.replace_part(self.edges[org_edge_id], edge_copy)
        self.assertIsNone(np.testing.assert_allclose(org_face_eq, new_face_eq))

    def test_remove_edge(self):
        face = self.faces[1]
        org_edge_id = face.parts[0].id_
        face.remove_part(face.parts[0])
        face_list = set([edge.id_ for edge in face.parts])-set([org_edge_id])
        test_face_list = set([edge.id_ for edge in face.parts])
        self.assertEqual(face_list, test_face_list)
        self.faces = tio.get_faces(self.lines, self.edges)


    def test_periodicity(self):
        face = self.faces[5].slaves[0]
        periodicity = np.array([0,0,1])
        test_periodicity = face.periodicity_to_master()
        self.assertIsNone(np.testing.assert_allclose(periodicity, test_periodicity))

    def test_direction_relative_to_master(self):
        face = self.faces[5].slaves[0]
        test_direction_relative_to_master = face.direction_relative_to_master()
        direction_relative_to_master = -1
        self.assertEqual(direction_relative_to_master, test_direction_relative_to_master)

    def test_distance_to_master(self):
        face = self.faces[5].slaves[0]
        vector_to_master = self.faces[5].xm() - face.xm()
        test_vector_to_master = face.vector_to_master()
        self.assertIsNone(np.testing.assert_allclose(vector_to_master, test_vector_to_master))

class TestPolyhedron(unittest.TestCase):
    def setUp(self):
        self.lines = tio.read_tess('tess_files/n10-id1.tess')
        self.verts = tio.get_verts(self.lines)
        self.edges = tio.get_edges(self.lines, self.verts)
        self.faces = tio.get_faces(self.lines, self.edges)
        self.polyhedrons = tio.get_polyhedrons(self.lines, self.faces)
        tio.get_periodicity(self.lines, self.verts, self.edges, self.faces)

    def test_volume(self):
        volume = 0.07928624408155101 #Face 1
        test_volume = self.polyhedrons[1].volume()
        self.assertIsNone(np.testing.assert_allclose(volume, test_volume))

    def test_area(self):
        area = 1.1063351901193357
        test_area = self.polyhedrons[1].area()
        self.assertIsNone(np.testing.assert_allclose(area, test_area))


    def test_sphericity(self):
        sphericity = 0.8067320195905399
        test_sphericity = self.polyhedrons[1].sphericity()
        self.assertIsNone(np.testing.assert_allclose(sphericity, test_sphericity))

    def test_face_replace(self):
        poly = self.polyhedrons[1]
        org_face_id = poly.parts[0].id_
        org_volume = poly.volume()
        new_face = copy.copy(poly.parts[0])
        new_face = new_face.reverse()
        poly.replace_part(new_face, poly.parts[0])
        test_volume = poly.volume()
        self.assertIsNone(np.testing.assert_allclose(org_volume, test_volume))
        poly.replace_part(self.faces[org_face_id], new_face)

    def test_remove_face(self):
        poly = self.polyhedrons[1]
        org_face_id = poly.parts[0].id_
        poly.remove_part(self.faces[org_face_id])
        poly_list = set([edge.id_ for edge in poly.parts])-set([org_face_id])
        test_poly_list = set([face.id_ for face in poly.parts])
        self.assertEqual(poly_list, test_poly_list)
        self.polyhedrons = tio.get_polyhedrons(self.lines, self.faces)

if __name__ == '__main__':
    unittest.main()
