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

pydeps_command = "pydeps %s --no-output --only %s --show-deps > %s"

def get_graph(commit):
    # unless a folder with the module name exists, descend into "src" directory if that exists
    if not os.path.isdir(args.module_name):
        if os.path.isdir("src"):
            os.chdir("src")
        # if a folder with the module name still doesn't exist, log and skip
        if not os.path.isdir(args.module_name):
            print("No module directory found for commit %s" % commit)
            return
    output_filename = os.path.join(args.output_path, commit + ".pydeps.json")
    os.system(pydeps_command % (args.module_name, args.module_name, output_filename))

git_revision_filter.for_each_month(args.repo_path, get_graph)
