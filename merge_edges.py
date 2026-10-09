import pandas as pd
import glob
import os

DATA_DIR = "data"

#Find all edge files
pattern = os.path.join(DATA_DIR, "got-s*-edges.csv")
edge_files = sorted(glob.glob(pattern))

print("Found edge files:")
for f in edge_files:
    print("  -", f)



# Διαβάζουε&Ενώνουμε όλα τα edges
dfs = [pd.read_csv(f) for f in edge_files]
all_edges = pd.concat(dfs, ignore_index=True)


#Απλά test για int κυριως
if "Weight" not in all_edges.columns:
    raise SystemExit("Error1!!")

all_edges["Weight"] = all_edges["Weight"].astype(int)

#Undirected edges
all_edges["Node1"] = all_edges[["Source", "Target"]].min(axis=1)
all_edges["Node2"] = all_edges[["Source", "Target"]].max(axis=1)

# Ομαδοποίηση ανά ζευγάρι χαρακτήρων και άθροιση Weight
merged_edges = (
    all_edges
    .groupby(["Node1", "Node2"], as_index=False)["Weight"]
    .sum()
)

# Ξαναδίνουμε Source / Target
merged_edges = merged_edges.rename(columns={"Node1": "Source", "Node2": "Target"})

print(f"Total unique edges after merging: {len(merged_edges)}")


merged_edges = merged_edges[["Source", "Target", "Weight"]]

output_path = os.path.join(DATA_DIR, "got-all-seasons-edges.csv")
merged_edges.to_csv(output_path, index=False)

