from command_processor import CommandProcessor
from organization import OrganizationError

class Main:
    """Program entry point; keeps the interactive loop separate from business logic."""
    @staticmethod
    def run():
        processor = CommandProcessor()
        print("The Dysfunctional Organization System")
        print("Type 'help' for commands. Type 'exit' to end.")
        while True:
            try:
                command = input("> ")
            except (EOFError, KeyboardInterrupt):
                print()
                break
            try:
                result = processor.execute(command)
                if result == "__EXIT__":
                    break
                if result:
                    print(result)
            except OrganizationError as exc:
                print(f"Error: {exc}")
        print("Goodbye.")

if __name__ == "__main__":
    Main.run()
