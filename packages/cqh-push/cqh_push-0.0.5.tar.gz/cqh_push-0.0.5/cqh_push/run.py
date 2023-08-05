import subprocess
import logging

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)
import os
import git

def main():
    pwd = os.getcwd()
    logger.info("pwd:{}".format(pwd))
    repo = git.Repo(pwd)
    branch_name = repo.active_branch.name
    logger.info("branch_name:{}".format(branch_name))
    subprocess.check_call("git push origin {}".format(branch_name), shell=True)
    
    

if __name__ == "__main__":
    main()