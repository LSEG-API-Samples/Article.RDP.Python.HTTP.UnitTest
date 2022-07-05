#|-----------------------------------------------------------------------------
#|            This source code is provided under the MIT license             --
#|  and is provided AS IS with no warranty or guarantee of fit for purpose.  --
#|                See the project's LICENSE.md for details.                  --
#|           Copyright Refinitiv 2022.       All rights reserved.            --
#|-----------------------------------------------------------------------------

"""
Example Code Disclaimer:
ALL EXAMPLE CODE IS PROVIDED ON AN “AS IS” AND “AS AVAILABLE” BASIS FOR ILLUSTRATIVE PURPOSES ONLY. REFINITIV MAKES NO REPRESENTATIONS OR WARRANTIES OF ANY KIND, EXPRESS OR IMPLIED, AS TO THE OPERATION OF THE EXAMPLE CODE, OR THE INFORMATION, CONTENT, OR MATERIALS USED IN CONNECTION WITH THE EXAMPLE CODE. YOU EXPRESSLY AGREE THAT YOUR USE OF THE EXAMPLE CODE IS AT YOUR SOLE RISK.
"""

import unittest
import pandas as pd
import json
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import convert_pandas

class TestConsoleApp(unittest.TestCase):
        
    
    def test_can_convert_json_to_pandas(self):
        """
        Test that the convert_pandas function can convert JSON to Pandas
        """
        #Mock RDP ESG View Score valid response JSON
        with open('./fixtures/rdp_test_esg_fixture.json', 'r') as esg_fixture_input:
            mock_esg_data = json.loads(esg_fixture_input.read())
        
        result = convert_pandas(mock_esg_data)
        # Verify if result is none empty Pandas Dataframe object
        self.assertIsInstance(result, pd.DataFrame)
        self.assertFalse(result.empty)
    
    def test_can_convert_json_none(self):
        """
        Test that the convert_pandas function can handle none/empty input
        """

        with self.assertRaises(TypeError) as exception_context:
            result = convert_pandas(None)

        self.assertEqual(str(exception_context.exception),'Received invalid (None or Empty) JSON data')
    
    def test_can_convert_json_invalid(self):
        """
        Test that the convert_pandas function can invalid JSON input
        """

        with self.assertRaises(TypeError) as exception_context:
            result = convert_pandas({"message":"Invalid"})

        self.assertEqual(str(exception_context.exception),'Error converting JSON to Dataframe')
        
if __name__ == '__main__':
    unittest.main()