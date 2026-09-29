from platformer.geometry import Rect,intersection,overlap

def test_edge_contact_is_not_overlap():
    assert not overlap(Rect(0,0,1,1),Rect(1,0,2,1))
    assert intersection(Rect(0,0,1,1),Rect(1,0,2,1)) is None
