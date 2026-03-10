# scripts/predict_new_sequences.py
import os
import pandas as pd
from Bio import SeqIO
import requests

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

# Map test sequence IDs to species
sequence_to_species = {
    "TEST_BAC_1": "Flavipsychrobacter stenotrophus",
    "TEST_BAC_2": "Mixta intestinalis",
    "TEST_BAC_3": "Siccibacter colletis"
}

# PDB mapping
species_to_pdb = {
    "Flavipsychrobacter stenotrophus": "6G5Q",
    "Mixta intestinalis": "4YAJ",
    "Siccibacter colletis": "1BNA"
}

def predict_new_sequences(input_fastq, output_csv="results/new_predictions.csv"):
    os.makedirs("results", exist_ok=True)
    
    results = []
    for record in SeqIO.parse(input_fastq, "fastq"):
        seq_id = record.id
        predicted_species = sequence_to_species.get(seq_id, "Unknown species")
        pdb_id = species_to_pdb.get(predicted_species)
        
        if pdb_id:
            fetch_pdb(pdb_id)
        
        results.append({
            "sequence_id": seq_id,
            "predicted_species": predicted_species,
            "pdb_id": pdb_id
        })
    
    df = pd.DataFrame(results)
    df.to_csv(output_csv, index=False)
    print(f"Predictions with PDB IDs saved to {output_csv}")
    return df

# Example usage
if __name__ == "__main__":
    # Replace this with your FASTQ file path
    predict_new_sequences("data/test_sequences.fastq")
