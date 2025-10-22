#!/usr/bin/env python3
"""
Sync and convert TON jetton metadata from YAML to JSON format.
This script clones the ton-assets repository and converts all jetton YAML files
into a single JSON file for easy consumption.
"""

import os
import json
import yaml
import tempfile
import shutil
from pathlib import Path
from typing import Dict, List, Any
import subprocess


def clone_ton_assets(temp_dir: str) -> str:
    """Clone the ton-assets repository to a temporary directory."""
    repo_url = "https://github.com/tonkeeper/ton-assets.git"
    print(f"Cloning {repo_url}...")
    
    subprocess.run(
        ["git", "clone", "--depth", "1", "--single-branch", repo_url, temp_dir],
        check=True,
        capture_output=True
    )
    
    jettons_path = os.path.join(temp_dir, "jettons")
    if not os.path.exists(jettons_path):
        raise FileNotFoundError(f"Jettons directory not found in repository: {jettons_path}")
    
    return jettons_path


def convert_yaml_to_dict(yaml_file: Path) -> Dict[str, Any]:
    """Convert a single YAML file to a dictionary."""
    with open(yaml_file, 'r', encoding='utf-8') as f:
        try:
            data = yaml.safe_load(f)
            if data is None:
                return {}
            return data
        except yaml.YAMLError as e:
            print(f"Warning: Failed to parse {yaml_file}: {e}")
            return {}


def process_jettons_directory(jettons_path: str) -> Dict[str, Any]:
    """Process all YAML files in the jettons directory."""
    jettons_data = {}
    jettons_dir = Path(jettons_path)
    skipped_count = 0
    duplicate_count = 0
    
    # Find all YAML files
    yaml_files = list(jettons_dir.glob("**/*.yaml")) + list(jettons_dir.glob("**/*.yml"))
    
    print(f"Found {len(yaml_files)} YAML files")
    
    for yaml_file in yaml_files:
        relative_path = yaml_file.relative_to(jettons_dir)
        
        # Convert YAML to dict or list
        data = convert_yaml_to_dict(yaml_file)
        
        if not data:
            continue
        
        # Handle arrays of jettons
        if isinstance(data, list):
            print(f"Processing array in {relative_path} ({len(data)} items)")
            for item in data:
                if not isinstance(item, dict):
                    continue
                
                symbol = item.get('symbol')
                if not symbol:
                    continue
                
                # Handle duplicate symbols
                if symbol in jettons_data:
                    duplicate_count += 1
                
                jettons_data[symbol] = item
            continue
        
        # Handle single jetton (dict)
        if not isinstance(data, dict):
            print(f"Warning: Invalid format in {relative_path}, skipping")
            skipped_count += 1
            continue
        
        # Use symbol as the key
        symbol = data.get('symbol')
        if not symbol:
            print(f"Warning: No symbol found in {relative_path}, skipping")
            skipped_count += 1
            continue
        
        # Handle duplicate symbols
        if symbol in jettons_data:
            print(f"Warning: Duplicate symbol '{symbol}' found in {relative_path}, overwriting previous entry")
            duplicate_count += 1
        
        jettons_data[symbol] = data
        print(f"Processed: {relative_path} -> {symbol}")
    
    if skipped_count > 0:
        print(f"\nSkipped {skipped_count} files without symbols")
    if duplicate_count > 0:
        print(f"Found {duplicate_count} duplicate symbols (last occurrence kept)")
    
    return jettons_data


def save_to_json(data: Dict[str, Any], output_file: str):
    """Save the data to a JSON file."""
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"Successfully saved {len(data)} jettons to {output_file}")


def main():
    """Main function to orchestrate the conversion process."""
    output_file = "jettons.json"
    
    # Create a temporary directory for cloning
    with tempfile.TemporaryDirectory() as temp_dir:
        try:
            # Clone the repository and get jettons path
            jettons_path = clone_ton_assets(temp_dir)
            
            # Process all YAML files
            jettons_data = process_jettons_directory(jettons_path)
            
            # Save to JSON
            save_to_json(jettons_data, output_file)
            
            print("\nConversion completed successfully!")
            print(f"Total jettons processed: {len(jettons_data)}")
            
        except Exception as e:
            print(f"Error during conversion: {e}")
            raise


if __name__ == "__main__":
    main()

