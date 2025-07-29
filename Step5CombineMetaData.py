import os
import json
import re
from typing import Dict, Any

# --- Simple Configuration ---
script_dir = os.path.dirname(os.path.abspath(__file__))
MARKDOWN_DIR = os.path.join(script_dir, 'psx_markdown_clean')
METADATA_DIR = os.path.join(script_dir, 'output_metadata')
OUTPUT_DIR = os.path.join(script_dir, 'psx_bank_metadata')

def combine_files_simple():
    """
    Simple file combination: Find matching JSON + MD files with identical names and combine them.
    """
    # Create output directory
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Check directories exist
    if not os.path.isdir(MARKDOWN_DIR):
        print(f"❌ ERROR: Markdown directory not found: {MARKDOWN_DIR}")
        return
    if not os.path.isdir(METADATA_DIR):
        print(f"❌ ERROR: Metadata directory not found: {METADATA_DIR}")
        return
    
    print("🚀 Simple File Combination Tool")
    print("=" * 40)
    print(f"📁 Metadata source: {METADATA_DIR}")
    print(f"📁 Markdown source: {MARKDOWN_DIR}")
    print(f"📁 Output destination: {OUTPUT_DIR}")
    print("=" * 40)
    
    processed = 0
    skipped = 0
    
    # Get all JSON files from metadata directory
    for filename in os.listdir(METADATA_DIR):
        if not filename.endswith('_chunks.json'):
            continue
            
        json_path = os.path.join(METADATA_DIR, filename)
        if not os.path.isfile(json_path):
            continue
        
        # Look for corresponding markdown file with same base name
        md_filename = filename.replace('_chunks.json', '_chunks.md')
        md_path = os.path.join(MARKDOWN_DIR, md_filename)
        
        if not os.path.isfile(md_path):
            print(f"⏭️  Skipping {filename} - no matching markdown file")
            skipped += 1
            continue
            
        print(f"🔄 Processing: {filename} + {md_filename}")
        
        try:
            # Load metadata
            with open(json_path, 'r', encoding='utf-8') as f:
                metadata_list = json.load(f)
            
            # Create metadata lookup by chunk number
            metadata_dict = {}
            for item in metadata_list:
                if isinstance(item, dict) and 'chunk_number' in item:
                    metadata_dict[item['chunk_number']] = item
            
            # Read markdown content
            with open(md_path, 'r', encoding='utf-8') as f:
                markdown_content = f.read()
            
            # Find chunk headers and insert metadata
            chunk_pattern = re.compile(r'^(##\s+Chunk\s+(\d+))', re.MULTILINE)
            output_parts = []
            last_end = 0
            metadata_added = 0
            
            for match in chunk_pattern.finditer(markdown_content):
                chunk_num = int(match.group(2))
                
                # Add content before this chunk
                output_parts.append(markdown_content[last_end:match.start()])
                
                # Add metadata JSON line if available
                if chunk_num in metadata_dict:
                    metadata_json = json.dumps(metadata_dict[chunk_num], ensure_ascii=False)
                    output_parts.append(f"{metadata_json}\n")
                    metadata_added += 1
                
                # Add the chunk header
                output_parts.append(match.group(1) + "\n")
                last_end = match.end()
            
            # Add remaining content
            output_parts.append(markdown_content[last_end:])
            
            # Write combined output
            output_path = os.path.join(OUTPUT_DIR, md_filename)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(''.join(output_parts))
            
            print(f"✅ SUCCESS: Combined {filename} + {md_filename} → {md_filename}")
            print(f"   Added {metadata_added} metadata entries")
            processed += 1
            
        except Exception as e:
            print(f"❌ ERROR processing {filename}: {e}")
            skipped += 1
    
    print("\n" + "=" * 40)
    print(f"📊 SUMMARY:")
    print(f"   ✅ Files processed: {processed}")
    print(f"   ⏭️  Files skipped: {skipped}")
    print(f"   📁 Output directory: {OUTPUT_DIR}")
    print("=" * 40)

if __name__ == '__main__':
    combine_files_simple()