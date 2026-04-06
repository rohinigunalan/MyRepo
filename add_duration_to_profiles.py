"""
Add duration_seconds = 43200 to all role-based profiles in ~/.aws/credentials
"""
import re
from pathlib import Path

def add_duration_to_profiles():
    creds_file = Path.home() / '.aws' / 'credentials'

    # Backup first
    backup_file = creds_file.with_suffix('.credentials.backup2')
    content = creds_file.read_text()
    backup_file.write_text(content)
    print(f"✓ Backup created: {backup_file}\n")

    lines = content.split('\n')
    new_lines = []
    profiles_updated = []

    i = 0
    while i < len(lines):
        line = lines[i]
        new_lines.append(line)

        # Check if this line has mfa_serial AND we haven't added duration_seconds yet
        if 'mfa_serial' in line and '=' in line:
            # Look ahead to see if duration_seconds already exists
            next_line_idx = i + 1
            has_duration = False

            if next_line_idx < len(lines):
                next_line = lines[next_line_idx]
                if 'duration_seconds' in next_line:
                    has_duration = True

            # Add duration_seconds if not already present
            if not has_duration:
                # Extract profile name from previous lines
                profile_name = None
                for j in range(i, max(0, i-10), -1):
                    if lines[j].startswith('[') and lines[j].endswith(']'):
                        profile_name = lines[j].strip('[]')
                        break

                new_lines.append('duration_seconds = 43200')
                profiles_updated.append(profile_name)

        i += 1

    # Write updated content
    creds_file.write_text('\n'.join(new_lines))

    print(f"✓ Updated {len(profiles_updated)} profiles:\n")
    for profile in profiles_updated:
        print(f"  - {profile}")

    print(f"\n✓ File updated: {creds_file}")
    print(f"\nTo restore backup if needed:")
    print(f"  cp {backup_file} {creds_file}")

if __name__ == '__main__':
    add_duration_to_profiles()
