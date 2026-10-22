class Employee:
    """
    Wrapper class for employee data.
    Stores an employee's unique name.
    """
    def __init__(self, name: str):
        self.name = " ".join(name.strip().split())
        if not self.name:
            raise ValueError("Employee name cannot be empty.")

    def __str__(self):
        return self.name
