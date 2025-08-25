import os

class FileComparator:
    def __init__(self, print_found_files: bool, excluded_paths: list[str]):
        self.root_files = set()
        self.print_found_files = print_found_files
        self.excluded_paths = excluded_paths

    def compare_files(self, log_file):
        should_process = False
        for line in log_file:
            if line.strip() == "":
                should_process = False
            elif line.startswith("Directory /"):
                should_process = True
            elif should_process:
                self.process_dir(line)


    def process_dir(self, line: str):
        idx = line.find('/')
        path = line[idx:].strip()

        if self.excluded_paths is not None and any(excluded_path in path for excluded_path in self.excluded_paths):
            return

        if path.endswith("/.") or path.endswith("/.."):
            return
                
        if path not in self.root_files:
            print(f"\033[31mNot found: {path}\033[0m")
            with open("./console.log", "a", encoding='utf-8') as output_file:
                output_file.write(f"Not found: {path}\n")
        elif self.print_found_files:
            print(f"\033[32mFound: {path}\033[0m")
            with open("./console.log", "a", encoding='utf-8') as output_file:
                output_file.write(f"Found: {path}\n")
            self.root_files.remove(path)
        

    def load_root_files(self, root_dir):
        for dirpath, dirnames, filenames in os.walk(root_dir):
            for filename in filenames:
                path = str(os.path.join(dirpath, filename)).replace(root_dir, "").replace("\\", "/")
                if self.excluded_paths is not None and any(excluded_path in path for excluded_path in self.excluded_paths):
                    continue
                self.root_files.add(path)


def clear_screen() -> None:
    os.system("cls" if os.name == "nt" else "clear")


def main():
    clear_screen()
    print("\033[1;36mWelcome to the FilesCompare!\033[0m")

    root_dir = input("Enter the root directory path: ")
    log_file_path = input("Enter the TestDisk log file path: ")
    print_found_files = (input("Do you wish to print found files to console and log file? (y/n) [y]: ").strip().lower() == "y" or "y") == "y"
    print_extra_files = (input("Do you wish to print files that are not found in TestDisk's log to console and log file? (y/n) [y]: ").strip().lower() == "y" or "y") == "y"
    excluded_paths = input("Enter any excluded paths line-separated, they need to contain the part to be excluded: ").strip().split("|")

    if len(excluded_paths) == 1 and excluded_paths[0] == "":
        excluded_paths = None

    if not os.path.exists(root_dir):
        print(f"\033[31mRoot directory '{root_dir}' does not exist.\033[0m")
        return

    if not os.path.exists(log_file_path):
        print(f"\033[31mLog file '{log_file_path}' does not exist.\033[0m")
        return

    comparator = FileComparator(print_found_files, excluded_paths)
    comparator.load_root_files(root_dir)
    with open(log_file_path, 'r+', encoding='utf-8') as log_file:
        comparator.compare_files(log_file)

    if print_extra_files:
        for root_file in comparator.root_files:
            print(f"\033[33mExtra file: {root_file}\033[0m")
            with open("./console.log", "a", encoding='utf-8') as output_file:
                output_file.write(f"Extra file: {root_file}\n")

    print("\033[32mComparison complete.\033[0m")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\033[31mProcess interrupted by user.\033[0m")
    except Exception as e:
        print(f"\n\033[31mAn error occurred: {e}\033[0m")
    input("Press Enter to exit...")