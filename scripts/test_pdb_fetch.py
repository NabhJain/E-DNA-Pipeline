import os
import requests
import pandas as pd

# Function to fetch PDB
def fetch_pdb(pdb_id, save_dir='results/pdb_structures'):
    os.makedirs(save_dir, exist_ok=True)
    url = f'https://files.rcsb.org/download/{pdb_id}.pdb'
    r = requests.get(url)
    if r.status_code == 200:
        path = os.path.join(save_dir, f'{pdb_id}.pdb')
        with open(path, 'w') as f:
            f.write(r.text)
        print(f"Downloaded {pdb_id}")
        return pdb_id
    else:
        print(f"Failed to download {pdb_id}")
        return None

# Manual mapping of predicted species → PDB IDs
species_to_pdb = {
    "Flavipsychrobacter stenotrophus": "6G5Q",
    "Mixta intestinalis": "4YAJ",
    "Siccibacter colletis": "1BNA"
}

# Example predicted species (replace this with your actual predictions later)
predicted_species_list = [
    "Flavipsychrobacter stenotrophus",
    "Mixta intestinalis",
    "Siccibacter colletis"
]

# Collect results
results = []

for i, species in enumerate(predicted_species_list, start=1):
    pdb_id = species_to_pdb.get(species)
    if pdb_id:
        pdb_id = fetch_pdb(pdb_id)  # Download PDB structure
    else:
        print(f"No PDB mapping found for {species}")
        pdb_id = None

    results.append({
        "sequence_id": f"seq{i}",
        "predicted_species": species,
        "pdb_id": pdb_id
    })

# Save results to CSV
os.makedirs('results', exist_ok=True)
df = pd.DataFrame(results)
df.to_csv("results/new_predictions.csv", index=False)
print("Results saved to results/new_predictions.csv")
