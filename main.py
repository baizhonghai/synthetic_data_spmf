import numpy as np
import random
import argparse
import os
from statistics import mean, stdev


# Function to generate a single sequence in SPMF format
def generate_sequence_spmf(mean_sentence_size, std_sentence_size,
                           mean_itemset_size, std_itemset_size,
                           item_universe_size):
    sentence_size = max(1, int(np.random.normal(mean_sentence_size, std_sentence_size)))
    sequence = []
    for _ in range(sentence_size):
        itemset_size = max(1, int(np.random.normal(mean_itemset_size, std_itemset_size)))
        itemset = random.sample(range(1, item_universe_size + 1), itemset_size)
        itemset_str = " ".join(str(item) for item in sorted(itemset))
        sequence.append(itemset_str + " -1")
    return " ".join(sequence) + " -2"


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Generate synthetic sequential dataset in SPMF format.")

    parser.add_argument('--num_sequences', type=int, default=50000, help='Number of sequences')
    parser.add_argument('--item_universe_size', type=int, default=200, help='Number of unique items')
    parser.add_argument('--mean_sentence_size', type=float, default=10.5, help='Mean number of itemsets per sequence') #10.5
    parser.add_argument('--std_sentence_size', type=float, default=1, help='Std dev of sentence size')
    parser.add_argument('--mean_itemset_size', type=float, default=3.5, help='Mean number of items per itemset')
    parser.add_argument('--std_itemset_size', type=float, default=1, help='Std dev of itemset size')
    parser.add_argument('--seed', type=int, default=42, help='Random seed (optional)')

    args = parser.parse_args()

    if args.seed is not None:
        np.random.seed(args.seed)
        random.seed(args.seed)

    # Generate dataset
    spmf_dataset = [
        generate_sequence_spmf(args.mean_sentence_size, args.std_sentence_size,
                               args.mean_itemset_size, args.std_itemset_size,
                               args.item_universe_size)
        for _ in range(args.num_sequences)
    ]

    # Analyze actual statistics of the generated dataset
    sentence_sizes = []
    itemset_sizes = []
    item_universe = set()

    for seq in spmf_dataset:
        itemsets = [s for s in seq.split(" -1") if s.strip() and "-2" not in s]
        sentence_sizes.append(len(itemsets))
        for itemset in itemsets:
            items = list(map(int, itemset.strip().split()))
            itemset_sizes.append(len(items))
            item_universe.update(items)

    actual_mean_sentence_size = mean(sentence_sizes)
    actual_std_sentence_size = stdev(sentence_sizes) if len(sentence_sizes) > 1 else 0.0

    actual_mean_itemset_size = mean(itemset_sizes)
    actual_std_itemset_size = stdev(itemset_sizes) if len(itemset_sizes) > 1 else 0.0

    actual_item_universe_size = len(item_universe)

    # Auto-generate output filename from parameters
    filename = (
        f"seq{args.num_sequences}"
        f"_u{args.item_universe_size}"
        f"_ss{args.mean_sentence_size:.1f}-{args.std_sentence_size:.2f}"
        f"_is{args.mean_itemset_size:.1f}-{args.std_itemset_size:.2f}"
        f"{f'_seed{args.seed}' if args.seed is not None else ''}.txt"
    )

    # Write dataset to file
    with open(filename, "w") as f:
        for sequence in spmf_dataset:
            f.write(sequence + "\n")

    # Print a sample of the dataset and actual stats
    print("\nSample sequences:")
    for line in spmf_dataset[:5]:
        print(line)

    print("\nActual stats from generated dataset:")
    print(f"  Mean sentence size (itemsets per sequence): {actual_mean_sentence_size:.2f}")
    print(f"  Std sentence size: {actual_std_sentence_size:.2f}")
    print(f"  Mean itemset size (items per itemset): {actual_mean_itemset_size:.2f}")
    print(f"  Std itemset size: {actual_std_itemset_size:.2f}")
    print(f"  Unique items used: {actual_item_universe_size}")
