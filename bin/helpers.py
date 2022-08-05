def buildMessasge(branchName: str, emoji: str, isSlack: bool):
    if(isSlack):
        return branchName + ' ' + emoji + '\n'
    else:
        return '| {0} | {1} |\n'.format(branchName, emoji)


def buildMessasgeFromList(results: list, projectName: str, isSlack: bool):
    if(isSlack):
        message = '@here Rebase results - {0}\n'.format(projectName)
        for result in results:
            branchName = result['branchName']
            emoji = result['emoji']
            message = message + buildMessasge(branchName, emoji, isSlack)

        return message
    else:
        message = '---\n#### @here Rebase results - {0}\n| Branch | Status |\n|:----:|:----:|\n'.format(
            projectName)
        for result in results:
            branchName = result['branchName']
            emoji = result['emoji']
            message = message + buildMessasge(branchName, emoji)

        return message
