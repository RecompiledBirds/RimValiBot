import git
import shutil
import os
import data
import glob
import stat
from dotenv import load_dotenv
load_dotenv()
path=f"{data.directory}\downloaded"


def selfupdate():
    if(os.path.exists(path)):
        pardir = os.path.abspath(os.path.join(path, os.path.pardir))
        os.chmod(pardir, stat.S_IWRITE )
        os.chmod(path, stat.S_IWRITE )
        os.unlink(path)
        for file in files:
            print(file)
      
        shutil.rmtree(path)

    git.Repo.clone_from(os.getenv("REPO"),path)
    shutil.rmtree(f"{path}/.git")
    shutil.copy(path,data.directory)



