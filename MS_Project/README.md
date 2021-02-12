# Group 01 - Spectra Project

Project for Group 01

Title: Compute the Number of Peptides of a Given Total Mass

Members: Ayberk, Linus, Fumilayo, Ram Kumar

Steps:

1. This package requires the installation of the package `pyopenms`. It can installed by the following command: `pip install pyopenms`.

2. CLI command for doing a MS file parsing operation:

`python cli.py parse -m file.mzXML -p`

3. CLI command for performing peptide identification and database search:
For this tasks, the pyopenms library is employed. Therefore only .mzML file only could be employed.


`python cli.py pep_search -m test.mzML -f test.fasta`