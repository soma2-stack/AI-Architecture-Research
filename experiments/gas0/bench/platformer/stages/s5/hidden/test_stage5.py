from platformer.geometry import Rect,intersection,overlap

def test_positive_area_still_collides_but_corner_contact_does_not():
    assert overlap(Rect(0,0,2,2),Rect(1,1,3,3))
    assert not overlap(Rect(0,0,1,1),Rect(1,1,2,2))

def test_intersection_uses_half_open_area():
    assert intersection(Rect(0,0,2,2),Rect(1,1,3,3))==Rect(1,1,2,2)
