import os

for root, _, files in os.walk('.'):
    for file in files:
        if file.endswith('.py'):
            path = os.path.join(root, file)
            with open(path, 'r') as f:
                content = f.read()
            if 'from __future__ import annotations' not in content:
                lines = content.split('\n')
                insert_idx = 0
                if len(lines) > 0 and lines[0].startswith('"""'):
                    if lines[0].count('"""') >= 2 and len(lines[0]) > 3:
                        insert_idx = 1
                    else:
                        for i in range(1, len(lines)):
                            if '"""' in lines[i]:
                                insert_idx = i + 1
                                break
                lines.insert(insert_idx, 'from __future__ import annotations')
                with open(path, 'w') as f:
                    f.write('\n'.join(lines))
