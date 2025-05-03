import numpy as np
from parse_geometry import extract_optimized_coordinates
from parse import parse_frequencies_and_modes
import xml.etree.ElementTree as ET

def get_atomic_masses(xml_file):
    """
    Parse an XML file containing atomic masses and return a dictionary.
    """
    masses = {}
    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()
        for element in root:
            if element.text:
                masses[element.tag.strip()] = float(element.text.strip())
    except Exception as e:
        raise RuntimeError(f"Error parsing XML file '{xml_file}': {e}")
    return masses

def geometry_to_mass_weighted_cartesian(coords, atomic_masses):
    """Convert Cartesian geometry to mass-weighted Cartesian vector."""
    vec = []
    for atom, x, y, z in coords:
        sqrt_m = np.sqrt(atomic_masses[atom])
        vec.extend([x * sqrt_m, y * sqrt_m, z * sqrt_m])
    return np.array(vec)

def project_to_normal_modes(geometry_coords, normal_modes_matrix, atomic_masses):
    """Project the mass-weighted Cartesian geometry onto the normal mode basis."""
    mass_weighted_geom = geometry_to_mass_weighted_cartesian(geometry_coords, atomic_masses)
    Q = normal_modes_matrix.T @ mass_weighted_geom  # shape (n_modes,)
    return Q

def main():
    # === INPUT FILES ===
    geom_file = "/Users/harshsmac/Desktop/azulene_optimisation.out"
    freq_file = "/Users/harshsmac/Downloads/ezFCF-master/azulene_S0_freq.out"
    mass_xml = "/Users/harshsmac/Downloads/atomicMasses.xml"

    # === STEP 1: Get geometry and atom list ===
    coords = extract_optimized_coordinates(geom_file)
    atom_labels = [atom for atom, _, _, _ in coords]
    natoms = len(atom_labels)

    # === STEP 2: Parse frequencies and normal modes ===
    with open(freq_file, "r") as f:
        freq_text = f.read()

    frequencies, modes_list, mode_atom_labels = parse_frequencies_and_modes(freq_text, natoms)

    if atom_labels != mode_atom_labels:
        raise ValueError("Atom label mismatch between geometry and frequency file.")

    # === STEP 3: Build normal modes matrix (3N × N_modes) ===
    normal_modes_matrix = np.column_stack([mode.flatten() for mode in modes_list])

    # === STEP 4: Load atomic masses
    atomic_masses = get_atomic_masses(mass_xml)

    # === STEP 5: Project to normal coordinates
    Q = project_to_normal_modes(coords, normal_modes_matrix, atomic_masses)

    # === Output
    print("Mass-weighted normal coordinates (Q) for optimized geometry:")
    for i, q in enumerate(Q, 1):
        print(f"Mode {i:3d}: {q: .6e}")

if __name__ == "__main__":
    main()


