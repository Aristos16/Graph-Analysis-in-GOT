import pandas as pd
import glob
import os

# Folder where the CSVs are
DATA_DIR = "data"


pattern = os.path.join(DATA_DIR, "got-s*-nodes.csv")
node_files = sorted(glob.glob(pattern))

print("Found node files:")
for f in node_files:
    print("  -", f)



# Read and stack all node CSVs
dfs = [pd.read_csv(f) for f in node_files]
all_nodes = pd.concat(dfs, ignore_index=True)

print(f"\nTotal rows before removing duplicates: {len(all_nodes)}")

#  Remove duplicates
all_nodes_unique = all_nodes.drop_duplicates(subset=["Id", "Label"])

print(f"Total unique characters after removing duplicates: {len(all_nodes_unique)}")

#Save
output_path = os.path.join(DATA_DIR, "got-all-seasons-nodes.csv")
all_nodes_unique.to_csv(output_path, index=False)


