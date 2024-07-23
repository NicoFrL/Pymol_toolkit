#Just drag and drop the scipt in Pymol, or load it through File > Run Script... or install it via plugging mannager
from pymol import cmd
import re

def find_motif(motif):
    # Get the sequence of the currently loaded protein
    seq = cmd.get_fastastr().split("\n")[1]
    
    # Find all occurrences of the motif
    matches = list(re.finditer(motif, seq))
    
    if not matches:
        print(f"Motif '{motif}' not found in the protein sequence.")
        return
    
    # Create selections for each occurrence
    for i, match in enumerate(matches, 1):
        start = match.start() + 1  # PyMOL uses 1-based indexing
        end = match.end()
        
        # Check if the selection name already exists
        base_name = f"motif{i}"
        selection_name = base_name
        suffix = 1
        
        while cmd.get_names("selections").count(selection_name) > 0:
            selection_name = f"{base_name}_{suffix}"
            suffix += 1
        
        # Create the selection
        cmd.select(selection_name, f"resi {start}-{end}")
        print(f"Created selection '{selection_name}' for residues {start}-{end}")

# Add the function to PyMOL's command set
cmd.extend("find_motif", find_motif)

print("Motif finder script loaded. Use 'find_motif motif_sequence' to search for motifs.")
print("\nUsage:")
print("1. To search for a simple motif:")
print("   PyMOL>find_motif KINR")
print("   This would search for the motif 'KINR' in your loaded protein structure.")
print("\n2. To search for a motif with spaces, enclose it in quotes:")
print("   PyMOL>find_motif \"KI NR\"")
print("\nThe script will create selections named motif1, motif2, etc. for each occurrence of the motif.")
