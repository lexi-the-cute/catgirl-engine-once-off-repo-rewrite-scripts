import os
import csv
import subprocess

import os.path

from time import sleep

# Output git log (0x09 is TAB)
# git --no-pager log --reverse --pretty=format:"%H%x09%ad%x09%s" > ../commits.log

# Go to first commit
# git reset --hard `git rev-list --all | tail -n 1`

# Display uncommitted files
# git add --all && git status -s

# Prune empty commits from commit history
# git filter-branch --prune-empty

# Delete all files except .git/*
# find . -not -wholename "./.git" -not -wholename "./.git/*" -delete

# List all files in commit history
# git log --pretty=format: --name-only | sort | uniq

# Find all files with non-ascii characters (will need further filtering cause of unicode)
# find . -not -wholename "./.git/*" -type f -exec sh -c 'file "$1" | grep -qv "ASCII text"' sh {} \; -exec echo {} \;

# Remove all non-ascii files with more filtering
# find . -not -wholename "./.git/*" -type f -exec sh -c 'file "$1" | grep -qv "ASCII text"' sh {} \; -exec sh -c 'echo "Binary File: $1" | grep -vE "\.md$|\.yml$|\.json$|\.disabled$|\.jar$|\.png$|\.sh$"' sh {} \; -exec sh -c 'rm -Rf --preserve-root=all "{}"' sh {} \;

# Clone Submodules
# cd .. && cd jni && git clone git@github.com:libsdl-org/SDL.git && cd SDL && git checkout ac13ca9ab691e13e8eebe9684740ddcb0d716203 && cd ..

globs_to_remove = [".apk", ".AppImage", ".bin", ".class", ".cxx", ".dex", ".DS_Store", ".exe", ".externalNativeBuild", ".gitignore.bak", ".hprof", ".idea", ".iml", ".jekyll-cache", ".jks", ".keystore", ".log", ".mm_profdata", ".o", ".profraw", ".pxd", ".ra-target", ".rlib", ".sass-cache", ".server-target", ".so", ".venv", ".zip", ".zsync"]

def reset_old_repo():
    p = subprocess.Popen('git checkout main', cwd='catgirl-engine', shell=True)
    p.wait()

    p = subprocess.Popen('git add --all', cwd='catgirl-engine', shell=True)
    p.wait()

    p = subprocess.Popen('git reset', cwd='catgirl-engine', shell=True)
    p.wait()

    p = subprocess.Popen('git clean -dfX', cwd='catgirl-engine', shell=True)
    p.wait()

    p = subprocess.Popen('git reset --hard', cwd='catgirl-engine', shell=True)
    p.wait()

def init_new_repo():
    os.makedirs("ce-rewrite", exist_ok=True)

    p = subprocess.Popen('find . -delete', cwd='ce-rewrite', shell=True)
    p.wait()

    p = subprocess.Popen('git init -b main .', cwd='ce-rewrite', shell=True)
    p.wait()

    p = subprocess.Popen('git config feature.manyFiles true', cwd='ce-rewrite', shell=True)
    p.wait()

    p = subprocess.Popen('git update-index --index-version 4', cwd='ce-rewrite', shell=True)
    p.wait()

    p = subprocess.Popen('git config core.fsmonitor true', cwd='ce-rewrite', shell=True)
    p.wait()

    p = subprocess.Popen('git config core.untrackedcache true', cwd='ce-rewrite', shell=True)
    p.wait()

    p = subprocess.Popen('git config core.commitgraph true', cwd='ce-rewrite', shell=True)
    p.wait()

    p = subprocess.Popen('git config fetch.writeCommitGraph true', cwd='ce-rewrite', shell=True)
    p.wait()

    p = subprocess.Popen('git lfs install', cwd='ce-rewrite', shell=True)
    p.wait()

    p = subprocess.Popen('git config lfs.https://codeberg.org/alexis/catgirl-engine.git/info/lfs.locksverify true', cwd='ce-rewrite', shell=True)
    p.wait()

    p = subprocess.Popen('git config lfs.https://github.com/foxgirl-labs/catgirl-engine.git/info/lfs.locksverify true', cwd='ce-rewrite', shell=True)
    p.wait()

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

def clean_files():
    p = subprocess.Popen('find . -not -wholename "./.git" -not -wholename "./.git/*" -delete', cwd='ce-rewrite', shell=True)
    p.wait()

def copy_files():
    p = subprocess.Popen('rsync -a . ../ce-rewrite/ --exclude .git', cwd='catgirl-engine', shell=True)
    p.wait()

def preempt_remove_glob():
    for glob in globs_to_remove:
        # print('Pre-emptively Removing Glob: `find . -type f -name "*\\%s" -delete`' % glob)
        p = subprocess.Popen('find . -type f -name "*\\%s" -delete' % glob, cwd='catgirl-engine', shell=True)
        p.wait()

def remove_glob():
    for glob in globs_to_remove:
        # print('Removing Glob: `find . -type f -name "*\\%s" -delete`' % glob)
        p = subprocess.Popen('find . -type f -name "*\\%s" -delete' % glob, cwd='ce-rewrite', shell=True)
        p.wait()

def skip_bad_files_worktree():
    with open('remove', mode='r') as file:
        for line in file:
            # print('Skipping Bad File(s) Worktree: `git update-index --ignore-missing --force-remove --skip-worktree "%s" 2> /dev/null`' % line.strip())
            p = subprocess.Popen('git update-index --ignore-missing --force-remove --skip-worktree "%s" 2> /dev/null' % line.strip(), cwd='ce-rewrite', shell=True)
            p.wait()

def unskip_bad_files_worktree():
    with open('remove', mode='r') as file:
        for line in file:
            # print('Unskipping Bad File(s) Worktree: `git update-index --ignore-missing --force-remove --no-skip-worktree "%s" 2> /dev/null`' % line.strip())
            p = subprocess.Popen('git update-index --ignore-missing --force-remove --no-skip-worktree "%s" 2> /dev/null' % line.strip(), cwd='ce-rewrite', shell=True)
            p.wait()

def preempt_remove_bad_files():
    with open('remove', mode='r') as file:
        files = ""
        for line in file:
            files = files + '"%s" ' % line.strip()

        print('Pre-emptively Removing Bad File(s): `rm -Rf --preserve-root=all %s`' % files)
        p = subprocess.Popen('rm -Rf --preserve-root=all %s' % files, cwd='catgirl-engine', shell=True)
        p.wait()

def remove_bad_files():
    with open('remove', mode='r') as file:
        files = ""
        for line in file:
            files = files + '"%s" ' % line.strip()

        print('Removing Bad File(s): `rm -Rf --preserve-root=all %s`' % files)
        p = subprocess.Popen('rm -Rf --preserve-root=all %s' % files, cwd='ce-rewrite', shell=True)
        p.wait()

def add_attributes_file():
    p = subprocess.Popen('cp -a ../.gitattributes .', cwd='ce-rewrite', shell=True)
    p.wait()

def remove_binary_files():
    p = subprocess.Popen('find . -not -wholename "./.git/*" -type f -exec sh -c \'file "$1" | grep -qv "ASCII text"\' sh \\{\\} \\; -exec sh -c \'echo "Found Binary File: $1" | grep -vE "\\.md$|\\.yml$|\\.json$|\\.disabled$|\\.jar$|\\.png$|\\.sh$|\\.webp$|gradlew$|\\.svg$|\\.DS_Store$|\\.icns$|\\.yml.d$|\\.gitignore$|\\.yaml$|\\.gradle$|\\.toml$"\' sh \\{\\} \\; -exec sh -c \'rm -Rf --preserve-root=all "\\{\\}"\' sh \\{\\} \\;', cwd='ce-rewrite', shell=True)
    p.wait()

def fix_submodules():
    p = subprocess.Popen('sed -i "s/alexisart/lexi-the-cute/" .gitmodules', cwd='ce-rewrite', shell=True)
    p.wait()

def init_submodules():
    if not os.path.exists("catgirl-engine/.gitmodules"):
        return

    p = subprocess.Popen('git submodule status', cwd='catgirl-engine', stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, text=True)

    submodules_stdout, submodules_stderr = p.communicate()
    p.wait()

    for line in submodules_stdout.split("\n"):
        line = line.lstrip("-").lstrip("+").lstrip("U")
        sub_status_split = line.split(" ")

        if len(sub_status_split) < 2:
            break

        print(sub_status_split)
        s_path = sub_status_split[1]
        s_commit = sub_status_split[0]

        print('Makedirs: `mkdir -p %s`' % (s_path))
        p = subprocess.Popen('mkdir -p %s' % (s_path), cwd='ce-rewrite', shell=True)
        p.wait()

        print('Copy submodule: `rsync -a submodules/%s ce-rewrite/%s`' % (s_path, s_path))
        p = subprocess.Popen('rsync -a submodules/%s ce-rewrite/%s/..' % (s_path, s_path), cwd='.', shell=True)
        p.wait()

        print('Checkout submodule: `cd %s && git checkout %s`' % (s_path, s_commit))
        p = subprocess.Popen('cd %s && git checkout %s' % (s_path, s_commit), cwd='ce-rewrite', shell=True)
        p.wait()

        # print('Adding submodule: `git submodule add %s %s`' % ("SET-ME", s_path))
        # p = subprocess.Popen('git submodule add %s %s' % ("SET-ME", s_path), cwd='ce-rewrite', shell=True)
        # p.wait()

    # input("Setup submodules manually...")

def create_new_commit(commit_date, commit_message):
    # Create New Commit
    environment_vars = dict(os.environ, GIT_AUTHOR_DATE=commit_date, GIT_COMMITTER_DATE=commit_date)
    escaped_commit_message = commit_message.replace("'", "\\'")

    p = subprocess.Popen('git add --all', cwd='ce-rewrite', shell=True)
    p.wait()

    print("Creating Git Commit: `git commit --allow-empty -m $'%s'`" % (escaped_commit_message))
    p = subprocess.Popen("git commit --allow-empty -m $'%s'" % escaped_commit_message, cwd='ce-rewrite', shell=True, env=environment_vars)
    p.wait()


input("Make sure to close vs-code first (so rust-analyzer doesn't keep regenerating './target')... Then press enter...")

reset_old_repo()
init_new_repo()

with open('commits.log', mode='r') as file:
  csvFile = csv.reader(file, delimiter='\t')
  for lines in csvFile:
        commit_hash = lines[0]
        commit_date = lines[1]
        commit_message = lines[2]

        print(f"Hash: {commit_hash}; Date: {commit_date}; Message: {commit_message}", flush=True)

        print("-"*40, flush=True)
        print("Checkout commit...", flush=True)
        checkout_commit(commit_hash, path='catgirl-engine')

        print("Clean files...", flush=True)
        clean_files()

        print("Pre-emptively Remove bad files...", flush=True)
        remove_bad_files()

        print("Pre-emptively Remove glob...", flush=True)
        remove_glob()

        print("Copy files...", flush=True)
        copy_files()

        print("Remove bad files from working tree...", flush=True)
        skip_bad_files_worktree()

        print("Remove bad files...", flush=True)
        remove_bad_files()

        print("Remove glob...", flush=True)
        remove_glob()

        print("Removing binary files...", flush=True)
        remove_binary_files()

        print("Add attributes file...", flush=True)
        add_attributes_file()

        print("Fix .gitmodules...", flush=True)
        fix_submodules()

        print("Check for submodules...", flush=True)
        init_submodules()

        print("Create new commit...", flush=True)
        create_new_commit(commit_date, commit_message)

        print("-"*40, flush=True)

# unskip_bad_files_worktree()
