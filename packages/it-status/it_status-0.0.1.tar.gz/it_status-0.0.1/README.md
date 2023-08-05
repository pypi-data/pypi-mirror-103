# it_status

This Python package can be used for reporting to the MSK IT Status Dashboard.

## Installation

```
pip install it_status
```

## Usage

```
from it_status.status import ITStatus

# Setup the ITStatus instance with the URL to the application API and your tenant schema name
status = ITStatus(os.getenv("IT_STATUS_API_URL"), os.getenv("IT_STATUS_TENANT_SCHEMA"))

# These are the different ways of reporting events to your job - the job key can be found on the Jobs page
job_key = "<unique_job_key_here>"
status.ping(job_key, message="Ping test is working!")
status.status(job_key, message="CPU Utilization", data=70)
status.start(job_key, message="Process is starting")
status.error(job_key, message="Error in processes", log="Some log message goes here")
status.done(job_key, message="Process is complete", data=100)
status.log(job_key, message="Logging", log={"info": "This is a test log"})
```