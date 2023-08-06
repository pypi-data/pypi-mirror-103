import IPython
from IPython.core import magic_arguments
from IPython.core.magic import (
    line_magic,
    Magics,
    magics_class,
)
from .helper import execute_on_all_nodes, execute_shell
import sys


@magics_class
class PlatformMagicsBase(Magics):
    """
    Base class with some utility functions, etc.
    """

    def __display_usage_error__(self, err_msg):
        """
        Display a usage error message
        """
        self.shell.show_usage_error(err_msg)

    def __display_error_message__(self, err_msg):
        """
        Display an error message
        """
        print("Error: %s" % err_msg, file=sys.stderr)


@magics_class
class PackageInstallationMagics(PlatformMagicsBase):
    """
    Magics to enable installing conda and pip packages
    on all nodes in a cluster.
    """

    @line_magic
    @magic_arguments.magic_arguments()
    @magic_arguments.argument(
        "pkg_names",
        nargs="+",
        type=str,
        default=[],
        help="name of the packages to install",
    )
    @magic_arguments.argument(
        "-c",
        "--channel",
        nargs="+",
        type=str,
        default=[],
        help="channels to use (same semantics as conda install -c)",
    )
    @magic_arguments.argument(
        "--timeout",
        type=int,
        default=None,
        help="number of seconds to timeout after",
    )
    @magic_arguments.argument(
        "--verbose",
        dest="verbose",
        action="store_true",
        default=False,
        help="Print information such as the mpiexec commands being run.",
    )
    def conda_install(self, line="", local_ns=None):
        """
        Bodo IPython Magic to install a conda package on all the cluster nodes.
        """
        # Parse the arguments
        args = magic_arguments.parse_argstring(self.conda_install, line)
        # Error out if no packages are listed
        if not args.pkg_names:
            self.__display_usage_error__("No packages provided")
            return
        # Channel substring based on if args.channel is provided
        channels = f"-c {' '.join(args.channel)}" if args.channel else ""
        # TODO Find a way to abstract /opt/conda/bin/conda away
        command = f"sudo /opt/conda/bin/conda install -y {' '.join(args.pkg_names)} {channels}"
        command = command.strip()
        # Execute on all nodes
        stdout_, stderr_, returncode, timed_out = execute_on_all_nodes(
            command,
            args.timeout,
            args.verbose,
        )
        # Handle output
        if timed_out:
            self.__display_error_message__("Timed out!")
        print("Output:\n", stdout_)
        if stderr_:
            self.__display_error_message__(stderr_)
        if args.verbose:
            print("returncode: ", returncode)

    @line_magic
    @magic_arguments.magic_arguments()
    @magic_arguments.argument(
        "pkg_names",
        nargs="+",
        type=str,
        default=[],
        help="name of the packages to install",
    )
    @magic_arguments.argument(
        "--timeout", type=int, default=None, help="number of seconds to timeout after."
    )
    @magic_arguments.argument(
        "--verbose",
        dest="verbose",
        action="store_true",
        default=False,
        help="Print information such as the mpiexec commands being run.",
    )
    def pip_install(self, line="", local_ns=None):
        """
        Bodo IPython Magic to install a pip package on all the cluster nodes.
        """
        # Parse the arguments
        args = magic_arguments.parse_argstring(self.pip_install, line)
        # Error out if no packages are listed
        if not args.pkg_names:
            self.__display_usage_error__("No packages provided")
            return
        # TODO Find a way to abstract /opt/conda/bin/pip away
        command = f"/opt/conda/bin/pip install {' '.join(args.pkg_names)}"
        # Execute on all nodes
        stdout_, stderr_, returncode, timed_out = execute_on_all_nodes(
            command,
            args.timeout,
            args.verbose,
        )
        # Handle output
        if timed_out:
            self.__display_error_message__("Timed out!")
        print("Output:\n", stdout_)
        if stderr_:
            self.__display_error_message__(stderr_)
        if args.verbose:
            print("returncode: ", returncode)


@magics_class
class BodoIPyParallelMagics(PlatformMagicsBase):
    """
    Magics to enable installing conda and pip packages
    on all nodes in a cluster.
    """

    @line_magic
    @magic_arguments.magic_arguments()
    @magic_arguments.argument(
        "--timeout", type=int, default=None, help="number of seconds to timeout after."
    )
    @magic_arguments.argument(
        "--verbose",
        dest="verbose",
        action="store_true",
        default=False,
        help="Print information such as the shell commands being run and its output.",
    )
    def restart_ipy(self, line="", local_ns=None):
        """
        Bodo IPython Magic to restart the IPyParallel setup on this cluster.
        """

        args = magic_arguments.parse_argstring(self.restart_ipy, line)

        cmd = f"sudo /bin/sh /tmp/restart_ipy.sh"

        stdout_, stderr_, returncode, timed_out = execute_shell(
            cmd, args.timeout, args.verbose
        )
        if timed_out:
            self.__display_error_message__("Timed out!")
        if args.verbose:
            print("Output:\n", stdout_)
        if stderr_:
            self.__display_error_message__(stderr_)
        if args.verbose:
            print("returncode: ", returncode)

        # If successful
        if not timed_out and not stderr_:
            print(
                "Successfully restarted IPyParallel cluster. Please restart the kernels on your notebooks before using IPyParallel again."
            )


def load_ipython_extension(ipython):
    """
    Register the magics with IPython
    """
    ipython.register_magics(PackageInstallationMagics)
    ipython.register_magics(BodoIPyParallelMagics)


from ._version import get_versions

__version__ = get_versions()["version"]
del get_versions
