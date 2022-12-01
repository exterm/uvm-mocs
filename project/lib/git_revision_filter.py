# for a given repository path, get the first revision of each month

import os

commit_list_cmd = '''
git log --first-parent --pretty=%H\\ %cd --date=short \
| awk '$2$3 != last { last=$2$3; print $1}' 'FS=[- ]' \
| git log --no-walk --stdin --pretty=format:"%as_%h"
'''

# execute given function for the last revision of each month
def for_each_month(repo_path, func):
    old_path = os.getcwd()
    os.chdir(repo_path)
    try:
        commit_list = os.popen(commit_list_cmd).read().split()

        print("Found %d commits" % len(commit_list))

        for commit in commit_list:
            sha = commit.split('_')[1]

            if os.system("git checkout -d %s" % sha) != 0:
                raise Exception("Could not checkout revision %s" % sha)

            os.system("git clean -fdx")

            func(commit)
    finally:
        os.chdir(old_path)

def for_each_revision_between(first, last, repo_path, func):
    old_path = os.getcwd()
    os.chdir(repo_path)

    try:
        output = os.popen("git rev-list --ancestry-path %s..%s" % (first, last)).read()
        revisions = output.split() + [first]

        revisions.reverse()

        # file name format: YYYY-MM-DD_Number_SHA
        for i, sha in enumerate(revisions):
            date = os.popen(f"git show -s --format=%as {sha}").read().strip()

            # abort if date empty
            if not date:
                print("Could not get date for revision %s" % sha)
                return

            if os.system("git checkout -d %s" % sha) != 0:
                raise Exception("Could not checkout revision %s" % sha)

            os.system("git clean -fdx")

            # number string from I that is at least 3 digits long
            number = str(i).zfill(3)

            func(f"{number}_{date}_{sha[:9]}")
    finally:
        os.chdir(old_path)
