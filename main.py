# -*- coding: utf-8 -*-
import base64
import re
import sys
import os
import argparse
from tqdm import tqdm
import logging
logging.basicConfig(
    filename='batch_crypt.log',
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
from concurrent.futures import ThreadPoolExecutor
from colorama import Fore, Style
from platform import system
from os import system as execute_command


def modify_batch_lines(batch_lines):
    count_lines = 0

    # Modify batch lines containing '%' characters and replace them with '%%'
    for batch_line in batch_lines:
        if re.search("%", batch_line) and batch_line.count("%") == 2:
            new_line = batch_line.replace("%", "%%")
            batch_line = "cmd /c " + new_line
            batch_lines[count_lines] = batch_line
        count_lines += 1

    return batch_lines


def generate_encoded_lines(result_file, batch_lines):
    # Encode and write modified batch lines to the result file
    total_lines = sum(len(batch) for batch in batch_lines)
    
    with tqdm(total=total_lines, desc="Processing", unit="line", leave=True, dynamic_ncols=True) as pbar:
        for batch in batch_lines:
            for line in batch:
                if line == '':
                    continue
                elif line == '\n':
                    continue
                elif line == '>':
                    continue
                elif line == '<':
                    continue
                if line == '%':
                    command = ''
                elif line == '>':
                    command = ''
                else:
                    line_bytes = line.encode("utf-8")
                    line_base64 = base64.b64encode(line_bytes)
                    line_base64 = line_base64.decode('utf-8')
                    line_base64 = line_base64.replace('=', '')
                    command = ("set {}={}".format(line_base64, line))
                    result_file.write(command)
                    result_file.write('\n')
                pbar.update(1)
        pbar.update(1)

    # Remove duplicate lines and write the formatted batch file
    result_file.close()
    with open(result_file.name, "r", encoding='utf-8') as read_result:
        result_lines = read_result.readlines()
        distinct_lines = set(result_lines)
        with open(result_file.name, "w", encoding='utf-8') as result:
            result.write("@echo off\n")
        result_file = open(result_file.name, "a", encoding='utf-8')
        for i in distinct_lines:
            result_file.write(i)

    result_file.write("cls\n")


def encode_lines(result_file_path, batch_lines):
    # Encode and write batch lines to the result file
    with open(result_file_path, "a", encoding='utf-8') as result_file:
        for batch in batch_lines:
            if batch[0] == ':':
                can_execute = False
            else:
                can_execute = True
            if not can_execute:
                result_file.write(batch)
                continue
            for line in batch:
                if line == '%':
                    encoded_line = '%'
                else:
                    line_bytes = line.encode('utf-8')
                    line_base64 = base64.b64encode(line_bytes)
                    encoded_line = line_base64.decode('utf-8')
                    encoded_line = encoded_line.replace('=', '')
                if encoded_line == 'Cg':
                    exc = '\n'
                elif encoded_line == 'Pg':
                    exc = '>'
                elif encoded_line == 'Jg':
                    exc = '&'
                elif encoded_line == 'PA':
                    exc = '<'
                elif encoded_line == 'IQ':
                    exc = '!'
                else:
                    if encoded_line != '%':
                        exc = "%" + encoded_line + "%"
                    else:
                        exc = "%"

                result_file.write(exc)


def process_batch_file(file_path):
    # Open the specified batch file and read its contents into a list
    with open(file_path, "r", encoding='utf-8') as input_file:
        batch_lines = input_file.readlines()

    # Create a new file for storing the encrypted batch file
    result_file_path = os.path.splitext(file_path)[0] + "_enced.bat"
    result_file = open(result_file_path, "w", encoding='utf-8')
    result_file.write("setlocal EnableDelayedExpansion\n")

    # Modify batch lines
    batch_lines = modify_batch_lines(batch_lines)

    # Call the function to generate the encoded batch lines
    generate_encoded_lines(result_file, batch_lines)

    # Call the function to encode and write the lines to the result file
    encode_lines(result_file_path, batch_lines)

    # Close the result file
    result_file.close()

    # Read the contents of the result file in binary mode, convert to hexadecimal, and prepend with a byte order mark
    with open(result_file_path, "rb") as bat_bytes:
        byte_data = bat_bytes.read().hex()
    byte_order_mark = 'fffe0d0a'
    with open(result_file_path, "wb") as bat_file:
        bat_file.write(bytes.fromhex(byte_order_mark + byte_data))

    # Print a message indicating that the encrypted batch file has been saved
    print(f"Encrypted Batch File Saved in '{result_file_path}'!")


def process_batch_directory(batch_directory):
    batch_directory = os.path.abspath(batch_directory)  # Convert to absolute path

    # Process all files in the batch directory
    if not os.path.isdir(batch_directory):
        raise ValueError("Batch directory does not exist.")

    batch_files = [
        os.path.join(batch_directory, f)
        for f in os.listdir(batch_directory)
        if os.path.isfile(os.path.join(batch_directory, f))
    ]

    with ThreadPoolExecutor() as executor:
        futures = []
        for batch_file in batch_files:
            future = executor.submit(process_batch_file, batch_file)
            futures.append(future)

        # Wait for all tasks to complete
        for future in futures:
            future.result()


def main():
    try:
        # Check the operating system and set console color for Windows
        if system() == "Windows":
            execute_command("color")

        # Print a stylized ASCII art logo
        print(Fore.GREEN +
              """
  ____        _       _      ____                  _ 
 | __ )  __ _| |_ ___| |__  / ___|_ __ _   _ _ __ | |_
 |  _ \ / _` | __/ __| '_ \| |   | '__| | | | '_ \| __|
 | |_) | (_| | || (__| | | | |___| |  | |_| | |_) | |_
 |____/ \__,_|\__\___|_| |_|\____|_|   \__, | .__/ \__|
                                       |___/|_|
                                        - MugoSquero
        """ + Style.RESET_ALL)

        # Create an ArgumentParser object
        parser = argparse.ArgumentParser(description="Batch Script Encrypter")

        # Add command-line arguments+
        parser.add_argument("-i", dest="input_file", help="Input file path")
        parser.add_argument("-r", dest="batch_directory", help="Directory containing batch files for encryption")

        # Parse the command-line arguments
        args = parser.parse_args()

        # Extract the arguments
        file_path = args.input_file
        batch_directory = args.batch_directory

        # Validate the arguments
        if not file_path and not batch_directory:
            parser.error("You must specify either an input file or a batch directory.")
        if file_path and batch_directory:
            parser.error("You can only specify either an input file or a batch directory, not both.")

        if file_path:
            # Process a single file
            process_batch_file(file_path)
        elif batch_directory:
            # Process all files in the batch directory
            process_batch_directory(batch_directory)

    except FileNotFoundError as fnf_error:
        logging.error("File not found: %s", str(fnf_error))
    except PermissionError as perm_error:
        logging.error("Permission error: %s", str(perm_error))
    except ValueError as val_error:
        logging.error(str(val_error))
    except Exception as ex:
        logging.error("An error occurred: %s", str(ex))



if __name__ == '__main__':
    main()
