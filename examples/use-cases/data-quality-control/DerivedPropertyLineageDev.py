import os

import lusid
import pandas as pd
import numpy as np
from datetime import datetime, timezone, date
import io
import json
import pytz
from IPython.core.display import HTML

# Then import the key modules from the LUSID package (i.e. The LUSID SDK)
import lusid as lu
import lusid.models as lm
from IPython.core.display_functions import display

# And use absolute imports to import key functions from Lusid-Python-Tools and other helper package

from lusid.utilities import ApiClientFactory
from lusidjam import RefreshingToken
from lusidtools.cocoon.cocoon import load_from_data_frame
from lusidtools.pandas_utils.lusid_pandas import lusid_response_to_data_frame
from lusidtools.jupyter_tools import StopExecution
from lusidtools.cocoon.cocoon_printer import (
    format_portfolios_response,
)

# Set DataFrame display formats
pd.set_option("max_colwidth", 100)
pd.set_option("display.max_columns", None)
pd.set_option("display.max_rows", None)
pd.options.display.float_format = "{:,.2f}".format
display(HTML("<style>.container { width:90% !important; }</style>"))

# Set the secrets path
secrets_path = os.getenv("FBN_SECRETS_PATH")

# For running the notebook locally
if secrets_path is None:
    secrets_path = os.path.join(os.path.dirname(os.getcwd()), "secrets.json")

api_factory = lu.utilities.ApiClientFactory(
        token=RefreshingToken(),
        api_secrets_filename = secrets_path,
        app_name="LusidJupyterNotebook")

api_status = pd.DataFrame(
    api_factory.build(lu.ApplicationMetadataApi).get_lusid_versions().to_dict()
)

display(api_status)

property_definitions_api: lu.PropertyDefinitionsApi = api_factory.build(lu.PropertyDefinitionsApi)
search_api: lu.SearchApi = api_factory.build(lu.SearchApi)

derivedPropsResponse = search_api.search_properties(filter="propertyDefinitionType eq 'DerivedDefinition'")

display(lusid_response_to_data_frame(derivedPropsResponse))

## Get ALL property definitions

all_properties = search_api.search_properties()
# going to have to loop through every one and start building out graphs
# and can then simplify at the end to remove duplicated sections of chains?
# filter to Derived properties only
# Identify all of the references in the formula to other datapoints
# recurse through tree and built out that data structure



