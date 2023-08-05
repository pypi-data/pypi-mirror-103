import json
import logging
from requests import Request, Session, Response, api
import sys
from urllib.parse import urlencode


log_levels = ["CRITICAL", "ERROR", "INFO", "DEBUG"]
formatter = logging.Formatter(fmt="[%(levelname)s] %(asctime)s.%(msecs)06d %(message)s", datefmt="%d-%b-%y %H:%M:%S")
log_file = "pytest.log"
log_severity = "DEBUG"


def _console_handler():
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    return console_handler


logger = logging.getLogger("pytest_logger")
logger.setLevel(log_severity)
logger.addHandler(_console_handler())
debug = logger.debug


def send_request(endpoint_url, method_type: str = "POST", session="", data="", additional_headers=None, query_path=""):
    s = Session()
    header = {'Content-Type': 'application/json', 'user-agent': 'PostmanRuntime/7.26.8'}

    if session:
        session = {'Authorization': f'Bearer {session}'}
        header.update(session)
    if query_path:
        endpoint_url += "?" + urlencode(query_path).replace('+', "&2B")

    prepared_request = Request(method=method_type,
                               url=endpoint_url,
                               headers=header,
                               data=json.dumps(data),
                               ).prepare()

    debug(f"Sending request to: {endpoint_url} \n with type: {method_type} \n and data: {data}")
    response = s.send(prepared_request)
    debug(f"Response is: {response.json()}")
    return response


def response_has_status_code(response: Response, *status_codes: [int]) -> None:
    debug(f"Check response has one of {status_codes} network_status code")
    actual_status_code = response.status_code
    assert actual_status_code in status_codes, \
        f"Expected response network_status codes: {status_codes}\n" + \
        "Actual network_status code: {actual_status_code}"


def json_has_key_with_value(response: Response, key: str, value="") -> None:
    j_son = response.json()
    response_key_value = j_son.get(key)
    debug_msg = f"Check response json have key: {key} with value: {value}"

    if not value:
        debug_msg = f"Check response json have key: {key} is not empty" + f" with value: {response_key_value}"

    debug(debug_msg)
    if value:
        assert value == response_key_value,\
            f"Expected '{key}' field value isn't equal to:{value}\n" + \
            f"Actual '{key}' field value:{response_key_value}"


def send_file_request(endpoint_url, session, file, data=None):
    debug(f"Sending request to: {endpoint_url} \n with file")
    response = api.post(endpoint_url, files=file, headers={'Authorization': f'Bearer {session}'}, data=data)
    debug(f"Response is: {response.json()}")
    return response
