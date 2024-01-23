# itau-collab-dashboard

## Introduction

This project implements a pipeline to retrieve data and metrics from Webex devices. The logic to gather these metrics is defined in the pipeline class, which specifies the metrics to be collected and the frequency of the queries. The Webex class defines the query to retrieve the metrics and the authentication process on Webex. Three classes have been implemented, each utilizing a different model of authentication (Services, Integration, On-premises). For automated processes, we recommend using Webex services.

For development, we recommend using the development token available at [webex developer](https://developer.webex.com/docs/getting-started). Simply set this token in the environment variable WEBEX_SERVICE_ACCESS_TOKEN.

For more information about Webex devices metrics, refer to [xAPI docs](https://roomos.cisco.com/xapi) and [Webex xAPI query](https://developer.webex.com/docs/api/v1/xapi/query-status). For more about services, refer to [Webex Services](https://developer.webex.com/docs/service-apps). For more about Integrations, refer to [Webex Integrations](https://developer.webex.com/docs/integrations).

## Installation

Clone the repository to your local machine.
Navigate to the project directory.

Install the necessary Python packages using pip:

```bash
 pip install -r requirements.txt
```

Copy the env-example to .env and set the asked values. You just need to add the values for the api mode selected on WEBEX_API_MODE variable.

```yaml
# API MODE Service, Integration, OnPrem
WEBEX_API_MODE=Service

# WEBEX SERVICE CREDENTIALS
WEBEX_SERVICE_CLIENT_ID=
WEBEX_SERVICE_CLIENT_SECRET=

WEBEX_SERVICE_ACCESS_TOKEN=
WEBEX_SERVICE_REFRESH_TOKEN=
# WEBEX INTEGRATION CREDENTIALS

WEBEX_INTEGRATION_CLIENT_ID=
WEBEX_INTEGRATION_CLIENT_SECRET=
WEBEX_INTEGRATION_REDIRECT_URI=

```

## How to Run
To execute the program, navigate to the project's root directory in your terminal and execute the following command:

```bash
python run_pipeline.py
```

Please note: Do not run '__main.py__', unless you are using Webex Integration. This code runs a web server needed to retrieve the user token requested by Webex Integration. The main script for executing the project is 'run_pipeline.py'.


## Contribution

We welcome contributions from everyone. Feel free to make a pull request or open an issue. If you're new to open source or git, we are more than happy to help.

Contact
If you have any questions, feel free to reach out to us.

Thank you for showing interest in our project. Happy coding!