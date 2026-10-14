THE DYSFUNCTIONAL ORGANIZATION SYSTEM

Files:
  main.py               Starts the command-line program
  employee.py           Employee class
  position.py           Position class and capacity definitions
  organization.py       Organization hierarchy and business rules
  organization_file.py Reads and validates organization files
  command_processor.py Parses commands and calls organization operations
  sample_org.txt        Example organization data

Run with Python 3:
  python main.py

Then enter:
  load sample_org.txt
  display
  help
  exit

File format:
  President|Bob
  VP|Carol|Bob
  Supervisor|Ted|Carol
  Worker|Alice|Ted

Each non-president line is Level|EmployeeName|ManagerName. Blank lines and
lines beginning with # are ignored. Quote multiword names in commands.
