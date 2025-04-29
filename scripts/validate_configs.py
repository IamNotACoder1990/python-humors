import difflib

def compare_configs(intended, actual):
    diff = difflib.unified_diff(
        intended.splitlines(), actual.splitlines(), lineterm=''
    )
    for line in diff:
        print(line)

# Example usage:
# compare_configs(open("intended.txt").read(), open("running.txt").read())
