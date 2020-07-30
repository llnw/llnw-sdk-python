
# Public Limelight python SDK for Limelight Networks services 

## Download and deployment

```
git clone <git_hub_url>
cd llnw-sdk-python
pip install -e .
```

## Example of usage config-api
```
import client:

from sdk.config_api import ConfigApiClient

Initialize client:

username = "{llnw_user}"
shared_key = "{llnw_shared_key}"

cl = ConfigApiClient('apis.llnw.com', username, shared_key)
```
Verify that it works
```
print(cl.get_status().json()) Should be returned something like this: {'version': '5.9-RC2', 'timestamp': '2020-04-03T15:39:03+0300', 'branch': 'ea4b4ca4c77cf8185d8b55381936a451bad87622', 'commitId': 'ea4b4ca4c77cf8185d8b55381936a451bad87622', 'mysqlConnection': {'connectionTime': '3'}, 'cfgMgmtConnection': {'available': 'true'}, 'remoteComponentsConnection': {'available': 'true'}, 'serviceDbConnection': {'available': 'true'}}
```

### How to create Delivery config 
    Generate delivery payload:
     ```
    from sdk.utils.config_api_helper.deilver import DeliverServiceInstanceObj
    a = DeliverServiceInstanceObj()
    a.generate_default('{llnw_shortname}', 'example.pub.llnw.com', 'w.example.orig.llnw.com', 'LLNW-Generic', 'https', 'https')
    
    {'accounts': [{'shortname': '{llnw_shortname}'}],
          'body': {'protocolSets': [{'options': [],
                            'publishedProtocol': 'http',
                            'sourceProtocol': 'http'}],
          'publishedHostname': 'example.pub.llnw.com',
          'publishedUrlPath': '',
          'serviceKey': {'name': 'delivery'},
          'serviceProfileName': 'LLNW-Generic',
          'sourceHostname': 'w.example.orig.llnw.com',
          'sourceUrlPath': ''}}
    ```
Using this payload you can create or validate delivery service instance:
    ```
    cl.validate_delivery_service_instance(a)
    ```
Validate call always return 200, but in body it has key 'Success' it can be True if everything is fine or False if an error occurs 
    ```
    cl.create_delivery_service_instance(a)
    ```
Return 200 if config was successfully created or error code(400, 403, etc) for errors  
                      
## Example of usage realtime-reporting-api
```
import client:

from sdk.realtime-reporting-api import RealtimeReportingClient

username = "{llnw_user}"
shared_key = "{llnw_shared_key}"

Initialize client:

cl = RealtimeReportingClient('apis.llnw.com', username, shared_key)
```

Verify that it works
```
print(cl.health_check().json()) ['OK']
```

### Get traffic data via realtime-reporting-api 
    response = cl.traffic(shortname="{llnw_shortname}",
                          service=[cl.SERVICE_HTTP, cl.SERVICE_HLS],
                          requestedFields=cl.TRAFFIC_REQUESTED_FIELDS,
                          timespan=cl.LAST_24_HOURS,
                          granularity=cl.GRANULARITY_FIVE_MINUTES)

or via general request and key: value argument (similar in limelight javaScript sdk) 

    response2 = cl2.request(**{"report": 'traffic', 
                               "shortname": "{llnw_shortname}",
                               "service": [cl2.SERVICE_HTTP, cl2.SERVICE_HLS],
                               "requestedFields": cl2.REQUESTED_FIELDS_INBYTES,
                               "timespan": cl2.LAST_24_HOURS,
                               "granularity": cl2.GRANULARITY_FIVE_MINUTES})
Congratulate you've done well


## Running the tests

Run tests

```
pytest -v --pyargs sdk.test
```