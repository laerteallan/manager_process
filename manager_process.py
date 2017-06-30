"""Class responsable by multi-processing."""

from multiprocessing import Process, cpu_count
import signal
import os
import sys
from time import sleep
ERROR_AMOUNT_PROCESS = """Higher than the existing process count.
                          Msg org: Amount Process Exists: %s
                                     Amount Process Terminate: %s
                        """
ERROR_PROCESS_NOT_FOUND = "Process not found"
ERROR_PID_MUST_INTEGER = "The pid of the process must be an integer."
PATH_SAVE_PID = "/var/run/"
PATH_PROCESS_ACTIVE = "/proc/"
PROCESS_PARENT = 'process.pid'
CMD_PROC_CHILD = 'pgrep -P %s'
TIMEOUT_DETROY_PROCESS = 0.1
STDOUT = '/tmp/stdout'
STDERR = '/tmp/stderr'


class ManagerProcesses(object):
    """Class Administration multi-processing."""

    def __init__(self, p_daemonize=False, p_configure_stdout=False):
        """Class contructor."""
        if p_configure_stdout:
            self.__configure_stdout_stderr()
        if p_daemonize:
            self.__daemonize()
        self.__list_process = []

    def __configure_stdout_stderr(self):
        """Set the out Error and the Normal."""
        sys.stdout.flush()
        sys.stderr.flush()
        stdout = file(STDOUT, 'a+')
        stderr = file(STDERR, 'a+', 0)
        os.dup2(stdout.fileno(), sys.stdout.fileno())
        os.dup2(stderr.fileno(), sys.stderr.fileno())

    def __daemonize(self):
        """Set Daemon Process."""
        try:
            pid = os.fork()
            if pid > 0:
                sys.exit(0)

        except OSError, error:
            print error
            sys.exit(1)
        os.chdir('/')
        os.setsid()
        os.umask(0)

    def __create_process(self, p_amount_process=0, p_function=None,
                         p_args=None):
        """Method create process.

        p_amount_process -> Amount create process
        p_function -> Function to perform
        p_args -> Tuple the Args to function
        """
        self.__save_pid_process(os.getpid(), PROCESS_PARENT)

        for i in range(p_amount_process):
            name_p = "process" + str(i) + '.pid'
            process = Process(name=name_p, target=p_function,
                              args=p_args)
            self.__list_process.append(process)
            process.start()
            self.__save_pid_process(process.pid, name_p)

    def __save_pid_process(self, p_pid, p_name_process):
        """Method to save pid the process."""
        file = open(PATH_SAVE_PID + p_name_process, "w")
        file.write(str(p_pid))
        file.close()

    def __return_process_child(self, p_pid_process_parent):
        """Method return process child."""
        lst_proc_child = os.popen(CMD_PROC_CHILD % (p_pid_process_parent))
        lst_proc_child = [pid_proc.strip('\n') for pid_proc in lst_proc_child]
        return lst_proc_child

    def create_process(self, p_create_cpu=False, p_amount_process=0,
                       p_function=None, p_args=()):
        """Method create most process."""
        amount_process = p_amount_process
        if p_create_cpu:
            amount_process = cpu_count()
        self.__create_process(amount_process, p_function, p_args)

    def check_process_exist(self, p_pid):
        """Method check process exist."""
        if os.path.exists(PATH_PROCESS_ACTIVE + str(p_pid)):
            return True

        return False

    def kill_all_process_parent_child(self):
        """Method to destroy all the parent and child processes."""
        pid_parent = open(PATH_SAVE_PID + PROCESS_PARENT).read()
        list_process_child = self.__return_process_child(pid_parent)

        for pid_process_child in list_process_child:
            if self.check_process_exist(pid_process_child):
                self.kill_process_pid(int(pid_process_child))

    def kill_process_pid(self, p_pid):
        """Method kill process by PID."""
        if not isinstance(p_pid, int):
            raise Exception(ERROR_PID_MUST_INTEGER)

        if self.check_process_exist(p_pid):
            os.kill(p_pid, signal.SIGKILL)
            return True
        raise Exception(ERROR_PROCESS_NOT_FOUND)

    def terminate_process(self, p_amount_process):
        """Method terminate process.

        p_amount_process - > Amount terminate Process created
        """
        amount_process = len(self.__list_process)
        if p_amount_process > amount_process:
            raise Exception(ERROR_AMOUNT_PROCESS % (str(amount_process),
                                                    str(p_amount_process)))

        for index_process in range(p_amount_process):
            process = self.__list_process[index_process]
            process.terminate()
            sleep(TIMEOUT_DETROY_PROCESS)
            process.exitcode == -signal.SIGTERM

    def get_amount_process_active(self):
        """Return amount processes active."""
        return len(self.__list_process)
