import subprocess
import os
from subprocess import Popen
from itertools import islice
import sys
sys.path.append(os.path.abspath(__file__))
import Utilities as utils
import Constants as c

projects = []
repos = c.ALL_PROJECTS
# repos = ["angular/linux"]

for repo in repos:
    projects.append("python ./scripts/CalculateMetrics_H1.py --p={repo}".format(repo=repo))

max_workers = 8
processes = (Popen(cmd, shell=True) for cmd in projects)
running_processes = list(islice(processes, max_workers))  # start new processes
while running_processes:
    for i, process in enumerate(running_processes):
        if process.poll() is not None:  # the process has finished
            running_processes[i] = next(processes, None)  # start new process
            if running_processes[i] is None: # no new processes
                del running_processes[i]
                break
