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

def get_diffs():
  ce_files = []
  for file in glob.iglob('catgirl-engine/**/*', recursive=True, include_hidden=True):
    if not file.startswith("catgirl-engine/.git/"):
      ce_files.append(file.removeprefix("catgirl-engine/"))

  re_files = []
  for file in glob.iglob('ce-rewrite/**/*', recursive=True, include_hidden=True):
    if not file.startswith("ce-rewrite/.git/"):
      re_files.append(file.removeprefix("ce-rewrite/"))

  removed_files = []
  for file in ce_files:
    if file not in re_files:
      removed_files.append(file)

  found_files_to_check = False
  for file in removed_files:
    if not file.startswith("android/app/src/main/assets") and not file.startswith("examples/osx/disk_image/.DS_Store"):
      found_files_to_check = True

    print(file)

  return found_files_to_check

input("Make sure to close vs-code first (so rust-analyzer doesn't keep regenerating './target')... Then press enter...")

new_file = open('new_commits.log', mode='r')
new_csvFile = csv.reader(new_file, delimiter='\t')
counter = open('commits.log', mode='r')

commit_count = len(counter.readlines())
commit_no = 0
with open('commits.log', mode='r') as file:
  csvFile = csv.reader(file, delimiter='\t')
  for lines in csvFile:
        new_lines = next(new_csvFile)

        commit_hash = lines[0]
        commit_date = lines[1]
        commit_message = lines[2]

        new_commit_hash = new_lines[0]
        new_commit_date = new_lines[1]
        new_commit_message = new_lines[2]

        print(f"Hash: {commit_hash}; Date: {commit_date}; Message: {commit_message}", flush=True)
        print(f"Hash: {new_commit_hash}; Date: {new_commit_date}; Message: {new_commit_message}", flush=True)

        checkout_commit(commit_hash, "catgirl-engine")
        checkout_commit(new_commit_hash, "ce-rewrite")
        
        print("-"*40)
        found_files_to_check = get_diffs()
        print("-"*40)

        commit_no += 1
        if found_files_to_check:
          input("Check paths %s/%s..." % (commit_no, commit_count))
        else:
          print("Check paths %s/%s..." % (commit_no, commit_count))
