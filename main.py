import os

def print_tree(start_path='.', indent=''):
    entries = sorted(os.listdir(start_path))
    entries = [e for e in entries if e not in {'.git', '__pycache__', '.venv'}]  # Filter ignored dirs
    for i, entry in enumerate(entries):
        path = os.path.join(start_path, entry)
        is_last = i == len(entries) - 1
        connector = '└── ' if is_last else '├── '
        print(indent + connector + entry)
        if os.path.isdir(path):
            extension = '    ' if is_last else '│   '
            print_tree(path, indent + extension)

# Usage
print_tree('C:/Users/HP/Desktop/school-manager')
