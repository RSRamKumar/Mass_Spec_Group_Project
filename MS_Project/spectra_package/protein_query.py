import os
import json
import logging
import re
import pandas as pd
import time


import requests


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class ProteinSearcher:
    """ PeptideAtlas Query Class

            Args:
                peptide_list: List of peptides to compare to the database.

            Returns:
                protein_matches: List of the matched proteins.
    """

    def __init__(self, peptide_list: pd.DataFrame):
        self.peptide_list = peptide_list
        self.protein_matches = None


    def download_protein_info(self):
        """
                Make API requests for each peptide in the peptide list.

                Will try to establish a server connection. API is buffered according to query size.

                Raises:
                    Logs errors when the connection could not be established.
                    Logs errors when no database entry could be found.
                    Warning. Results are empty.
                    Warning when API is throttled.

                """
        # Peptide list to local variable
        peptide_list = self.peptide_list['Peptide hit sequence']

        # Safety check for querying more than 10 peptides
        n_peptides = len(peptide_list)

        if n_peptides < 10:
            api_policy = 0
            logger.warning(f"The peptide list is {n_peptides} entries long.\nCalling API ...")
        elif n_peptides >= 10 and n_peptides < 50:
            api_policy = 1
            logger.warning(f"The peptide list is {n_peptides} entries long. API calls are delayed by 0.25s.\nCalling API ...")
        elif n_peptides >= 50 and n_peptides < 200:
            api_policy = 2
            logger.warning(f"The peptide list is {n_peptides} entries long. API calls are delayed by 0.5s.\nCalling API ...")
        else:
            api_policy = 3
            logger.warning(f"The peptide list is {n_peptides} entries long. API is currently capped for more than 200 calls.\nCalling API ...")


        # API - Loop through Peptides and collect results

        protein_matches = dict()

        for peptide in peptide_list:

            # Preprocessing for (Oxidation) or other parenthesises
            if "(" in peptide:
                peptide = re.sub(r'\([^)]*\)', '', peptide)


            ### API - Query

            if api_policy == 0:
                pass
            elif api_policy == 1:
                time.sleep(0.25)
            elif api_policy == 2:
                time.sleep(0.5)
            else:
                logger.error(f"API call stopped due to overflow.")
                return


            api_query = f"http://www.peptideatlas.org/api/promast/v1/map?peptide={peptide}" # &output=json if no header?

            print("Api_query with peptide:", peptide)
            r = requests.get(api_query, headers={"Accept": "application/json"})

            if r.status_code != 200:
                logger.error(f"{api_query} returned bad status code: {r.status_code}")
                break

            # Positive Server Result
            if r.json()['status'] == 'OK':
                # Mapping Results
                if 'mappings' in r.json():
                    mapping_result = r.json()['mappings']
                else:
                    mapping_result = []
                    logger.warning(f"0 mappings found")

                # Add to peptide Dictionary
                protein_matches[peptide] = mapping_result

            # Negative Server Result
            if r.json()['status'] == 'ERROR':
                logger.error(f"API request returned 'ERROR'. Something wrong with query?")
                return

        if len(protein_matches) > 0:
            self.protein_matches = protein_matches
            return protein_matches
        else:
            logger.warning(f"Warning. Results are empty.")

