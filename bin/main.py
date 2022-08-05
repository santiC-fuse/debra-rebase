import optparse
from asserts import assert_argument_ammount, assert_projectName
from rebaseBranches import rebase_branches


def main():
    parser = optparse.OptionParser()
    parser.set_defaults(debug=False, xls=False)
    (options, args) = parser.parse_args()

    assert_argument_ammount(args)

    project_name = args[0]
    branches = args[1].split(',')

    assert_projectName(project_name)

    rebase_branches(project_name, branches, True)


main()
