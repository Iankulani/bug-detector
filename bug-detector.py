# -*- coding: utf-8 -*-
"""
Created on Thurs Jan  1 11:42:47 2025

@author: IAN CARTER KULANI
"""

from colorama import Fore
import pyfiglet
import os
font=pyfiglet.figlet_format("BUG DETECTOR")
print(Fore.GREEN+font)


import re

# Function to read the C file
def read_file(file_path):
    """Reads the content of a C source file."""
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except FileNotFoundError:
        print(f"Error: File {file_path} not found.")
        return None

# Function to save the modified C code to a file
def save_file(file_path, content):
    """Saves the modified C content to a new file."""
    with open(file_path, 'w') as file:
        file.write(content)
    print(f"File saved as {file_path}")

# Function to check for undeclared variables
def check_undeclared_variables(code):
    """Checks for undeclared variables in the code."""
    undeclared_vars = []
    declared_vars = set()

    # Regex to match variable declarations (int, float, char, etc.)
    variable_declaration_pattern = r'\b(int|float|char|double|long|short|void)\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*;'
    matches = re.findall(variable_declaration_pattern, code)

    # Add declared variables to the set
    for match in matches:
        declared_vars.add(match[1])

    # Find variable usage
    variable_usage_pattern = r'\b([a-zA-Z_][a-zA-Z0-9_]*)\b'
    usage_matches = re.findall(variable_usage_pattern, code)

    # Check if any variable used is undeclared
    for var in usage_matches:
        if var not in declared_vars and var not in undeclared_vars:
            undeclared_vars.append(var)

    return undeclared_vars

# Function to check for uninitialized variables
def check_uninitialized_variables(code):
    """Checks for uninitialized variables in the code."""
    uninitialized_vars = []

    # Regex to match variable assignments and declarations
    assignments = re.findall(r'\b([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*[^;]+;', code)

    # Extract variable names from assignments
    initialized_vars = [re.match(r'\b([a-zA-Z_][a-zA-Z0-9_]*)\s*=', assignment).group(1) for assignment in assignments]

    # Regex to match variable declarations without initialization
    declarations = re.findall(r'\b(int|float|char|double|long|short|void)\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*;', code)

    # Check for uninitialized variables
    for declaration in declarations:
        if declaration[1] not in initialized_vars:
            uninitialized_vars.append(declaration[1])

    return uninitialized_vars

# Function to check for mismatched braces
def check_braces_balance(code):
    """Checks for mismatched braces in the code."""
    opening_braces = 0
    closing_braces = 0
    for char in code:
        if char == '{':
            opening_braces += 1
        elif char == '}':
            closing_braces += 1

    if opening_braces != closing_braces:
        return True
    return False

# Function to analyze the C code for bugs
def analyze_code(code):
    """Analyzes the C code for common bugs and issues."""
    bugs = []

    # Check for undeclared variables
    undeclared_vars = check_undeclared_variables(code)
    if undeclared_vars:
        bugs.append(f"Warning: Undeclared variables found: {', '.join(undeclared_vars)}.")

    # Check for uninitialized variables
    uninitialized_vars = check_uninitialized_variables(code)
    if uninitialized_vars:
        bugs.append(f"Warning: Uninitialized variables found: {', '.join(uninitialized_vars)}.")

    # Check for mismatched braces
    if check_braces_balance(code):
        bugs.append("Warning: Mismatched braces found in the code.")

    # Check for unreachable code (if there are return statements followed by code in the same block)
    unreachable_code_pattern = r'return\s+.*;.*\n.*'
    matches = re.findall(unreachable_code_pattern, code)
    if matches:
        bugs.append("Warning: Unreachable code detected after return statements.")

    return bugs

# Main function
def main():
    print("Binary Analysis tool created by Ian Carter Kulani")
    print("iancarterkulani@gmail.com\n")

    # Prompt user for the path to the C file
    file_path = input("Enter the path to the C source file:").strip()

    # Read the file content
    code = read_file(file_path)

    if code:
        # Analyze and check for bugs
        bugs = analyze_code(code)

        # Show the detected bugs to the user
        if bugs:
            print("\nDetected issues and bugs:")
            for bug in bugs:
                print(f"- {bug}")
        else:
            print("\nNo bugs detected. The code appears to be fine.")

        # Prompt the user for the path to save the modified file
        save_path = input("Enter the path to save the modified file: ").strip()
        save_file(save_path, code)

if __name__ == "__main__":
    main()
