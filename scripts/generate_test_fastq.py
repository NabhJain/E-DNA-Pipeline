from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from Bio import SeqIO

def create_test_fastq(output_file="raw_data/test_sequences.fastq"):
    """Create properly formatted test FASTQ files"""
    
    # Real 16S rRNA sequences (shortened for demo)
    sequences = [
        "AGAGTTTGATCCTGGCTCAGGATGAACGCTAGCGGCAGGCTTAACACATGCAAGTCGAGCGGCAGCACGGGT",
        "TACGGAGGGTGCAAGCGTTAATCGGAATTACTGGGCGTAAAGCGCACGCAGGCGGTCTGTCAAGTCGGATGT", 
        "AACTGAAGAGTTTGATCATGGCTCAGATTGAACGCTGGCGGCAGGCCTAACACATGCAAGTCGAACGGTAAC"
    ]
    
    records = []
    for i, seq in enumerate(sequences, 1):
        # Create sequence record
        record = SeqRecord(
            Seq(seq),
            id=f"TEST_BAC_{i}",
            description="16S_rRNA_test_sequence"
        )
        
        # Add quality scores (same length as sequence)
        # 'I' represents high quality score (Phred+33 encoding)
        record.letter_annotations["phred_quality"] = [40] * len(seq)
        
        records.append(record)
    
    # Write to FASTQ file
    SeqIO.write(records, output_file, "fastq")
    print(f"Created properly formatted test file: {output_file}")
    print(f"Sequences: {len(records)}, Length: {len(sequences[0])} bp")

if __name__ == "__main__":
    create_test_fastq()