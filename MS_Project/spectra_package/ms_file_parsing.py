"""
method for parsing the mzXML/mzML file
The following attributes were extracted:
Base Peak, Base Peak Intensity, Highest Observed M/Z, Lowest Observed M/Z,Total Ion Current
All values (originally in str format) are appended into their list
"""
import xml.etree.ElementTree as ET
import os
import pandas as pd
import sys
from typing import Optional

class MSFileParser:
      """Class for parsing the MS file input and extracting the required fields"""

      def __init__(self,ms_file_input:str):
            self.ms_file_input = ms_file_input

      def parser(self)-> pd.DataFrame :
            """
            The parser method parses the MS file that is uploaded in either .mzML or .mzXML files

            :return: A data frame representing the attributes of MS and their values
            """

            if self.ms_file_input == None:
                  return "Upload a MS dataset"

            else:
                  _, file_extension = os.path.splitext(self.ms_file_input)
                  tree = ET.parse(self.ms_file_input)
                  root = tree.getroot()

                  # extraction for .mzML file
                  if file_extension == ".mzML":
                        base_peak_array = []
                        base_peak_intensity_array = []
                        highest_observed_mz = []
                        lowest_observed_mz = []
                        ion_current = []
                        # print([elem.tag for elem in root.iter()])  # prints all the tags
                        for item in root.iter():
                              if 'cvParam' in item.tag:
                                    if item.attrib['name'] == "base peak m/z": base_peak_array.append(item.attrib['value'])
                                    if item.attrib['name'] == "base peak intensity": base_peak_intensity_array.append(
                                          item.attrib['value'])
                                    if item.attrib['name'] == "highest observed m/z": highest_observed_mz.append(
                                          item.attrib['value'])
                                    if item.attrib['name'] == "lowest observed m/z": lowest_observed_mz.append(item.attrib['value'])
                                    if item.attrib["name"] == "total ion current": ion_current.append(item.attrib["value"])

                        mzMl_df = pd.DataFrame({"Base Peak": base_peak_array,
                                                "Base Peak Intensity": base_peak_intensity_array,
                                                "Highest Observed M/Z": highest_observed_mz,
                                                "Lowest Observed M/Z": lowest_observed_mz,
                                                "Total Ion Current": ion_current})

                        return mzMl_df
                  # extraction for .mzXML file
                  if file_extension == ".mzXML":
                        base_peak_intensity_array = []
                        base_peak_mz_array = []
                        high_mz_array = []
                        low_mz_array = []
                        ion_current=[]
                        # print([elem.tag for elem in root.iter()])
                        for item in root.iter():
                              if 'scan' in item.tag:
                                    base_peak_intensity_array.append(item.attrib['basePeakIntensity'])
                                    base_peak_mz_array.append(item.attrib['basePeakMz'])
                                    high_mz_array.append(item.attrib['highMz'])
                                    low_mz_array.append(item.attrib['lowMz'])
                                    ion_current.append(item.attrib["totIonCurrent"])
                        mzXMl_df = pd.DataFrame({"Base Peak": base_peak_mz_array,
                                                 "Base Peak Intensity": base_peak_intensity_array,
                                                 "Highest Observed M/Z": high_mz_array,
                                                 "Lowest Observed M/Z": low_mz_array,
                                                 "Total Ion Current":ion_current})

                        return mzXMl_df

if __name__ == "__main__":
      file_input = sys.argv[1]
      parsing_instance= MSFileParser(ms_file_input=file_input)
      output=parsing_instance.parser()
      print(output)