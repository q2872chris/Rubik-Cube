from pathlib import Path

print(Path(__file__).absolute())

self_path = Path(__file__).absolute()
project_path = self_path.parent
directory = "project_files"
file_paths = list(Path(f"{project_path}/{directory}").glob("*.py"))
file_paths += [Path(f"{project_path}/main.py"), self_path]


# see if any lines exceed 79 characters
def test_file_line_lengths():
    total_count = 0
    print("Modules with line lengths above 79:")
    for path in file_paths:
        count = 0
        with open(path) as t:
            lines = [i.rstrip() for i in t.readlines()]
            for ind, line in enumerate(lines):
                length = len(line)
                if length > 79:
                    if count == 0:
                        print(f"{path.parts[-1]}:")
                    print(f"\tLine {ind + 1}: {length}")
                    count += 1
        total_count += count
        if count > 0:
            print("\tTotal issues:", count)
    if total_count == 0:
        print(None)
    print("Total issues across all modules:", total_count)


# includes function definition in line count
def test_file_function_lengths():
    # doesn't work properly with class's/blank lines/nested functions
    tab = lambda x: len(x) - len(x.lstrip())
    print("Function lengths across all modules:")
    for path in file_paths:
        with open(path) as t:
            count = 0
            func_tab = 0
            counting = False
            lines = [line.rstrip("\n") for line in t.readlines()]
            print(f"{path.parts[-1]}:")
            for ind, line in enumerate(lines):
                if line.lstrip()[:6] == "class ":
                    print(f"\tLine {ind + 1}, {line.strip()}")
                elif line.lstrip()[:4] == "def ":
                    counting = True
                    name = "function " + line.strip()[4:]
                    print(f"\tLine {ind + 1}, {name}", end=" ")
                    func_tab = tab(line)
                    count = 1
                elif counting:
                    if tab(line) <= func_tab:
                        counting = False
                        print(count)
                    else:
                        count += 1
            if counting:
                print(count)
            elif count == 0:
                print("\tNo functions found")


# Line counts don't include whitespace at the end of project_files
# Line counts excluding comments exclude all blank lines
def count_total_lines(exclude_self=False):
    total_count = 0
    total_count_no_whitespace = 0
    total_count_no_comments = 0
    print("Module line counts:")
    for path in file_paths:
        if exclude_self and path == self_path:
            continue
        with open(path) as t:
            lines = [i.strip() for i in t.readlines()]
            while len(lines) > 0 and lines[-1] == '':
                lines.pop(-1)
            count = len(lines)
            white_space = [i for i in lines if i != '']
            count_no_whitespace = len(white_space)
            count_no_comments = len([i for i in white_space if i[0] != '#'])
            total_count += count
            total_count_no_whitespace += count_no_whitespace
            total_count_no_comments += count_no_comments
            print(f"{path.parts[-1]}:")
            print("\tLines:", count)
            print("\tLines (excluding whitespace):", count_no_whitespace)
            print("\tLines (excluding comments):", count_no_comments)
    print("Total lines:", total_count)
    print("Total lines (excluding whitespace):", total_count_no_whitespace)
    print("Total lines (excluding comments):", total_count_no_comments)
    number_of_files = len(file_paths) - int(exclude_self)
    print("Total number of python project_files:", number_of_files)
    exclude_flag = "don't" if exclude_self else "do"
    print(f"Line length stats {exclude_flag} include this file.")


if __name__ == "__main__":
    # test_file_line_lengths()
    print()
    count_total_lines(True)
