import sys
from collections import defaultdict

def parse_fasta(file_path):
    """
    Parses a FASTA file and returns a list of sequences.
    
    Args:
        file_path (str): Path to the FASTA file.
    
    Returns:
        list: List of sequences.
    """
    sequences = []  # Initialize an empty list to store sequences
    with open(file_path, 'r') as file:  # Open the FASTA file in read mode
        sequence = ""  # Temporary variable to accumulate sequence lines
        for line in file:  # Iterate through each line in the file
            if line.startswith(">"):  # Check if the line is a header (starts with ">")
                if sequence:  # If a sequence has been accumulated, save it
                    sequences.append(sequence)
                    sequence = ""  # Reset the sequence accumulator
            else:
                sequence += line.strip()  # Append the current line to the sequence (remove whitespace)
        if sequence:  # After the loop, ensure the last sequence is saved
            sequences.append(sequence)
    return sequences  # Return the list of sequences


def generate_kmers(sequence, k):
    """
    Generates all k-mers and their subsequent characters from a sequence.
    
    Args:
        sequence (str): DNA sequence.
        k (int): Length of k-mers.
    
    Yields:
        tuple: (k-mer, next character or None).
    """
    # Loop over the sequence to extract k-mers and their subsequent characters
    for i in range(len(sequence) - k + 1):  # Ensure all k-mers, including the last one, are included
        kmer = sequence[i:i+k]  # Extract the k-mer starting at position i
        # Determine the next character after the k-mer, or None if there isn't one
        next_char = sequence[i+k] if i + k < len(sequence) else None
        yield kmer, next_char  # Yield the k-mer and its subsequent character


def update_counts(kmer_dict, context_dict, kmer, next_char):
    """
    Updates the k-mer frequency and context dictionaries.
    
    Args:
        kmer_dict (dict): Dictionary storing k-mer frequencies.
        context_dict (dict): Nested dictionary storing context frequencies.
        kmer (str): Current k-mer.
        next_char (str): Character following the k-mer.
    """
    kmer_dict[kmer] += 1  # Increment the count of the current k-mer
    if next_char is not None:  # Only update the context dictionary if there is a subsequent character
        context_dict[kmer][next_char] += 1  # Increment the count of the subsequent character


def process_sequence(sequence, k):
    """
    Processes a single sequence to compute k-mer and context frequencies.
    
    Args:
        sequence (str): DNA sequence.
        k (int): Length of k-mers.
    
    Returns:
        tuple: (k-mer frequency dictionary, context frequency dictionary).
    """
    # Initialize dictionaries to store k-mer frequencies and their contexts
    kmer_dict = defaultdict(int)  # Default dictionary for k-mer counts
    context_dict = defaultdict(lambda: defaultdict(int))  # Nested default dictionary for context counts
    
    # Generate k-mers and update the dictionaries
    for kmer, next_char in generate_kmers(sequence, k):
        update_counts(kmer_dict, context_dict, kmer, next_char)
    
    # Convert defaultdicts to regular dictionaries for output consistency
    return dict(kmer_dict), {k: dict(v) for k, v in context_dict.items()}


def write_output(output_file, kmer_dict, context_dict):
    """
    Writes the k-mer and context frequencies to an output file.
    
    Args:
        output_file (str): Path to the output file.
        kmer_dict (dict): Dictionary storing k-mer frequencies.
        context_dict (dict): Nested dictionary storing context frequencies.
    """
    # Write the results to the specified output file
    with open(output_file, 'w') as file:
        for kmer, freq in kmer_dict.items():  # Iterate through the k-mer frequencies
            file.write("{}: {}\n".format(kmer, freq))  # Write the k-mer and its frequency
            for next_char, count in context_dict.get(kmer, {}).items():  # Get the context for the k-mer
                file.write("  -> {}: {}\n".format(next_char, count))  # Write the subsequent character and its count


def main():
    """
    Main function to orchestrate the workflow.
    """
    # Validate command-line arguments
    if len(sys.argv) != 4:  # Ensure exactly three arguments are provided
        print("Usage: python script.py <input_file> <output_file> <k>")
        sys.exit(1)  # Exit with an error code if arguments are invalid
    
    input_file = sys.argv[1]  # Input FASTA file path
    output_file = sys.argv[2]  # Output file path
    try:
        k = int(sys.argv[3])  # Parse the value of k as an integer
    except ValueError:  # Handle cases where k is not a valid integer
        print("Error: k must be an integer.")
        sys.exit(1)  # Exit with an error code if k is invalid
    
    # Parse the input FASTA file to extract sequences
    sequences = parse_fasta(input_file)
    
    # Initialize dictionaries to aggregate results across all sequences
    kmer_dict = defaultdict(int)  # Aggregate k-mer frequencies
    context_dict = defaultdict(lambda: defaultdict(int))  # Aggregate context frequencies
    
    # Process each sequence and update the aggregated dictionaries
    for sequence in sequences:
        seq_kmer_dict, seq_context_dict = process_sequence(sequence, k)  # Process the current sequence
        for kmer, freq in seq_kmer_dict.items():  # Update k-mer frequencies
            kmer_dict[kmer] += freq
        for kmer, next_chars in seq_context_dict.items():  # Update context frequencies
            for next_char, count in next_chars.items():
                context_dict[kmer][next_char] += count
    
    # Write the aggregated results to the output file
    write_output(output_file, dict(kmer_dict), {k: dict(v) for k, v in context_dict.items()})


if __name__ == "__main__":
    main()  # Execute the main function when the script is run directly