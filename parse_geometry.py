def extract_optimized_coordinates(file_path):
    """
    Extracts only atom labels and their Cartesian coordinates (X, Y, Z) from the
    final 'Standard Nuclear Orientation' block after 'OPTIMIZATION CONVERGED'.
    
    Returns:
        coordinates (list of tuples): Each tuple is (Atom, X, Y, Z)
    """
    with open(file_path, "r") as f:
        lines = f.readlines()

    # Step 1: Find "OPTIMIZATION CONVERGED"
    opt_idx = None
    for idx, line in enumerate(lines):
        if "OPTIMIZATION CONVERGED" in line:
            opt_idx = idx
            break

    if opt_idx is None:
        raise ValueError("OPTIMIZATION CONVERGED not found in file.")

    # Step 2: Search for all "Standard Nuclear Orientation" blocks after convergence
    blocks = []
    i = opt_idx
    while i < len(lines):
        if "Standard Nuclear Orientation" in lines[i]:
            start = i + 3  # Skip header and dashed lines
            block = []
            for j in range(start, len(lines)):
                if lines[j].strip() == "":
                    break
                parts = lines[j].split()
                # Only keep lines that look like atomic coordinate lines
                if len(parts) == 5:
                    atom = parts[1]
                    try:
                        x = float(parts[2])
                        y = float(parts[3])
                        z = float(parts[4])
                        block.append((atom, x, y, z))
                    except ValueError:
                        continue  # skip malformed lines
            blocks.append(block)
            i = j  # jump ahead to after the block
        else:
            i += 1

    if not blocks:
        raise ValueError("No valid Standard Nuclear Orientation block found.")

    return blocks[-1]  # Return the *last* valid geometry block

def main():
    file_path = "/Users/harshsmac/Desktop/azulene_optimisation.out"
    coords = extract_optimized_coordinates(file_path)
    for atom, x, y, z in coords:
        print(f"{atom:2s}  {x:10.6f}  {y:10.6f}  {z:10.6f}")

if __name__ == "__main__":
    main()






