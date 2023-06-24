# BatchCrypt

![__init__](https://github.com/MugoSquero/BatchCrypt/raw/main/welcome.png)

BatchCrypt is a command-line tool that allows you to encrypt (obfuscate) batch files to enhance their security. It modifies and encodes batch file lines, ensuring that sensitive information within the batch files remains protected.

## Features

- Encrypts batch files by modifying and encoding the lines
- Supports both single file encryption and batch directory encryption
- Generates an encrypted batch file with the "_enced.bat" extension
- Provides informative logging in the `batch_crypt.log` file

## Prerequisites

- Python 3.5 or higher
- Required Python packages can be installed using the `requirements.txt` file.

## Installation

1. Clone the BatchCrypt repository:

   ```bash
   git clone https://github.com/MugoSquero/BatchCrypt.git
   ```

2. Navigate to the project directory:

   ```bash
   cd BatchCrypt
   ```

3. Install the required Python packages:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

To encrypt a single batch file, use the following command:

```bash
python main.py -i /path/to/input_file.bat
```

To encrypt all batch files in a directory, use the following command:

```bash
python main.py -r /path/to/batch_directory
```

## Output

The encrypted batch file will be saved in the same directory as the original batch file with the suffix "_enced.bat". For example, if the original batch file is named "script.bat", the encrypted file will be named "script_enced.bat".

## Logging

The tool generates a log file named `batch_crypt.log` in the same directory as the script. This log file contains any errors or exceptions encountered during the encryption process.

## Disclaimer

Please note that BatchCrypt is provided as-is without any warranty. Use it responsibly and ensure that you have appropriate permissions to encrypt batch files.

## License

This project is licensed under the [MIT License](LICENSE).

## Credits

BatchCrypt is created and maintained by [MugoSquero](https://github.com/MugoSquero).
