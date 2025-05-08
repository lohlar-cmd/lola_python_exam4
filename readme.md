This repository contains a Python script to analyze k-mers and their contexts in genomic sequences stored in FASTA format. The script processes a file of sequence fragments (reads.fa), extracts k-mers and their subsequent characters for a user-specified value of `k`, and writes the results to an output file.

## Table of Contents
1. Usage
2. Explanation of Data Structures
3. Handling Edge Cases
4. Avoiding Overcounting or Missing Context
5. Testing
6. Submission Instructions

---

## Usage

To run the script, use the following command:

```
python script.py <input_file> <output_file> <k>
```

### Example:
```
python script.py reads.fa output.txt 4 
```

### Arguments:
- `<input_file>`: Path to the input FASTA file containing genomic sequences.
- `<output_file>`: Path to the output file where results will be written.
- `<k>`: Length of k-mers (e.g., `2` for substrings of length 2).

The output file will contain:
1. The total frequency of each k-mer.
2. The frequency of each character that comes immediately after the k-mer.

---

## Explanation of Data Structures

### 1. **K-mer Frequency Dictionary**
   - A dictionary where keys are k-mers and values are their frequencies.
   - Example:
     ```
     {"AT": 1, "TG": 3, "GT": 2, ...}
     ```

### 2. **Context Dictionary**
   - A nested dictionary where:
     - The outer key is the k-mer.
     - The inner key is the subsequent character.
     - The value is the count of occurrences.
   - Example:
     ```
     {
         "AT": {"G": 1},
         "TG": {"T": 2, "A": 1},
         ...
     }
     ```

These data structures ensure efficient storage and retrieval of k-mer frequencies and their contexts.

---

## Handling Edge Cases

### 1. **First and Last K-mers**
   - The first k-mer has no preceding context, and the last k-mer may not have a subsequent character.
   - Solution: Include all k-mers, even if they don’t have a subsequent character. For example, the last k-mer `"AA"` in the sequence `"ATGTCTGTCTGAA"` will have no subsequent character (`None`).

### 2. **Short Sequences**
   - If a sequence is shorter than `k`, it is skipped since no valid k-mers can be extracted.

### 3. **Invalid Input**
   - If the input file is missing or improperly formatted, the script exits with an error message.
   - If `k` is not a positive integer, the script exits with an error message.

---

## Avoiding Overcounting or Missing Context

1. **Overcounting**:
   - Each k-mer and its context are processed exactly once per occurrence in the input. This ensures accurate frequency counts.

2. **Missing Context**:
   - The `generate_kmers` function ensures that all k-mers are included, even if they don’t have a subsequent character. For example, the last k-mer in a sequence is still counted, with its subsequent character set to `None`.

3. **Modularity**:
   - The script is divided into multiple functions, each performing a single task. This ensures clarity and avoids unintended duplication of logic.

---

## Testing

The script includes thorough testing using `pytest`. To run the tests:

```
pytest test_script.py
```

### Test Coverage:
- Parsing FASTA files.
- Generating k-mers and their subsequent characters.
- Updating k-mer and context dictionaries.
- Processing sequences and handling edge cases.

All tests include typical and edge cases to ensure robustness.

---

## Repository Structure

The repository contains the following files:
1. **`script.py`**: Main Python script for k-mer analysis.
2. **`test_script.py`**: tests for the script.
3. **`README.txt`**: This document.
4. **`output txt`**: result from the script with an output of 2 and 5 k-mer.
---

## Additional Notes

- Ensure you have Python 3. installed on your system.
- Install `pytest` if not already installed:
  ```






 