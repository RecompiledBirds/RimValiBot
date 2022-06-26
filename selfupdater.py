import git
import shutil
import os
import data
import glob
from dotenv import load_dotenv
load_dotenv()
path=f"{data.directory}\downloaded"


def selfupdate():
  if(os.path.exists(path)):
    shutil.rmtree(path)

  git.Repo.clone_from(os.getenv("REPO"),path)
  shutil.rmtree(f"{path}/.git")
 
  files = glob.glob(f"{path}/*")
  for file in files:
    fileName=file.replace(path,"")
    fp=f"{data.directory}/{fileName}"
    if os.path.exists(fp):
      if os.path.isdir(fp):
        shutil.rmtree(fp)
      else:
        os.remove(fp)
    print(f"Updaing: {fileName}")
    shutil.move(file,data.directory)



