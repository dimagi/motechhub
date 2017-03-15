import subprocess


def javascript_is_valid(js_string):
    process = subprocess.Popen(
        ['node', '--check'],
        stdin=subprocess.PIPE, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    process.communicate(js_string)
    if process.returncode == 0:
        return True
    else:
        return False
