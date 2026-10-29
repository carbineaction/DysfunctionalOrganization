# The Dysfunctional Organization System
CS-4230-601 | 2026 Fall - Full Term, UVU, Team 5

## Team Members
1. Keomony Mary
2. Ryan Carbine

## Project Description 
The Dysfunctional Organization System is a Python command-line application that manages a hierarchical company structure consisting of a President, Vice Presidents, Supervisors, and Workers. The program supports hiring, firing, layoffs, transfers, promotions, organization display, and file-based organization loading while enforcing organizational business rules.

## Project Structure
```
THE DYSFUNCTIONAL ORGANIZATION SYSTEM
├── docs/
│   ├── command_processor_flowgraph.pdf
│   ├── command_processor_flowgraph.PNG
│   └── Project Instructions.doc
│   └── Project_4.doc
├── command_processor.py
├── employee.py
├── main.py
├── organization_file.py
├── organization.py
├── position.py
├── README.md
├── sample_org.txt
├── sample_org2.txt
```

## Running the Program

Run the program from the command line using:

```
python main.py
```

or

```
python3 main.py
```

## Files

| File | Description  |
|---|---|
| docs/ | Contains project documentation, including the project_4 description, project instructions, flow graphs, and other documents. | 
|main.py| Starts the command-line program. |
|employee.py | Defines the Employee class. |
|position.py | Defines the Position class and the organization capacity structure. |
| organization.py |Implements the organization hierarchy and business rules. |
| organization_file.py Reads and validates organization data files. |
| command_processor.py |Parses user commands and invokes organization operations. |
| sample_org.txt | Sample organization data used for testing.|
| sample_org2.txt | Additional sample organization data used for testing. |
| README | Instructions on how to run the program and project overview. |


## Step-by-Step Guide

1. **Load a file:** Start by loading your text file into the application. Type `load FILE_NAME`.
2. **View personnel:** Type `display` or `show` to view the organization's current structure.
3. **Get help:** Type `help` to display command syntax and instructions.
4. **Exit:** Type `exit` or `quitprogram` to close the application.


## Example Command

Names containing spaces must be enclosed in quotation marks when entered in commands to ensure they are parsed correctly as a single employee name. 

**Examples:**
* `hire "Ted Smith" Worker "Alice Johnson"`
* `fire "Carol Jones" "Alice Johnson"`
* `transfer "Carol Jones" "Alice Johnson" "Mark Brown"`

| Command | Syntax | Description |
| :--- | :--- | :--- |
| **load** | `load FILE_NAME` | Load an organization file by entering `load FILE_NAME`. The file must follow the required organization file format. |
| **display / show** | `display` / `show` | View the current organization that has successfully been loaded. |
| **hire** | `hire NAME Worker NAME` <br> `MANAGER VP\|Supervisor\|Worker EMPLOYEE` | Hire a new employee into a vacant position of the specified level. |
| **fire** | `fire MANAGER_NAME EMPLOYEE_NAME` | Fire an employee who is within the manager's direct hierarchy. |
| **quit** | `quit EMPLOYEE_NAME` | Employee quits the organization. |
| **layoff** | `layoff MANAGER_NAME EMPLOYEE_NAME` | Lay off an employee who is within the manager's direct hierarchy. |
| **transfer** | `transfer PRESIDENT/VICE_PRESIDENT_NAME EMPLOYEE_NAME DESTINATION_MANAGER` | Transfer an employee to a different manager. |
| **promote** | `promote RECEIVING_MANAGER EMPLOYEE_NAME` | Promote an employee to a higher position. |
| **help** | `help` | Display this help message. |
| **exit / quitprogram** | `exit` / `quitprogram` | Exit the program. |


## Organization File Format

The plain text file is formatted as follows:

```
President|Bob
VP|Carol|Bob
Supervisor|Ted|Carol
Worker|Alice|Ted
```

* The president is specified as `President|EmployeeName`.
* Each non-president line is `Level|EmployeeName|ManagerName`.
* Blank lines and lines beginning with `#` are ignored. 
* Quote multiword names in commands.