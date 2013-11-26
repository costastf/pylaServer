pylaServer
==========

python based virtual printer used with pyla.py for submiting jobs to a hylafax server by printing to a printer directly

(Based on a perl solution from http://archives.seul.org/pyla/list/Nov-2003/msg00008.html)

When run it creates a virtual printer (name can be changed in the main of the script and so can the port ) that receives raw print jobs and invokes pyla.py script to submit the job. Pyla.py should be configured to connect to the Hylafax server. It should be run in the user session startup jobs.
