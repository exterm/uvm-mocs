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
        if os.system("git checkout main") != 0:
            raise Exception("Could not checkout main branch")

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

