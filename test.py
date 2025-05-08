import pytest
from collections import defaultdict
from script import parse_fasta, generate_kmers, update_counts, process_sequence

def test_parse_fasta(tmp_path):
    """Test parsing a FASTA file."""
    file = tmp_path / "test.fa"
    file.write_text(">seq1\nATGC\n>seq2\nCGTA")
    assert parse_fasta(file) == ["ATGC", "CGTA"]

def test_generate_kmers():
    """Test generating k-mers and their subsequent characters."""
    sequence = "ATGTCTGTCTGAA"
    k = 2
    result = list(generate_kmers(sequence, k))
    expected = [
        ("AT", "G"), ("TG", "T"), ("GT", "C"), ("TC", "T"),
        ("CT", "G"), ("TG", "T"), ("GT", "C"), ("TC", "T"),
        ("CT", "G"), ("TG", "A"), ("GA", "A"), ("AA", None)
    ]
    assert result == expected

def test_update_counts():
    """Test updating k-mer and context dictionaries."""
    kmer_dict = defaultdict(int)
    context_dict = defaultdict(lambda: defaultdict(int))
    update_counts(kmer_dict, context_dict, "AT", "G")
    assert kmer_dict["AT"] == 1
    assert context_dict["AT"]["G"] == 1

def test_process_sequence():
    """Test processing a single sequence."""
    sequence = "ATGTCTGTCTGAA"
    k = 2
    kmer_dict, context_dict = process_sequence(sequence, k)
    expected_kmer_dict = {
        "AT": 1, "TG": 3, "GT": 2, "TC": 2, "CT": 2, "GA": 1, "AA": 1
    }
    expected_context_dict = {
        "AT": {"G": 1},
        "TG": {"T": 2, "A": 1},
        "GT": {"C": 2},
        "TC": {"T": 2},
        "CT": {"G": 2},
        "GA": {"A": 1}
    }
    assert kmer_dict == expected_kmer_dict
    assert context_dict == expected_context_dict