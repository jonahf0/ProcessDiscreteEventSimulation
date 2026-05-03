ProcessDiscreteEventSimulation
------------------------------

This program and tool set will be used for creating proof-of-concept discrete-event simulations of singular computer processes (and potentially sub-processes).
The current goal is to:
- Use auditd, strace, and similar data sources to collect granual process events
- Use clustering algorithms to breakdown events into actions (for example, all syscalls that occur when a file is opened could be called "file open")
- These clustered events, and the individual events themselves, will be parsed into a discrete-event model for simulation

Another goal of the project is to "metricize" the clustered events so they can be compared. Similar processes will hopefully have similar clustered events.
However, another key goal is to compare clustered events of normal processes to processes that are victims of memory injection or shared object hijacking.
