from employee import Employee
from organization import Organization, OrganizationError

class OrganizationFile:
    """Reads and validates an initial organization from a text file."""
    @staticmethod
    def load(filename):
        try:
            with open(filename, encoding="utf-8") as file:
                rows = [(n, [x.strip() for x in line.strip().split("|")])
                        for n, line in enumerate(file, 1)
                        if line.strip() and not line.strip().startswith("#")]
        except OSError as exc:
            raise OrganizationError(f"Could not read file: {exc}") from exc
        presidents = [(n, p) for n, p in rows if p and p[0].casefold() == "president"]
        if len(presidents) != 1 or len(presidents[0][1]) != 2:
            raise OrganizationError("File must contain exactly one President|name entry.")
        org = Organization()
        org.root.employee = Employee(presidents[0][1][1])
        pending = []
        for line_no, parts in rows:
            if parts and parts[0].casefold() == "president":
                continue
            if len(parts) != 3:
                raise OrganizationError(f"Line {line_no}: use Level|EmployeeName|ManagerName.")
            level = {"vp": "VP", "supervisor": "Supervisor", "worker": "Worker"}.get(parts[0].casefold())
            if not level or not parts[1] or not parts[2]:
                raise OrganizationError(f"Invalid entry on line {line_no}.")
            pending.append((line_no, level, parts[1], parts[2]))
        while pending:
            remaining, progressed = [], False
            for line_no, level, name, manager_name in pending:
                manager = org.find(manager_name)
                if manager is None:
                    remaining.append((line_no, level, name, manager_name))
                    continue
                try:
                    org.hire(manager.employee.name, level, name)
                except OrganizationError as exc:
                    raise OrganizationError(f"Line {line_no}: {exc}") from exc
                progressed = True
            if not progressed:
                line_no, _, _, manager_name = remaining[0]
                raise OrganizationError(f"Line {line_no}: manager '{manager_name}' was not found or hierarchy is invalid.")
            pending = remaining
        return org
