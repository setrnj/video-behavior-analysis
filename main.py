#!/usr/bin/env python3
"""
Simple launcher for this project.

Usage examples:
  python3 main.py --mode all
  python3 main.py --mode etl
  python3 main.py --mode visualize
"""

import argparse
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
PARENT = os.path.abspath(os.path.join(ROOT, ".."))

def run_cmd(cmd, cwd=PARENT):
    print(">>> Running:", cmd)
    try:
        subprocess.check_call(cmd, shell=True, cwd=cwd)
    except subprocess.CalledProcessError as e:
        print("Command failed with return code:", e.returncode)
        sys.exit(e.returncode)

def main():
    parser = argparse.ArgumentParser(description="Project launcher")
    parser.add_argument("--mode", choices=["all", "etl", "visualize", "stub"], default="stub",
                        help="What to run")
    args = parser.parse_args()

    if args.mode == "all":
        # ETL then visualizations (if scripts exist)
        etl_path = os.path.join(PARENT, "run_etl.sh")
        vis_path = os.path.join(PARENT, "run_visualizations.sh")

        if os.path.isfile(etl_path):
            run_cmd("bash run_etl.sh")
        else:
            print("ETL script not found at", etl_path)

        if os.path.isfile(vis_path):
            run_cmd("bash run_visualizations.sh")
        else:
            print("Visualizations script not found at", vis_path)

    elif args.mode == "etl":
        etl_path = os.path.join(PARENT, "run_etl.sh")
        if os.path.isfile(etl_path):
            run_cmd("bash run_etl.sh")
        else:
            print("ETL script not found at", etl_path)

    elif args.mode == "visualize":
        vis_path = os.path.join(PARENT, "run_visualizations.sh")
        if os.path.isfile(vis_path):
            run_cmd("bash run_visualizations.sh")
        else:
            print("Visualizations script not found at", vis_path)

    else:
        print("Stub mode: project root is", PARENT)
        print("Available files in project root:")
        for name in sorted(os.listdir(PARENT)):
            print("  ", name)

if __name__ == "__main__":
    main()
