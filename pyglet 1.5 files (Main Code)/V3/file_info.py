from pathlib import Path
from utilities.general_utilities import safe_sum


def get_root(start: Path, flag="main.py") -> Path:
    path = start.resolve()
    while path != path.parent:
        if (path / flag).exists():
            return path
        path = path.parent
    raise FileNotFoundError(f"Could not find {flag} in any parent directories.")


self_path = Path(__file__).absolute()
root = get_root(self_path)
file_paths = [path for path in root.rglob("*.py")]


# see if any lines exceed 79 characters
def test_line_lengths(max_length=79):
    total_count = 0
    print("Modules with line lengths above 79:")
    for path in file_paths:
        count = 0
        with open(path) as t:
            lines = [i.rstrip() for i in t.readlines()]
            for ind, line in enumerate(lines):
                length = len(line)
                if length > max_length:
                    if count == 0:
                        print(f"{path.relative_to(root)}:")
                    print(f"\tLine {ind + 1}: {length}")
                    count += 1
        total_count += count
        if count > 0:
            print("\tTotal issues:", count)
    if total_count == 0:
        print(None)
    print("Total issues across all modules:", total_count)


class line_count_container:
    def __init__(self, path: Path):
        self.files = 1
        self.name = path.relative_to(root)
        self.count, self.count_no_whitespace, self.count_no_comments = \
            self.count_module_lines(path)

    @staticmethod
    def count_module_lines(path: Path):
        with open(path) as reader:
            lines = [i.strip() for i in reader.readlines()]
            while len(lines) > 0 and lines[-1] == '':
                lines.pop(-1)
            count = len(lines)
            white_space = [i for i in lines if i != '']
            count_no_whitespace = len(white_space)
            count_no_comments = len([i for i in white_space if i[0] != '#'])
        return count, count_no_whitespace, count_no_comments

    def print(self, print_name=True):
        messages = ["{0}: {1}", "{0} (excluding whitespace): {2}",
                    "{0} (excluding whitespace and comments): {3}"]
        sep = "\n\t" if print_name else "\n"
        message = f"{self.name}:" if print_name else ""
        message += ("\n\t" if print_name else "") + sep.join(messages)
        message += f"{sep}Total files: {self.files}" if self.files > 1 else ""
        return message.format("Lines" if self.files == 1 else "Total lines",
                              self.count, self.count_no_whitespace,
                              self.count_no_comments)

    def __str__(self):
        return self.print()

    def __add__(self, other):
        self.name = f"{self.name} & {other.name}"
        self.count += other.count
        self.count_no_whitespace += other.count_no_whitespace
        self.count_no_comments += other.count_no_comments
        self.files += 1
        return self


# Line counts don't include whitespace at the end of project_files
# line count > line count no whitespace > line count no comments
def count_total_lines(sorting_mode="None", reverse=False,
                      exclude_self=False, exclude_init=False,
                      exclude_list=()):
    print("Module line counts:")
    counts = [line_count_container(path) for path in file_paths
              if (path != self_path or not exclude_self) and
              ("__init__.py" not in str(path) or not exclude_init) and
              not any(i in str(path) for i in exclude_list)]
    if sorting_mode in ("count", "whitespace", "comments"):
        counts.sort(key=lambda x: getattr(x, sorting_mode), reverse=reverse)
    print(*counts, sep="\n")
    print(safe_sum(counts).print(print_name=False))
    message = "Line length stats %sinclude %s."
    print(message % ("don't " if exclude_self else "", "this file"))
    print(message % ("don't " if exclude_init else "", "__init__.py files"))
    # Add statements for exclude list



if __name__ == "__main__":
    # test_line_lengths()
    count_total_lines(sorting_mode="count", exclude_self=True,
                      exclude_init=True,
                      exclude_list=("spare_code.py", ))


