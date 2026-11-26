#!/usr/bin/env python3
import os
import shutil
import sys

def main():
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        src = os.path.join(script_dir, "entry.png")
        if not os.path.exists(src):
            print(f"Error: Source image not found at {src}", file=sys.stderr)
            sys.exit(1)
            
        output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
        os.makedirs(output_dir, exist_ok=True)
        dst = os.path.join(output_dir, "entry.png")
        
        shutil.copyfile(src, dst)
        print(f"Successfully copied {src} to {dst}")
    except Exception as e:
        print(f"Error executing main.py: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
