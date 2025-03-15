import json
import os
import math
import random

def split_json_file(input_file, output_dir, objects_per_file=100):
    """
    Split a large JSON file into multiple smaller minified files, each containing a 
    specified number of objects, and create an index mapping keys to their file locations.
    Also creates a doc.json with a single example item.
    
    Args:
        input_file (str): Path to the input JSON file
        output_dir (str): Directory to save output files
        objects_per_file (int): Number of objects per output file
    
    Returns:
        str: Path to the created index file
    """
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Load the large JSON file
    print(f"Loading JSON file: {input_file}")
    with open(input_file, 'r') as f:
        data = json.load(f)
    
    # Initialize index dictionary
    index = {}
    
    # Calculate number of output files
    total_objects = len(data)
    num_files = math.ceil(total_objects / objects_per_file)
    
    print(f"Splitting {total_objects} objects into {num_files} files, with {objects_per_file} objects per file")
    
    # Select a random key for the example document
    example_key = random.choice(list(data.keys()))
    example_data = {example_key: data[example_key]}
    
    # Create example document with pretty formatting
    doc_file = os.path.join(output_dir, "doc.json")
    with open(doc_file, 'w') as f:
        json.dump(example_data, f, indent=2)
    
    print(f"Created documentation file {doc_file} with an example item")
    
    # Process data in chunks
    keys = list(data.keys())
    for file_num in range(num_files):
        # Calculate start and end indices for current chunk
        start_idx = file_num * objects_per_file
        end_idx = min(start_idx + objects_per_file, total_objects)
        
        # Get keys for current chunk
        chunk_keys = keys[start_idx:end_idx]
        
        # Create chunk data dictionary
        chunk_data = {key: data[key] for key in chunk_keys}
        
        # Update index
        for key in chunk_keys:
            index[key] = file_num
        
        # Write chunk to file (minified - no indentation)
        output_file = os.path.join(output_dir, f"geometry_{file_num}.json")
        with open(output_file, 'w') as f:
            json.dump(chunk_data, f, separators=(',', ':'))
        
        print(f"Created minified file {output_file} with {len(chunk_keys)} objects")
    
    # Write index to file (minified)
    index_file = os.path.join(output_dir, "geometry_index.json")
    with open(index_file, 'w') as f:
        json.dump(index, f, separators=(',', ':'))
    
    print(f"Created minified index file {index_file} with {len(index)} entries")
    return index_file

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Split a large JSON file into smaller minified files with an index')
    parser.add_argument('input_file', help='Path to the input JSON file')
    parser.add_argument('--output-dir', default='split_output', help='Directory to save output files')
    parser.add_argument('--objects-per-file', type=int, default=100, help='Number of objects per output file')
    
    args = parser.parse_args()
    
    split_json_file(args.input_file, args.output_dir, args.objects_per_file)