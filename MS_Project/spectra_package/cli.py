# Peptide - Protein prediction CLI
# Unified test command: 'python cli.py pep_search -m test.mzml -f test.fasta'
#
# CLI commands have to be used explicitely!
# Tried 'click commands without names' like here https://github.com/pallets/click/issues/1180 or here
# https://stackoverflow.com/questions/65779025/click-cli-in-python-option-tags-are-not-recognized
# but didn't work. So for now commands have to be called by name.


import pandas as pd
import json

import click
from db_searcher import DbSearcher
from ms_file_parsing import MSFileParser
from protein_query import ProteinSearcher
import os
from pprint import pprint

#Init
MS_dataframe = pd.DataFrame()


@click.group()
def main():
    """CLI Entry Method"""
    pass


@main.command(name="parse")
@click.option("-m", "--ms_file", help=".mzML or .mzXML file containing MS data")
@click.option("-p", "--printdf", is_flag=True, default = False, help="Prints the parsed DataFrame and Size")
def parser_cli(ms_file, printdf):
    """The parser_cli method is a CLI version of the parser method that parses the MS file that is uploaded in either .mzML or .mzXML files"""
    ms_parsing = MSFileParser(ms_file_input=ms_file)
    MS_dataframe = ms_parsing.parser()
    print("File parsing...")
    if printdf:
        print("Print order: ", printdf)
        print("Data Dimensions (row col): ", MS_dataframe.shape)
        print(MS_dataframe)

    return MS_dataframe


# @main.command(name="analyse")
# @click.option("-a", '--analyse', help="Send the spectrum peak data to the pep-calc api for analysis. ")
# @click.option("-p", "--printdf", is_flag=True, default = False, help="Prints the parsed DataFrame and Size")
# def pep_api(MS_dataframe, printdf):
#     """Plot a Spectrum, if a spectrum file has been parsed."""
#     pep_calc = None
#     if MS_dataframe:
#         print("Sending data to API...")
#         # <peaks here?> Currently wants sequence, Nterm, Cterm. Returns json
#         # <preprocess here?> MS_dataframe
#         pep_calc = peptideBasics(MS_dataframe)
#         if not pep_calc:
#             print("No results were returned. Check your internet connection.")
#             return
#
#         if printdf:
#             print(pep_calc) # <print json here>
#
#     else:
#         print("No data found! Upload a mass spectroscopy file first.")


# CLI for Peptide search
# Unified test command: python cli.py pep_search -m test.mzML -f test.fasta 
@main.command(name="pep_search")
@click.option("-m", "--mzml_file", type=str, default = '', help="mzML file path. Absolute path should work, to prevent error when ä,ö,ü in path of openms input.")
@click.option("-f", "--fasta_file", type=str, default = '', help="Fasta file path. Absolute path should work, to prevent error when ä,ö,ü in path of openms input.")
@click.option("-p", "--peptide", is_flag=True, default = False, help="Only MS Peptide Analysis. Uses only local OpenMS pipeline and returns results. ELSE uses complete Pipeline ")
def dbsearch_cli(mzml_file, fasta_file,peptide):
    """Compares MassSpectronomy file with FASTA file to identify peptides"""

    assert mzml_file, "MzML file is missing!"
    assert fasta_file, "Fasta file is missing!"

    # Get file paths
    PATH = os.path.dirname(os.path.abspath(__file__))
    fasta_file = os.path.join(PATH, fasta_file)
    mzml_file = os.path.join(PATH, mzml_file)

    fasta_file = fasta_file.encode().decode("utf-8")
    mzml_file = mzml_file.encode().decode("utf-8")

    ### Call Peptide Search Script
    db_instance = DbSearcher(mzml_file=mzml_file,fasta_file=fasta_file)
    peptide_list = db_instance.db_searcher()

    # API Call when 'not only peptide analysis'
    if not peptide:

        ### Call Protein Search Script - PeptideAtlas API
        protein_instance = ProteinSearcher(peptide_list=peptide_list)
        protein_instance.download_protein_info()

        # Protein matches Results
        print("\n","Protein Atlas Results:")
        pprint(protein_instance.protein_matches)



if __name__ == "__main__":
    main()

