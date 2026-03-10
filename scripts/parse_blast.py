import pandas as pd

# Load BLAST tabular output
df = pd.read_csv("results/blast_hits.tsv", sep="\t", header=None)
df.columns = ["qseqid","sseqid","pident","length","evalue","bitscore","stitle","staxids"]

# Save parsed CSV
df.to_csv("results/blast_hits_parsed.csv", index=False)
print("BLAST results saved to results/blast_hits_parsed.csv")
