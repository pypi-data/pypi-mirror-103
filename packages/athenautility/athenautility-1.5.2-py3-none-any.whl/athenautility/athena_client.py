#!/usr/bin/env python
import json
import os
import logging
import requests
import pandas as pd
from IPython.display import display, HTML


logger = logging.getLogger(__name__)

STATUS = "status"
DATA = "data"
MESSAGE = "message"
SUCCESS = "SUCCESS"
FAILED = "FAILED"

# Athena services
API_VALIDATE_USER = "/ccf/services/validate_user"
API_GET_ATHENA_DATABASES = "/ccf/services/get_athena_databases"
API_GET_ATHENA_TABLES = "/ccf/services/get_athena_tables"
API_QUERY_ATHENA_TABLE = "/ccf/services/query_athena_table"
API_RUN_QUERY_ON_ATHENA = "/ccf/services/run_query_on_athena"
API_SAVE_DATA_TO_S3 = "/ccf/services/save_data_to_s3"

# Environment Variables
_USER_ID: str = 'USER_ID'
_ACCESS_TOKEN: str = 'ACCESS_TOKEN'
_ID_TOKEN: str = 'ID_TOKEN'
_USER_ROLE_ID: str = 'USER_ROLE'
_CCF_SERVICES_HOST: str = 'CCF_SERVICES_HOST'
_USER_S3_BUCKET: str = 'USER_S3_BUCKET'


TABLE_STYLES = [dict(selector="caption", props=[("text-align", "inline"), ("font-size", "100%"), ("color", 'black')]),
                dict(selector="td", props=[('border', '1px solid black'), ("text-align", "left")]),
                dict(selector="th", props=[('border', '1px solid black'), ("text-align", "center")])]


################################################################################
# Athena Client
################################################################################
def connect():
    # TODO - Add user validation
    try:
        _user_id = os.getenv(_USER_ID, None)
        _user_role_id = os.getenv(_USER_ROLE_ID, None)
        _access_token = os.getenv(_ACCESS_TOKEN, None)
        _id_token = os.getenv(_ID_TOKEN, None)
        _ccf_services_url = os.getenv(_CCF_SERVICES_HOST, None)
        _user_s3_bucket = os.getenv(_USER_S3_BUCKET, None)

        _headers = {
            "content-type": "application/json",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/89.0.4389.90 Safari/537.36",
            "userid": _user_id,
            "roleid": _user_role_id,
            "idtoken": _id_token,
            "accesstoken": _access_token

        }
        _cookie = dict(sessionid=os.getenv(_ACCESS_TOKEN, None))

        r = requests.post(_ccf_services_url + API_VALIDATE_USER, headers=_headers,
                          cookies=_cookie)
        response = r.json()
        if response[STATUS] == SUCCESS:
            athena_client = AthenaClient(ccf_services_url=_ccf_services_url, headers=_headers, cookie=_cookie,
                                         user_s3_bucket=_user_s3_bucket)
            return athena_client
        else:
            print(response[MESSAGE])

    except requests.exceptions.HTTPError:
        print("Http error occurred")
    except requests.exceptions.ConnectionError:
        print("Connection error occurred")
    except requests.exceptions.Timeout:
        print("Request timed out...")
    except requests.exceptions.RequestException:
        print("RequestException occurred")


class AthenaClient:

    def __init__(self, ccf_services_url, headers, cookie, user_s3_bucket):
        self._ccf_services_url = ccf_services_url
        self._headers = headers
        self._cookie = cookie
        self._user_s3_bucket = user_s3_bucket
        print("Connection is successful...")

    def databases(self, result_as_df=True):
        """Returns all the schemas available in Athena"""
        try:
            payload = json.dumps({})
            r = requests.post(self._ccf_services_url + API_GET_ATHENA_DATABASES, data=payload, headers=self._headers,
                              cookies=self._cookie)
            response = r.json()
            if response[STATUS] == SUCCESS:
                if not result_as_df and isinstance(response[DATA], (dict, list)):
                    response_as_df = pd.DataFrame.from_dict(response[DATA]).style.set_caption(
                        "Databases").hide_index().set_table_styles(TABLE_STYLES)
                    return display(response_as_df)
                else:
                    response_as_df = pd.DataFrame.from_dict(response[DATA])
                    return response_as_df
            else:
                print(response[MESSAGE])

        except requests.exceptions.HTTPError:
            print("Http error occurred")
        except requests.exceptions.ConnectionError:
            print("Connection error occurred")
        except requests.exceptions.Timeout:
            print("Request timed out...")
        except requests.exceptions.RequestException:
            print("RequestException occurred")

    def tables(self, schema_name, result_as_df=True):
        """Returns all the tables present in a schema"""
        try:
            payload = json.dumps({"schema_name": schema_name})
            r = requests.post(self._ccf_services_url + API_GET_ATHENA_TABLES, data=payload, headers=self._headers,
                              cookies=self._cookie)
            response = r.json()
            if response[STATUS] == SUCCESS:
                if not result_as_df and isinstance(response[DATA], (dict, list)):
                    response_as_df = pd.DataFrame.from_dict(response[DATA]).style.set_caption(
                        "Tables").hide_index().set_table_styles(TABLE_STYLES)
                    return display(response_as_df)
                else:
                    response_as_df = pd.DataFrame.from_dict(response[DATA])
                    return response_as_df
            else:
                print(response[MESSAGE])

        except requests.exceptions.HTTPError:
            print("Http error occurred")
        except requests.exceptions.ConnectionError:
            print("Connection error occurred")
        except requests.exceptions.Timeout:
            print("Request timed out...")
        except requests.exceptions.RequestException:
            print("RequestException occurred")

    def top(self, schema_name, table_name, limit=None, result_as_df=True):
        """Returns records from a table"""
        try:
            payload = json.dumps({"schema_name": schema_name, "table_name": table_name, "limit": limit})
            r = requests.post(self._ccf_services_url + API_QUERY_ATHENA_TABLE, data=payload, headers=self._headers,
                              cookies=self._cookie)
            response = r.json()
            if response[STATUS] == SUCCESS:
                if not result_as_df and isinstance(response[DATA], (dict, list)):
                    table_header = f'Top {limit} records of table {schema_name}.{table_name}' if limit else f'Top 100 records of table <i>{schema_name}.{table_name}</i>'
                    response_as_df = pd.DataFrame.from_dict(response[DATA]).style.set_caption(
                        table_header).hide_index().set_table_styles(TABLE_STYLES)
                    return display(response_as_df)
                else:
                    response_as_df = pd.DataFrame.from_dict(response[DATA])
                    return response_as_df
            else:
                print(response[MESSAGE])

        except requests.exceptions.HTTPError:
            print("Http error occurred")
        except requests.exceptions.ConnectionError:
            print("Connection error occurred")
        except requests.exceptions.Timeout:
            print("Request timed out...")
        except requests.exceptions.RequestException:
            print("RequestException occurred")

    def run_query(self, query_string, result_as_df=True):
        """Run a specified query"""
        try:
            payload = json.dumps({"query_string": query_string})
            r = requests.post(self._ccf_services_url + API_RUN_QUERY_ON_ATHENA, data=payload, headers=self._headers,
                              cookies=self._cookie)
            response = r.json()
            queries = list(filter(None, query_string.split(';')))
            if response[STATUS] == SUCCESS:
                if not result_as_df and isinstance(response[DATA], (dict, list)):
                    if len(queries) > 1:
                        results = [pd.DataFrame.from_dict(item).style.set_caption(
                            f"""Query results for <i>\"{queries[i]};\"</i>""").hide_index().set_table_styles(TABLE_STYLES) for i, item in
                                   enumerate(response[DATA])]
                        return display(*results)
                    else:
                        result = pd.DataFrame.from_dict(response[DATA]).style.set_caption(
                            f"""Query results for <i>\"{queries[0]};\"</i>""").hide_index().set_table_styles(
                            TABLE_STYLES)
                        return display(result)
                else:
                    if len(queries) > 1:
                        results = [pd.DataFrame.from_dict(item) for item in response[DATA]]
                    else:
                        results = pd.DataFrame.from_dict(response[DATA])
                    return results
            else:
                print(response[MESSAGE])

        except requests.exceptions.HTTPError:
            print("Http error occurred")
        except requests.exceptions.ConnectionError:
            print("Connection error occurred")
        except requests.exceptions.Timeout:
            print("Request timed out...")
        except requests.exceptions.RequestException:
            print("RequestException occurred")

    def save_data(self, data, file_name):
        """Returns records from a table"""
        try:
            data = data.to_dict(orient='records')
            if os.path.splitext(file_name)[1] == '':
                file_name = f'{file_name}.csv'
            payload = json.dumps({"file_name": file_name, "s3_bucket": self._user_s3_bucket, "data": data})
            r = requests.post(self._ccf_services_url + API_SAVE_DATA_TO_S3, data=payload, headers=self._headers,
                              cookies=self._cookie)
            response = r.json()
            if response[STATUS] == SUCCESS:
                print(response[MESSAGE])
                return response[DATA]
            else:
                print(response[MESSAGE])

        except requests.exceptions.HTTPError:
            print("Http error occurred")
        except requests.exceptions.ConnectionError:
            print("Connection error occurred")
        except requests.exceptions.Timeout:
            print("Request timed out...")
        except requests.exceptions.RequestException:
            print("RequestException occurred")
