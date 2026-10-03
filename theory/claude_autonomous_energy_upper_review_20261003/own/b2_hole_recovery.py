"""Scalar off-cycle 'hole' recovery at large n under zero input: x -> tanh(a x + B*),
B* ~ 4.161e-5 (from b1 at n=1e8), H ~ 0.049951. Numerical illustration only."""
import math
B=4.161e-05; a=1-1e-8; H=0.049951
x=0.0; t=0; marks={}
while x<H*(1-1e-3):
    x=math.tanh(a*x+B); t+=1
    for f in (0.25,0.5,0.9):
        if f not in marks and x>=f*H: marks[f]=t
print('steps for a hole (h=0) to recover under zero input:',marks,'to 99.9%:',t)
x=0.0;p=1.0;S=0.0
for _ in range(200000):
    x=math.tanh(a*x+B); p*=a*(1-x*x); S+=p
print('effective transport sum along the recovering coordinate:',round(S,1),'vs at h*: 1/(1-a(1-H^2)) =',round(1/(1-a*(1-H*H)),1))
print('per-step cost of HOLDING the hole at 0 (input -B*):',B,' => steps held per unit energy R^2:',round(1/B**2))
