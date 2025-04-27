The code plots adiabatic potential surfaces according to the potential matrix given by equation 
```math
V= \begin{pmatrix}
  A_1tanh(BR) & Ce^{-DR^{2}} \\
  Ce^{-DR^{2}} & A_2tanh(BR)
\end{pmatrix}
```
where $A_1$=0.01, B=0.06, C=0.001, D=1. In this case $A_2$ has been kept -0.01 to show avoided crossing, which can be changed according to problem definition. The python code is in the fiile adiabatic_potential.py, to see the plot it has bee provided in jupyter notebook file.
