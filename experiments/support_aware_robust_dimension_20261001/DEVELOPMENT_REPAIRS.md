# Pre-official development checks

First eight-test invocation passed six and failed two. The test imported NumPy
before the resource module set BLAS environment limits, so the loaded BLAS pool
was not one thread. Import resources first. The Neumann test incorrectly demanded
an interval lower endpoint equal exactly1; outward multiplication encloses1
with a two-ulp outward extension. Test containment instead. No certificate or
official endpoint result was collected. The failed test JSON and CPU charge
are preserved separately; scientific criteria are unchanged.
