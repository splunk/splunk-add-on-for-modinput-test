:warning: DO NOT INSTALL THIS ADDON ON ANY SPLUNK INSTANCE MANUALLY.

# Splunk Add-on for Modinput test

Splunk add-on for modinput test created to use the Splunk's custom rest API to handle the file actions such as read, write and delete. Follow the below mentioned URLs to perform file activity using Modinput test add-on.

## Create File:

#### URL:

`https://<splunk_ip>:<managment_port>/servicesNS/nobody/Splunk_TA_Modinput_Test/Splunk_TA_Modinput_Test_perform_crd_operation/<entry>/create`

#### Required params:

- **file_path**: The path of file along with file name
- **data**: content to be written in a file

#### Request Type: POST

## Delete file:

#### URL:

`https://<splunk_ip>:<managment_port>/servicesNS/nobody/Splunk_TA_Modinput_Test/Splunk_TA_Modinput_Test_perform_crd_operation/<entry>/delete`

#### Required params:

- **file_path**: The path of file which want to delete along with file name

#### Request Type: DELETE

## Read file:

#### URL:

`https://<splunk_ip>:<managment_port>/servicesNS/nobody/Splunk_TA_Modinput_Test/Splunk_TA_Modinput_Test_perform_crd_operation/<entry>/read`

#### Required params:

- **file_path**: The path of file for want to read the data

#### Request Type: GET

> **Note:** The file content is present under entry[0].get("content").get("file_content") while `output_mode` is set as `json`.

Please follow the below python script for better understanding.

```python
import requests

create_file_url = "https://<splunk_host_ip>:<splunk_port>/servicesNS/nobody/Splunk_TA_Modinput_Test/Splunk_TA_Modinput_Test_perform_crd_operation/<entry>/create"
payload = {"file_path": FILE_PATH, "data" : "Hello World"}
response = requests.request("POST", create_file_url, auth=(USERNAME, PASSWORD), data=payload, verify=False)

read_file_url = "https://<splunk_host_ip>:<splunk_port>/servicesNS/nobody/Splunk_TA_Modinput_Test/Splunk_TA_Modinput_Test_perform_crd_operation/<entry>/read"
payload = {"file_path": FILE_PATH}
response = requests.request("GET", read_file_url, auth=(USERNAME, PASSWORD), data=payload, verify=False)

delete_file_url = "https://<splunk_host_ip>:<splunk_port>/servicesNS/nobody/Splunk_TA_Modinput_Test/Splunk_TA_Modinput_Test_perform_crd_operation/<entry>/delete"
payload = {"file_path": FILE_PATH}
response = requests.request("DELETE", delete_file_url, auth=(USERNAME, PASSWORD), data=payload, verify=False)
```

> **Note:** `<entry>` in the URL is Splunk's interpretation way to differentiate the Splunk's default API with custom rest API. It is static and "should remain the same" for all the file actions scenarios.
