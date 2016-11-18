import argparse
import subprocess
import sys
import pexpect

# --debug flag prints the stdout and stderr.
parser = argparse.ArgumentParser(description="Choose debug mode or not.")
parser.add_argument("--debug", help="Print stdout and stderr messages.",
                    action="store_true")
args = parser.parse_args()

def main():
    # child process can be anything interactive.
    # /bin/bash is an example of an interactive menu.
    child = pexpect.spawn("/bin/bash")
    # sendline runs commands.
    child.sendline("ls")
    child.sendline("echo EOF")
    # What do I expect after I use ls? Well, I expect to see a $.
    child.expect("echo EOF")
    # child.before represents everything before the expect, which means:
    # when we see the next $, child.before will contain the `ls` output.
    print(child.before)
    # child.after prints things after the expect. Which is the `echo EOF` output.
    print(child.after)

    # exit from /bin/bash.
    child.sendline("exit")
    """
    You can send multiple lines before expecting them.
    You can expect multiple things and print the child.before or child.after.
    """

def run_command(name, return_code, command):
    """Runs arbitrary command and exits with return_code if failure.

    Args:
        name: Name of the command for identification purposes.
        return_code: An integer to exit if command fails.
        command: An array with the components of the command.

    Raises:
        OSError or CalledProcessError: An error occurred running the
        command.
    """
    try:
        process = subprocess.Popen(command,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
    except (OSError, subprocess.CalledProcessError) as err:
        print(name + " runtime error: " + str(err))
        sys.exit(return_code)

    # Check standard output and error of the command and print in debug mode. 
    output, error = process.communicate()

    if (args.debug):
        print(output)
        print(error)

    if (error):
        print(" ".join(command))
        print(error)
        sys.exit(return_code)

    return output

def run_interactive_command(name, return_code, command, expectances, responses):
    """Runs arbitrary command and exits with return_code if failure.

    Args:
        name: Name of the command for identification purposes.
        return_code: An integer to exit if command fails.
        command: An array with the components of the command.

    Raises:
        OSError or CalledProcessError: An error occurred running the
        command.
    """
    for i, expectance in enumerate(expectances):
        print(expectance)
        print(responses[i])
        try:
            child = pexpect.spawn(command)
        except (OSError, subprocess.CalledProcessError) as err:
            print(name + " runtime error: " + str(err))
            sys.exit(return_code)

        child.sendline(responses[i])
        child.expect(expectance)
        print(child.before)
        child.interact()

if __name__ == "__main__":
    main()
