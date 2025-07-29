#Write me a python file that will read my code files I specify and write to a local text file all the code with the filename identified

import os
import glob

# Specify the directory containing the code files
directory = 'D:/projects/rfp_accelerator_v2/'

# Define file patterns to include
file_patterns = [
    # Backend Python files
    'backend/*.py',
    
    # Frontend configuration files
    'frontend-vite/package.json',
    'frontend-vite/vite.config.ts',
    'frontend-vite/tsconfig.json',
    'frontend-vite/tsconfig.app.json',
    'frontend-vite/tsconfig.node.json',
    'frontend-vite/eslint.config.js',
    'frontend-vite/index.html',
    
    # Frontend source files
    'frontend-vite/src/*.tsx',
    'frontend-vite/src/*.ts',
    'frontend-vite/src/*.css',
    'frontend-vite/src/components/*.tsx',
    'frontend-vite/src/components/*.css',
]

# Specify the output file path
output_file = 'D:/temp/tmp_codebase/codebase.txt'

# Create output directory if it doesn't exist
os.makedirs(os.path.dirname(output_file), exist_ok=True)

# Collect all files
all_files = []
for pattern in file_patterns:
    full_pattern = os.path.join(directory, pattern)
    matched_files = glob.glob(full_pattern)
    all_files.extend(matched_files)

# Remove duplicates and sort
all_files = sorted(list(set(all_files)))

# Open the output file in write mode
with open(output_file, 'w', encoding='utf-8') as f:
    f.write(f"Codebase Export - {len(all_files)} files\n")
    f.write('='*80 + '\n\n')
    
    # Iterate over all collected files
    for filepath in all_files:
        try:
            # Get relative path for cleaner output
            relative_path = os.path.relpath(filepath, directory)
            
            # Open the file in read mode
            with open(filepath, 'r', encoding='utf-8') as code_file:
                # Write the filename to the output file
                f.write(f"<File: {relative_path}>\n")
                # Write the code from the file to the output file
                f.write(code_file.read())
                # Add a separator between files
                f.write('\n' + '-'*80 + '\n\n')
        except Exception as e:
            f.write(f"<File: {relative_path}>\n")
            f.write(f"Error reading file: {str(e)}\n")
            f.write('-'*80 + '\n\n')

print(f"Codebase exported to: {output_file}")
print(f"Total files processed: {len(all_files)}")