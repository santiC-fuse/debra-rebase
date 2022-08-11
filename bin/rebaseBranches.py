import asyncio
from concurrent.futures import ThreadPoolExecutor
from github import Github
from git import Repo
import tempfile
import shutil
from helpers import buildMessasgeFromList

def get_or_create_eventloop():
    try:
        return asyncio.get_event_loop()
    except RuntimeError as ex:
        if "There is no current event loop in thread" in str(ex):
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            return asyncio.get_event_loop()

def create_directory():
    try: 
        tempDir = tempfile.TemporaryDirectory()
        return tempDir
    except OSError as error: 
        print(error)

def delete_directory(dirPath: str):
    try: 
        shutil.rmtree(dirPath)
    except OSError as error: 
        print(error)

def process_result(branchName: str, result: bool):
    result = {
        "branchName": branchName, 
        "result": result,
        "emoji": ':white_check_mark:' if result else ':red_circle:'
    }
    return result

def branch_rebase(projectName: str, branchName: str):
    newDirectory = create_directory()
    try: 
        GITHUB_TOKEN = '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'
        
        pyGitHub = Github(GITHUB_TOKEN)
        originRepo = pyGitHub.get_repo("saveupfront/" + projectName)
        
        mainBranch = originRepo.default_branch
        
        repo = Repo.clone_from(originRepo.clone_url, newDirectory.name)
        
        remote = repo.remote("origin")
        
        remote.fetch(branchName)
        
        repo.git.checkout(branchName)
        
        repo.git.rebase(mainBranch)
        
        remote.push(force=True)
        
        return process_result(branchName, True)
    except Exception as error:
        print(error)
        return process_result(branchName, False)
    finally:
        delete_directory(newDirectory.name)

async def asynchronous_rebase(projectName: str, branches: list):
    with ThreadPoolExecutor(max_workers=10) as executor:
        loop = get_or_create_eventloop()
        try:
            tasks = [
                loop.run_in_executor(
                    executor,
                    branch_rebase,
                    *(projectName, branch)
                )
                for branch in branches
            ]
            return await asyncio.gather(*tasks)
        finally:
            loop.close

def parallel_async_rebases(projectName: str, branches: list):
    loop = get_or_create_eventloop()
    try:
        future = asyncio.ensure_future(asynchronous_rebase(projectName, branches))
        result = loop.run_until_complete(future)
        return result
    finally:
        loop.close

def rebase_branches(projectName: str, branches: list, isSlack: bool):
    if (len(branches) != 1):
        result = parallel_async_rebases(projectName, branches)
        textResponse = buildMessasgeFromList(result, projectName, isSlack)
        print(textResponse)
    else:
        result = branch_rebase(projectName, branches[0])
        textResponse = buildMessasgeFromList([result], projectName, isSlack)
        print(textResponse)
