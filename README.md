# f8a-hpf-insights (maven)
**(fabric8-analytics-hpf-insights)**

HPF Matrix Factorizations for companion recommendation.
*HPF- Hierarchical Poisson Factorization*

## Index:
* [Supported Ecosystems](#supported-ecosystems)
* [Build Upon](#build-upon)
* [Deploy Locally](#to-run-locally-via-docker-compose)
* [Deploy on DevCluster](#to-run-on-dev-cluster)
* [Run Unit Tests](#unit-tests)
* [Run Load Tests](#to-run-load-testing-for-recommendation-api)
* [Footnotes](#footnotes)
    * [Coding Standards](#coding-standards)
    * [Code Complexity Measurement](#code-complexity-measurement)
* [Additional links](#additional-links)

## Supported ecosystems:
* Maven - Last trained at: 2018-08-08 11:30 IST(UTC +5:30)

## Build upon:
* https://github.com/arindamsarkar93/hcpf

## To run locally via docker-compose:

* Setup Minio and start Minio server so that `hpf-insights` is loaded as a folder inside it upon running. To use AWS S3 instead of Minio add your AWS S3 credentials in the next step instead of Minio credentials.
* Create a `.env` file and add credentials to it.
* In the `.env` set the `AWS_S3_ENDPOINT_URL` to `<blank>` for using AWS S3 and to `http://ip:port` for using Minio.
* `source .env`
* `docker-compose build`
* `docker-compose up`
* `curl  http://0.0.0.0:6006/` should return `status: ok`


## To run on dev-cluster:

* `cp secret.yaml.template secret.yaml`
* Add your AWS S3 credentials to `secret.yaml`
* `oc login`
* `oc new-project hpf-insights`
* `oc create -f secret.yaml`
* `oc process -f openshift/template.yaml -o yaml|oc create -f -` If you want to update the template.yaml and redeploy it, then do `oc process -f openshift/template.yaml -o yaml|oc apply -f -` Use apply instead of create for subsequent re-deployments.
* Go your Openshift console and expose the route
* `curl <route_URL>` should return `status:ok`

## Unit Tests
There's a script named `runtests.sh` that can be used to run all unit tests. The unit test coverage is reported as well by this script.

Usage:
```
./runtests.sh
```

## To run load testing for recommendation API:

* `pip install locustio==0.8.1`
* Bring up the service.
* `locust -f perf_tests/locust_tests.py --host=<URL of the service>`

## Footnotes:

#### Check for all possible issues

The script named `check-all.sh` is to be used to check the sources for all detectable errors and issues. This script can be run w/o any arguments:

```
./check-all.sh
```

Expected script output:

```
Running all tests and checkers
  Check all BASH scripts
    OK
  Check documentation strings in all Python source file
    OK
  Detect common errors in all Python source file
    OK
  Detect dead code in all Python source file
    OK
  Run Python linter for Python source file
    OK
  Unit tests for this project
    OK
Done

Overall result
  OK
```

An example of script output when one error is detected:

```
Running all tests and checkers
  Check all BASH scripts
    Error: please look into files check-bashscripts.log and check-bashscripts.err for possible causes
  Check documentation strings in all Python source file
    OK
  Detect common errors in all Python source file
    OK
  Detect dead code in all Python source file
    OK
  Run Python linter for Python source file
    OK
  Unit tests for this project
    OK
Done

Overal result
  One error detected!
```

Please note that the script creates bunch of `*.log` and `*.err` files that are temporary and won't be commited into the project repository.

#### Coding standards:

- You can use scripts `run-linter.sh` and `check-docstyle.sh` to check if the code follows [PEP 8](https://www.python.org/dev/peps/pep-0008/) and [PEP 257](https://www.python.org/dev/peps/pep-0257/) coding standards. These scripts can be run w/o any arguments:

```
./run-linter.sh
./check-docstyle.sh
```

The first script checks the indentation, line lengths, variable names, whitespace around operators etc. The second
script checks all documentation strings - its presence and format. Please fix any warnings and errors reported by these
scripts.

List of directories containing source code, that needs to be checked, are stored in a file `directories.txt`

#### Code complexity measurement

The scripts `measure-cyclomatic-complexity.sh` and `measure-maintainability-index.sh` are used to measure code complexity. These scripts can be run w/o any arguments:

```
./measure-cyclomatic-complexity.sh
```
and:

```
./measure-maintainability-index.sh
```

The first script measures cyclomatic complexity of all Python sources found in the repository. Please see [this table](https://radon.readthedocs.io/en/latest/commandline.html#the-cc-command) for further explanation how to comprehend the results.

The second script measures maintainability index of all Python sources found in the repository. Please see [the following link](https://radon.readthedocs.io/en/latest/commandline.html#the-mi-command) with explanation of this measurement.

You can specify command line option `--fail-on-error` if you need to check and use the exit code in your workflow. In this case the script returns 0 when no failures has been found and non zero value instead.

#### Dead code detection

The script `detect-dead-code.sh` can be used to detect dead code in the repository. This script can be run w/o any arguments:

```
./detect-dead-code.sh
```

Please note that due to Python's dynamic nature, static code analyzers are likely to miss some dead code. Also, code that is only called implicitly may be reported as unused.

Because of this potential problems, only code detected with more than 90% of confidence is reported.

List of directories containing source code, that needs to be checked, are stored in a file `directories.txt`

#### Common issues detection

The script `detect-common-errors.sh` can be used to detect common errors in the repository. This script can be run w/o any arguments:

```
./detect-common-errors.sh
```

Please note that only semantical problems are reported.

List of directories containing source code, that needs to be checked, are stored in a file `directories.txt`

#### Check for scripts written in BASH

The script named `check-bashscripts.sh` can be used to check all BASH scripts (in fact: all files with the `.sh` extension) for various possible issues, incompatibilities, and caveats. This script can be run w/o any arguments:

```
./check-bashscripts.sh
```

Please see [the following link](https://github.com/koalaman/shellcheck) for further explanation, how the ShellCheck works and which issues can be detected.

#### Code coverage report

Code coverage is reported via the codecov.io. The results can be seen on the following address:

[code coverage report](https://codecov.io/gh/fabric8-analytics/f8a-hpf-insights)


## Additional links:
* [Feedback logic](https://github.com/fabric8-analytics/f8a-hpf-insights/wiki/Feedback-Logic)
* [Pushing Image to Docker Hub](https://ropenscilabs.github.io/r-docker-tutorial/04-Dockerhub.html)
* [PAPER: Scalable Recommendation with Poisson Factorization](https://arxiv.org/abs/1311.1704)
* [PAPER: Hierarchical Compound Poisson Factorization](https://arxiv.org/abs/1604.03853)
