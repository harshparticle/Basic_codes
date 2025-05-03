The code plots adiabatic potential surfaces according to the potential matrix given by equation 
```math
V= \begin{pmatrix}
  A_1tanh(BR) & Ce^{-DR^{2}} \\
  Ce^{-DR^{2}} & A_2tanh(BR)
\end{pmatrix}
```
where $A_1$=0.01, B=0.06, C=0.001, D=1. In this case $A_2$ has been kept -0.01 to show avoided crossing, which can be changed according to problem definition. The python code is in the fiile adiabatic_potential.py, to see the plot it has bee provided in jupyter notebook file.

parse_geometry.py- This code parses geometry in cartesian coordinates from Q-Chem output.

parse.py- This code parses frequencies, normal mode vectors in cartesian coordinates from Q-chem output

normal_mode.py- This code is for converting normal modes in cartesian coordinates to normal mode coordinates

plot_new_spectrum_1.py- This code is for comparing convoluted spectra from ezFCF output.
