from platformer.geometry import Rect,overlap

def test_closed_edge_contact_counts_as_collision_in_legacy_geometry():
    assert overlap(Rect(0,0,1,1),Rect(1,0,2,1))
