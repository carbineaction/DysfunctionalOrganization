from employee import Employee
from position import Position, CHILD_LEVEL

class OrganizationError(Exception):
    """An invalid organization operation or input file."""

class Organization:
    """Owns the company hierarchy and enforces business rules."""
    def __init__(self):
        self.root = Position("President")

    @staticmethod
    def normalize(name):
        return " ".join(name.strip().split())

    def positions(self):
        result = []
        def visit(pos):
            result.append(pos)
            for child in pos.children:
                visit(child)
        visit(self.root)
        return result

    def find(self, name):
        wanted = self.normalize(name).casefold()
        return next((p for p in self.positions() if p.employee and p.employee.name.casefold() == wanted), None)

    def require(self, name):
        found = self.find(name)
        if found is None:
            raise OrganizationError(f"Employee not found: {name}")
        return found

    def is_descendant(self, position, manager):
        current = position.parent
        while current:
            if current is manager:
                return True
            current = current.parent
        return False

    def ancestor(self, position, level):
        current = position
        while current:
            if current.level == level:
                return current
            current = current.parent
        return None

    def vacant_child(self, manager, level):
        return next((p for p in manager.children if p.level == level and p.is_vacant), None)

    def check_unique(self, name):
        employee = Employee(name)
        if self.find(employee.name):
            raise OrganizationError(f"That name is already used: {employee.name}")
        return employee

    def hire(self, manager_name, level, name):
        manager = self.require(manager_name)
        if manager.level not in CHILD_LEVEL or CHILD_LEVEL[manager.level] != level:
            raise OrganizationError(f"{manager.level} may hire only its direct subordinate level.")
        slot = self.vacant_child(manager, level)
        if slot is None:
            raise OrganizationError(f"No vacant {level} position under {manager_name}.")
        slot.employee = self.check_unique(name)
        return f"Hired {slot.employee.name} as {level} under {manager_name}."

    def fire(self, manager_name, employee_name):
        manager, target = self.require(manager_name), self.require(employee_name)
        if target is self.root:
            raise OrganizationError("The president cannot be fired.")
        if not self.is_descendant(target, manager):
            raise OrganizationError("You may only fire someone in your hierarchy.")
        target.employee = None
        return f"{employee_name} was fired; the position is now vacant."

    def quit(self, employee_name):
        target = self.require(employee_name)
        if target is self.root:
            raise OrganizationError("The president cannot quit.")
        target.employee = None
        return f"{employee_name} quit; the position is now vacant."

    def layoff(self, manager_name, employee_name):
        manager, target = self.require(manager_name), self.require(employee_name)
        if target is self.root or not self.is_descendant(target, manager):
            raise OrganizationError("The president cannot be laid off, and you may only lay off subordinates.")
        level, name = target.level, target.employee.name
        parent = target.parent
        source_vp = self.ancestor(target, "VP")
        destination = None
        if level == "Worker":
            destination = self.vacant_child(parent, "Worker")
            if destination is None:
                destination = next((p for p in self.positions() if p.level == level and p.is_vacant and self.ancestor(p, "VP") is source_vp), None)
            if destination is None:
                destination = next((p for p in self.positions() if p.level == level and p.is_vacant), None)
        else:
            destination = self.vacant_child(parent, level)
            if destination is None:
                destination = next((p for p in self.positions() if p.level == level and p.is_vacant and p is not target), None)
        target.employee = None
        if destination and destination is not target:
            destination.employee = Employee(name)
            return f"{name} was laid off and moved to another {level} position."
        return f"{name} was laid off; no comparable vacancy was available."

    def transfer(self, initiator_name, employee_name, destination_manager_name):
        initiator = self.require(initiator_name)
        target = self.require(employee_name)
        destination_manager = self.require(destination_manager_name)
        if initiator.level not in ("President", "VP"):
            raise OrganizationError("Only the president or a vice president may initiate transfers.")
        if not self.is_descendant(target, initiator):
            raise OrganizationError("The initiator must oversee the source position.")
        if initiator.level == "VP" and not self.is_descendant(destination_manager, initiator):
            raise OrganizationError("A vice president may transfer only within their organization.")
        if destination_manager.level not in CHILD_LEVEL or CHILD_LEVEL[destination_manager.level] != target.level:
            raise OrganizationError("Transfers must be to a vacant position at the same level.")
        destination = self.vacant_child(destination_manager, target.level)
        if destination is None or destination is target:
            raise OrganizationError("No suitable vacant destination position.")
        name = target.employee.name
        target.employee = None
        destination.employee = Employee(name)
        return f"Transferred {name} under {destination_manager_name}."

    def promote(self, receiving_manager_name, employee_name):
        manager, target = self.require(receiving_manager_name), self.require(employee_name)
        next_level = {"Worker": "Supervisor", "Supervisor": "VP"}.get(target.level)
        if next_level is None or manager.level not in CHILD_LEVEL or CHILD_LEVEL[manager.level] != next_level:
            raise OrganizationError("Promotions must be exactly one level; nobody can be promoted to president.")
        destination = self.vacant_child(manager, next_level)
        if destination is None:
            raise OrganizationError("The receiving manager has no vacant position for this promotion.")
        boundary = "Supervisor" if target.level == "Worker" else "VP"
        if self.ancestor(target, boundary) is self.ancestor(destination, boundary):
            raise OrganizationError("Promotion must be to a different organization.")
        name = target.employee.name
        target.employee = None
        destination.employee = Employee(name)
        return f"Promoted {name} to {next_level} under {receiving_manager_name}."

    def has_employee_below(self, position):
        return any(p.employee is not None or self.has_employee_below(p) for p in position.children)

    def display(self):
        if self.root.employee is None:
            return "(No file loaded. Type 'load FILE_NAME' first.)"
        lines = [f"President: {self.root.employee.name}"]
        def visit(parent, indent):
            for child in parent.children:
                if child.level == "Worker":
                    if child.employee:
                        lines.append(" " * indent + f"Worker: {child.employee.name}")
                elif child.employee or self.has_employee_below(child):
                    label = child.employee.name if child.employee else "[VACANT]"
                    title = "Vice President" if child.level == "VP" else "Supervisor"
                    lines.append(" " * indent + f"{title}: {label}")
                    visit(child, indent + 2)
        visit(self.root, 2)
        return "\n".join(lines)
