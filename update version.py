with open('version.txt') as f:
    version = f.read().strip()

major, patch = version.split('.')
major, patch = int(major), int(patch)

if patch >= 32:
    major += 1
    patch = 0
else:
    patch += 1
new_version = f"{major}.{patch:02d}"

with open('version.txt', 'w') as f:
    f.write(new_version)
print(f"\033[34m!\033[0m Updated version to: {new_version}")