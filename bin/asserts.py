from constants import VALID_PROJECT_NAMES

def assert_argument_ammount(arguments: list):
    result = False
    if(len(arguments) == 0):
        raise Exception("No arguments received")
    if(len(arguments) > 1 and len(arguments) < 4):
        result = True
        
    if(result == False):
        raise Exception("Invalid arguments amount")

def assert_projectName(projectName: str):
    result = False
    for name in VALID_PROJECT_NAMES:
        if name == projectName:
            result = True

    if(result == False):
        raise Exception("Invalid projectName param")