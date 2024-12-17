* Look for files of all media types and add to git lfs
* Look for largest files ever committed to repo and either .gitignore or add to lfs
* Loop through each commit and remove files listed in .gitignore files in this directory and subdirectories
* Search for files with non-ASCII bytes and remove (except gradle-wrapper.jar)
* Review .gitignore files list
* Skips copying over empty commits
