from Bio import SeqIO

input_fastq = "qc/sample_trimmed.fastq"
output_fasta = "qc/sample_trimmed.fasta"

# Convert FASTQ to FASTA
SeqIO.convert(input_fastq, "fastq", output_fasta, "fasta")

print(f"Converted {input_fastq} to {output_fasta}")
