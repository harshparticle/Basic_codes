#!/usr/bin/env python3

import sys,os

def main():
    """
    Usage:
        ./plot_spectrum_new.py file1.spectrum file2.spectrum ...
    All spectra will be plotted on one figure and saved to 'combined_spectrum.pdf' for example in this code which can be changed in line 89.
    """

    import matplotlib.pyplot as plt
    import spectral_tools_new as spt  
    import numpy as np

    # Gather all filenames from command-line arguments
    fnames = sys.argv[1:]
    if not fnames:
        print("Usage: ./plot_spectrum_new.py file1.spectrum [file2.spectrum ...]")
        sys.exit(1)

    # Figure setup
    width_inches = 8
    rect = (0.2, 0.2, 0.75, 0.75)
    fig = plt.figure(figsize=(width_inches, width_inches))
    ax = fig.add_axes(rect)

    # Define a Gaussian full width at half maximum (FWHM) in eV
    gauss_fwhm = 0.025
    print(f"A full width at half maximum of {gauss_fwhm} eV is used. Modify this if needed.")

    
    global_min_x = float('inf')
    global_max_x = -float('inf')
    global_max_y = 0.0

    # Loop over each spectrum file
    for fname in fnames:
        labels = []
        data = spt.read_data_with_labels(fname, labels)
        clean_label=os.path.basename(fname).replace(".spectrum_parallel","")

        # Get the lower/upper bounds of the energy from the raw data
        x_0 = round((data[0, 0] - 0.05)*10.0)/10.0
        npts = len(data[:, 0])
        x_end = round((data[npts - 1, 0] + 0.05)*10.0)/10.0

        # Define the grid for the convolved spectrum
        nx = 1000
        step = abs(x_end - x_0)/nx

        
        spectrum = spt.compute_spectrum(abs(x_0), abs(x_end), step,
                                        abs(data[:, 0]), data[:, 1],
                                        gauss_fwhm)

        # Update global min/max X
        global_min_x = min(global_min_x, abs(x_0))
        global_max_x = max(global_max_x, abs(x_end)+0.1)

        # Update global max Y
        local_max_y = max(spectrum[:, 1])
        global_max_y = max(global_max_y, local_max_y)

        # Plot the convolved spectrum
        ax.plot(spectrum[:, 0], spectrum[:, 1], '-', label=clean_label)

    # Determine a suitable Y-limit based on the global maximum
    if global_max_y < 10:
        ylim = round(global_max_y + 0.5)
    elif global_max_y < 100:
        ylim = round((global_max_y + 5)/10.0)*10
    else:
        ylim = round((global_max_y + 50)/100.0)*100

    # Set the final axes ranges
    ax.set_xlim(global_min_x, global_max_x)
    ax.set_ylim(0, ylim)
    

    # Labeling
    ax.set_xlabel('Energy, eV', fontsize=12)
    ax.set_ylabel('Intensity', fontsize=12)

    # Legend
    ax.legend(prop={"size":12},loc="upper right")

    # Save figure
    outname = "combined_spectrum.pdf"
    plt.savefig(outname)
    print(f"Saved combined plot to '{outname}'.")

# Standard boilerplate
if __name__ == '__main__':
    main()

