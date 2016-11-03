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
    run_interactive_command("bash", 1, "/bin/bash", [".*"], ["ls"])
    print("Do computation here.")
    
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
