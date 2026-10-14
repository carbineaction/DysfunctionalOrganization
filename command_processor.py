import shlex
from organization import Organization, OrganizationError
from organization_file import OrganizationFile

class CommandProcessor:
    """Parses user commands and calls the appropriate organization method."""
    HELP = '''Commands (quote names with spaces):
  load FILE
  display
  hire MANAGER VP|Supervisor|Worker EMPLOYEE_NAME
  fire MANAGER EMPLOYEE_NAME
  quit EMPLOYEE_NAME
  layoff MANAGER EMPLOYEE_NAME
  transfer PRESIDENT_OR_VP EMPLOYEE_NAME DESTINATION_MANAGER
  promote RECEIVING_MANAGER EMPLOYEE_NAME
  help
  exit'''

    def __init__(self, organization=None):
        self.organization = organization or Organization()

    def execute(self, command):
        try:
            parts = shlex.split(command)
        except ValueError as exc:
            raise OrganizationError(f"Invalid quotation marks: {exc}") from exc
        if not parts:
            return ""
        cmd, org = parts[0].casefold(), self.organization
        if cmd in ("help", "?"):
            return self.HELP
        if cmd in ("display", "show") and len(parts) == 1:
            return org.display()
        if cmd == "load" and len(parts) >= 2:
            loaded = OrganizationFile.load(" ".join(parts[1:]))
            org.root = loaded.root
            return f"Loaded organization from {' '.join(parts[1:])}."
        if cmd == "hire" and len(parts) >= 4:
            level = {"vp": "VP", "supervisor": "Supervisor", "worker": "Worker"}.get(parts[2].casefold())
            if not level:
                raise OrganizationError("Level must be VP, Supervisor, or Worker.")
            return org.hire(parts[1], level, " ".join(parts[3:]))
        if cmd == "fire" and len(parts) >= 3:
            return org.fire(parts[1], " ".join(parts[2:]))
        if cmd == "quit" and len(parts) >= 2:
            return org.quit(" ".join(parts[1:]))
        if cmd == "layoff" and len(parts) >= 3:
            return org.layoff(parts[1], " ".join(parts[2:]))
        if cmd == "transfer" and len(parts) >= 4:
            return org.transfer(parts[1], parts[2], " ".join(parts[3:]))
        if cmd == "promote" and len(parts) >= 3:
            return org.promote(parts[1], " ".join(parts[2:]))
        if cmd in ("exit", "quitprogram"):
            return "__EXIT__"
        raise OrganizationError("Invalid command. Type 'help' for commands.")
