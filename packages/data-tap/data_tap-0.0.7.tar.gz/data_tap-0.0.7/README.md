# data-tap

A python wrapper that connects to multiple 3rd party resources for AWS.

[![Python Tests](https://github.com/DirksCGM/data-tap/actions/workflows/tests.yml/badge.svg)](https://github.com/DirksCGM/data-tap/actions/workflows/tests.yml)
[![Publish PyPi Package](https://github.com/DirksCGM/data-tap/actions/workflows/publish.yml/badge.svg)](https://github.com/DirksCGM/data-tap/actions/workflows/publish.yml)

# Google Analytics

The GoogleAnalyticsTap connects to the v4 GA api and returns data from Google Analytics.

```yaml
batch_dates: 'bool. enables batching of queries by date'
start_date: 'str. "yesterday", "today",  "3_days_ago" or "2020-01-01" etc...'
end_date: 'str. "yesterday", "today",  "3_days_ago" or "2020-01-01" etc...'
metrics:
  - expression: 'str. metric name'
dimensions:
  - name: 'str. dimension name'
pageSize: 'int. page size, defaults to 1000'
view_ids:
  - 'str. a list of view to iterate over'
```

```python
from datetime import datetime

import pandas as pd

from data_tap.google_tap.google_analytics import GoogleAnalyticsTap

ga_tap = GoogleAnalyticsTap(
    config_file='',
    creds_file='',
    auth_method='',
    service_account_email=''
)

dfA = pd.DataFrame()
for report in ga_tap.run_query():
    dfB = pd.DataFrame(report)
    dfA = dfA.append(dfB, ignore_index=True)

dfA.to_json(f"{datetime.utcnow()}.json")
```

# Google Search Console

The GoogleSearchConsoleTap connects to the v3 GSC api and returns data from Google Search Console.
Functionality to generate an authentication token is available.

```yaml
batch_dates: 'bool. enables batching of queries by date'
start_date: 'str. "yesterday", "today",  "3_days_ago" or "2020-01-01" etc...'
end_date: 'str. "yesterday", "today",  "3_days_ago" or "2020-01-01" etc...'
dimensions:
  - 'str. dimension name'
metrics:
  - 'str. metric name'
search_types:
  - 'str. available gsc search types'
site_urls:
  - 'str. website urls in question'
row_limit: 'int. max row limit is 25000'
```

```python
from datetime import datetime

import pandas as pd

from data_tap.google_tap.google_seach_console import GoogleSeachConsoleTap

gsc_tap = GoogleSeachConsoleTap(
    config_file='',
    creds_file='.pickle'
)

dfA = pd.DataFrame()
for report in gsc_tap.run_query():
    dfB = pd.DataFrame(report)
    dfA = dfA.append(dfB, ignore_index=True)

dfA.to_json(f"{datetime.utcnow()}.json")
```