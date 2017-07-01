# Manger ProCess

Process Manager is an API to high Performance.
Where the user can add the amount of process by choosing 
the  core quantity of the core machine ou adding manually.

```
Usage:

from manager_process import ManagerProcesses

def teste():
    while True:
        print 'laerte'
 
process = ManagerProcesses(p_daemonize=True)
process.create_process(p_create_cpu=False, p_amount_process=3,
                  p_function=teste, p_args=(), p_configure_stdout=False)
```
