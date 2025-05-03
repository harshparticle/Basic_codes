import re
import numpy as np

def parse_frequencies_and_modes(qchem_output, natoms):
    """
    Parse vibrational frequencies and normal mode vectors from a Q-Chem frequency output.
    
    This function looks for:
      - Lines that start with "Frequency:" (case-insensitive) and extracts all numbers on those lines.
      - Blocks of displacement vectors that follow a header line containing groups 
        of "X Y Z". Each block is assumed to have 'natoms' lines.
    
    Additionally, it extracts the atom labels from the first block (assuming every
    block uses the same ordering).
    
    Parameters:
      qchem_output (str): The entire text of the Q-Chem frequency output.
      natoms (int): Number of atoms in the molecule.
      
    Returns:
      frequencies: A list of vibrational frequencies (floats, assumed to be in cm⁻¹).
      modes: A list of NumPy arrays, each of shape (natoms, 3), containing the displacement vectors.
      atom_labels: A list of atom labels (e.g., "C", "H") as they appear in the displacement blocks.
    """
    # ------------------
    # Extract frequencies.
    # ------------------
    freq_pattern = re.compile(r"^\s*Frequency:\s+(.+)$", re.MULTILINE | re.IGNORECASE)
    freq_matches = freq_pattern.findall(qchem_output)
    frequencies = []
    for line in freq_matches:
        for token in line.split():
            try:
                frequencies.append(float(token))
            except ValueError:
                continue

    # ------------------
    # Extract normal mode displacement blocks.
    # ------------------
    mode_header_re = re.compile(r"^\s*X\s+Y\s+Z(?:\s+X\s+Y\s+Z)+", re.MULTILINE)
    lines = qchem_output.splitlines()
    mode_blocks = []
    i = 0
    while i < len(lines):
        if mode_header_re.match(lines[i]):
            block = lines[i+1:i+1+natoms]
            mode_blocks.append(block)
            i += 1 + natoms
        else:
            i += 1

    # ------------------
    # Extract atom labels from the first mode block.
    # ------------------
    atom_labels = []
    if mode_blocks:
        for line in mode_blocks[0]:
            parts = line.split()
            if parts:
                # The very first token on each line is the atom's label.
                atom_labels.append(parts[0])
    
    # ------------------
    # Process each mode block to extract the displacement vectors.
    # ------------------
    modes = []
    for block in mode_blocks:
        if not block:
            continue
        # The first token on the first line is an atom label;
        # the remaining tokens are numerical values.
        tokens = block[0].split()
        num_values = len(tokens) - 1  # Exclude the atom label.
        group_count = num_values // 3  # each mode yields 3 numbers.
        # For each mode in this block, prepare an empty list.
        mode_group = [ [] for _ in range(group_count) ]
        for line in block:
            parts = line.split()
            try:
                # Convert the tokens (excluding the first one) to floats.
                numbers = list(map(float, parts[1:]))
            except ValueError:
                continue
            # Split the numbers into groups of 3 (x, y, z) for each mode.
            for k in range(group_count):
                vec = numbers[3*k : 3*(k+1)]
                mode_group[k].append(vec)
        # Convert each mode group to a NumPy array with shape (natoms, 3)
        for k in range(group_count):
            modes.append(np.array(mode_group[k]))
    
    return frequencies, modes, atom_labels

def main():
    # Update the file path below to point to your Q-Chem frequency output file.
    freq_file = "/Users/harshsmac/Downloads/ezFCF-master/azulene_S0_freq.out"
   
    # The number of atoms in the molecule 
    natoms = 18

    # Open and read the entire file content.
    with open(freq_file, 'r') as f:
        qchem_output = f.read()
   

    frequencies, modes, atom_labels = parse_frequencies_and_modes(qchem_output, natoms)

    if len(frequencies) != len(modes):
        print("Warning: Number of extracted frequencies ({}) does not equal number of mode blocks ({})."
              .format(len(frequencies), len(modes)))
    
    # Print out each vibrational mode's details.
    for mode_idx, (freq, mode) in enumerate(zip(frequencies, modes), start=1):
        print(f"Mode {mode_idx}: Frequency = {freq:.2f} cm⁻¹")
        print("Displacement vectors for each atom:")
        for i, vector in enumerate(mode):
            label = atom_labels[i] if i < len(atom_labels) else f"Atom {i+1}"
            x, y, z = vector
            print(f"  {label}: x = {x:.4f}, y = {y:.4f}, z = {z:.4f}")
        print("-" * 50)

if __name__ == "__main__":
    main()

