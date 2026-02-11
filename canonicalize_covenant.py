#!/usr/bin/env python3
"""
Deterministic YAML canonicalization script.
Constraints:
- Alphabetical key sorting at all nesting levels
- Whitespace normalization
- UTF-8 encoding
- Unix line endings
- Preserve string values exactly
- Preserve array order
"""

import yaml
import sys
from collections import OrderedDict


def sort_dict_recursive(obj):
    """Recursively sort dictionary keys alphabetically."""
    if isinstance(obj, dict):
        return OrderedDict(sorted((k, sort_dict_recursive(v)) for k, v in obj.items()))
    elif isinstance(obj, list):
        return [sort_dict_recursive(item) for item in obj]
    else:
        return obj


def canonicalize_yaml(input_path, output_path):
    """Read YAML, canonicalize, write output."""
    try:
        # Read input
        with open(input_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        
        # Sort keys recursively
        canonical_data = sort_dict_recursive(data)
        
        # Write output with canonical formatting
        with open(output_path, 'w', encoding='utf-8', newline='\n') as f:
            yaml.dump(
                canonical_data,
                f,
                default_flow_style=False,
                allow_unicode=True,
                sort_keys=False,  # Already sorted manually
                width=float('inf')  # No line wrapping
            )
        
        return 0
    
    except Exception as e:
        print(f"ERROR: {type(e).__name__}: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    input_file = "C:\\Users\\Aidor\\sigma-lora-covenant\\covenant.yaml"
    output_file = "C:\\Users\\Aidor\\sigma-lora-covenant\\canonicalized_covenant.yaml"
    
    exit_code = canonicalize_yaml(input_file, output_file)
    
    if exit_code == 0:
        print(f"SUCCESS: Canonicalized {input_file} -> {output_file}")
    
    sys.exit(exit_code)
