# Extract a dependency graph for each month of a project's history.

import argparse
import os

from lib import git_revision_filter

args = argparse.ArgumentParser()
args.add_argument("repo_path", help="path to the repository")
args.add_argument("module_name", help="name of the module to analyze")
args.add_argument("output_path", help="path to the output directory")

args = args.parse_args()

# make output path absolute
args.output_path = os.path.abspath(args.output_path)

pydeps_command = "pydeps --no-output --show-deps --nodot %s > %s"

def get_graph(commit):
    output_filename = os.path.join(args.output_path, commit + ".json")
    os.system(pydeps_command % (args.module_name, output_filename))

git_revision_filter.for_each_month(args.repo_path, get_graph)
