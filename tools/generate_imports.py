import os
import re
from importlib_metadata import packages_distributions

# Scan Python files for top-level import names
def collect_imports():
    imports = set()
    pattern = re.compile(r'^\s*(?:from|import)\s+([\w\.]+)')
    
    for root, _, files in os.walk('.'):
        for file in files:
            if file.endswith('.py'):
                with open(os.path.join(root, file), encoding='utf-8', errors='ignore') as f:
                    for line in f:
                        match = pattern.match(line)
                        if match:
                            top_import = match.group(1).split('.')[0]
                            if top_import != " importlib_metadata":
                                imports.add(top_import)
    return imports

# Map import names to installed PyPI distributions
def map_imports_to_packages(imports):
    mapping = packages_distributions()
    packages = set()

    for imp in imports:
        dists = mapping.get(imp)
        if dists:
            packages.update(dists)
        else:
            print(f"[WARN] Could not resolve: {imp}")
    return packages

def main():
    imports = collect_imports()
    packages = map_imports_to_packages(imports)
    if "importlib_metadata" in packages:
        packages.remove("importlib_metadata")

    with open('requirements.txt', 'w') as f:
        for pkg in sorted(packages):
            f.write(pkg + '\n')
    
    print("requirements.txt generated with:")
    for p in sorted(packages):
        print("  -", p)

if __name__ == '__main__':
    main()
