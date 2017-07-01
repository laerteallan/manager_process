Process Manager is an API to high Performance.
Where the user can add the amount of process by choosing 
the  core quantity of the core machine ou adding manually.

Usage:

from manager_process import ManagerProcesses


def teste():
    while True:
        print 'laerte'


# Create Process
process = ManagerProcesses(p_daemonize=True)

#adding the function to execute in the process

# Option p_create_cpu=True -> Set amount core machine exist
# p_amount_process=10 -> Set amount the core exist of machine. OBs: if p_create_cpu=True is active these option not used
#p_function -> Function that need high perfomance
#p_args (tuple) -> Params of function
#p_configure_stdout -> Set configure of out Sdterr and Stdout Defautl (/tmp)
process.create_process(p_create_cpu=False, p_amount_process=3,
                  p_function=teste, p_args=(), p_configure_stdout=False)