import csv
import glob
import subprocess

# Output git log (0x09 is TAB)
# git --no-pager log --reverse --pretty=format:"%H%x09%ad%x09%s" > ../commits.log

def checkout_commit(commit_hash, path):
    p = subprocess.Popen('git add --all', cwd=path, shell=True)
    p.wait()

    p = subprocess.Popen('git reset', cwd=path, shell=True)
    p.wait()

    p = subprocess.Popen('git clean -dfX', cwd=path, shell=True)
    p.wait()

    p = subprocess.Popen('git reset --hard', cwd=path, shell=True)
    p.wait()

    p = subprocess.Popen('git checkout %s' % commit_hash, cwd=path, shell=True)
    p.wait()

input("Make sure to close vs-code first (so rust-analyzer doesn't keep regenerating './target')... Then press enter...")

commit_count = 0
with open('commits.log', mode='r') as file:
  csvFile = csv.reader(file, delimiter='\t')
  for lines in csvFile:
    commit_hash = lines[0]
    commit_date = lines[1]
    commit_message = lines[2]

    print(f"Hash: {commit_hash}; Date: {commit_date}; Message: {commit_message}", flush=True)

    checkout_commit(commit_hash, "catgirl-engine")

    for file in glob.iglob('catgirl-engine/**/*', recursive=True, include_hidden=True):
      if file.startswith("catgirl-engine/.gitmodules"):
        commit_count += 1
        break
    print("-"*40)

    print("Check count %s..." % (commit_count))
