with open('version.txt') as f:
    version = f.read().strip()

major, patch = version.split('.')
if int(patch) < 10:
    new_version = f"{major}.0{int(patch) + 1}"
else:
    new_version = f"{major}.{int(patch) + 1}"

# Write back
with open('version.txt', 'w') as f:
    f.write(new_version)
print(f"\033[34m!\033[0m Updated version to: {new_version}")