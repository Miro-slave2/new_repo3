from forecast.file_service import load_data
from forecast.forecast_service import *
from forecast.migration_data import MigrationData

import numpy as np
import pandas as pd

data = pd.read_csv("samples/migration.csv")

print(max_percent_change(data["emmigration"]))
print(moving_average_forecast(data["emmigration"].tolist(), 5, 5))