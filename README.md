# SDG query execution


## Setup

### Requirements
We recommend to install the prerequisites using the packaging system of your distribution. On Debian/Ubuntu use:

```
sudo apt install build-essential python3-dev python3-pip python3-venv git
```

on RHEL/CentOS use:

```
sudo yum install gcc gcc-c++ python34-devel python34-pip python34-virtualenv git
```

On Ubuntu 14.04, python3-venv is not available. Please use python3.5-venv instead.

On RHEL/CentOS selinux is enabled by default. This can result in unexpected errors, depending on where you store the RDMO source code on the system. While the prefereble way is to configure it correctly (which is beyond the scope of this documentation), you can also set selinux to permissive or disabled in /etc/selinux/config (and reboot afterwards).

### Clone project
Firstly create a directory by cloning the corresponding repository:
```
git clone https://github.com/ETspielberg/sdg_query_execution.git
```


### Install requirements

The programme is written as python flask application. 
Necessary dependencies are listed in the requirements.txt and can be installed via

```
$ pip install -r requirements.txt
```

### Configuration

The configuration file holds all the local information and credentials needed to make the API calls to Scopus, Altmetric and Unpaywall.
In addition a general data directory is provided used to store intermediate and result files.
For obtaining API keys for Scopus, Scival and Altmetric, please refer to [https://dev.elsevier.com](https://dev.elsevier.com/) and [https://api.altmetric.com](https://api.altmetric.com/) 
The place of the configuration file needs to be declared as environmet variable (vide infra), we recommend to use a local path in the home directory.

```
LIBINTEL_DATA_DIR = "${USER_HOME}/.libintel/data"
LIBINTEL_USER_EMAIL = "mike.smith@example.com"

ELSEVIER_URL = "https://api.elsevier.com"
SCOPUS_API_KEY = "<api-key>"
SCIVAL_API_KEY = ""

ALTMETRIC_URL = "https://api.altmetric.com/v1/"
ALTMETRIC_API_KEY = "<api-key>"

UNPAYWALLL_API_URL = "https://api.unpaywall.org/my/request"
```

### Start up into development server

To start the application the virtual environment has to be activated.
After that some environmental parameters need to be set for the flask application.
For a development version the following code can be executed:

 
On Windows Powershell:
```
./venv/Scripts/activate
$env:FLASK_APP="start.py"
$env:FLASK_ENV="development"
$env:LIBINTEL_SETTINGS = "${USER_HOME}\\.libintel\\config\\query_execution.cfg"
python -m flask run
```

On the Linus Command Prompt:
```
./venv/Scripts/activate
export FLASK_APP="start.py"
export FLASK_ENV="development"
export LIBINTEL_SETTINGS = "${USER_HOME}\\.libintel\\config\\query_execution.cfg"
python -m flask run
```

the environment variables PLASK_APP and FLASK_ENV are needed by the the flask framework, while the LIBINTEL_SETTINGS point toward the configuration file (vide supra).
The last line runs the program and opens a server accessible under 
`http://127.0.0.1:5000`


### Start up into production server

If you want to run the script in a production enviroment, Vladikk has written nice introduction in his blog post [Serving Flask with Nginx](https://vladikk.com/2013/09/12/serving-flask-with-nginx-on-ubuntu/)  

## Running an analysis

Analyses are started using a HTTP POST request, for example using cURL:

```
curl -X POST -H "Content-Type: application/json" 
    --data '<query data in json>'
 http://127.0.0.1:5000/query_execution
```

The query defining terms are provided as a JSON document. The structure is as follows: 

```
{
    "topic": "<topic query>",
    "author": "<author query>",
    "year": "<year query>",
    "subject": "<subject query>",
    "title": "<title query>",
    "auth_id": "<author id query>"
}
```

Data can also be provided by a simple Web-Frontend.

## Output
_to be done_ 
