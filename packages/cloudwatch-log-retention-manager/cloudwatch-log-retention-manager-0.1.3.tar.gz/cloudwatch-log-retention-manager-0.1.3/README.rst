================================
cloudwatch-log-retention-manager
================================

.. image:: https://img.shields.io/pypi/v/cloudwatch-log-retention-manager.svg
   :target: `PyPI link`_

.. _PyPI link: https://pypi.org/project/cloudwatch-log-retention-manager


CloudWatch Logs Retention Manager is a configurable tool that can be used to validate or enforce CloudWatch log retention rules.

Unlike other tools in this space, the ``cwlrm`` provides flexibility through the use of configuration, this configuration can apply to a subset of log groups - useful when working in shared environments.

Usage
=====

Install ``cwlrm`` through pip and create a ``config.yml`` file within your project.

::

    ➜ cwlrm --help
    usage: cwlrm [-h] [--version] [-u] [-c CONFIGFILE] [-s] [-v] [-vv]

    CloudWatch logs retention manager

    optional arguments:
      -h, --help            show this help message and exit
      --version             show program's version number and exit
      -u, --update          update settings in AWS
      -c CONFIGFILE, --config CONFIGFILE
                            location of config.yaml
      -s, --show_all        show all log groups in filter
      -v, --verbose         set loglevel to INFO
      -vv, --very-verbose   set loglevel to DEBUG

Once installed, all that is needed is a ``config.yml`` file containing the log group patterns and retention periods to set.
The tool supports a **Compliance** mode, where the live AWS environment will be validated
against the described config file.

When you are ready to apply the changes, run `cwlrm -u` to enforce Compliance as defined.

The format of the `config.yml` file is as follows:

* A single root object names retentionPatterns
* An array of child objects consisting of the following attributes:

1. **name** - mandatory - names a section of log groups to be processed
2. **logPrefix** - optional - the pattern of logs to apply the group to - default: all logs
3. **retentionInDays** - optional - the log retention period to set - default: Forever
4. **override** - optional - if set will require the exact retentionInDays values to be compliant, otherwise any log retention is considered compliant - default: false
5. **showAlways** - optional - when set, will show all log groups that match irrespective of their compliance - default: false

Optionally the **logPrefix** can be an array of patterns to be collected into the matching group.

Example::

    retentionPatterns:
      - name: CodeBuild jobs
        logPrefix: /aws/codebuild/
        retentionInDays: 14
        override: true
        showAlways: true

      - name: AWS Glue Crawlers
        logPrefix: /aws-glue/crawlers
        retentionInDays: 14

      - name: Specific application lambda logs
        logPrefix:
         - /aws/lambda/Application1
         - /aws/lambda/Application2
         - /aws/lambda/Application3
        retentionInDays: 45

      - name: Lambda logs
        logPrefix: /aws/lambda
        retentionInDays: 30

      - name: API Gateway access logs
        logPrefix: /aws/api-gateway/
        retentionInDays: 120

      - name: API Gateway Execution Logs
        logPrefix: API-Gateway-Execution-Logs
        retentionInDays: 120

      - name: All remaining log groups
        showAlways: true
        retentionInDays: 90

**IMPORTANT Note:** For each run a log group will only be processed by a single control - the first control to process the log group will be the active one, if subsequent patterns are to match that same log group it will be ignored.



Examples
========

Some example config files.

Simple retention pattern
------------------------

::

    retentionPatterns:
      - name: AWS Glue Crawlers
        logPrefix: /aws-glue/crawlers
        retentionInDays: 14

      - name: CloudFront Lambda Function logs
        logPrefix: /aws/cloudfront/LambdaEdge
        retentionInDays: 30

This configuration will ensure that all glue-crawler and lambdaedge function logs have a retention set, when applied will set 15 and 30 days respectivly.

Specific compliance retention period
------------------------------------

::

    retentionPatterns:
      - name: CodeBuild jobs
        logPrefix: /aws/codebuild/
        retentionInDays: 14
        override: true

This configuration will enforce that all codebuild log groups have specifically a 14 day retention period - any other value will be considered "Non Compliant"

Logs that should be retained Forever
------------------------------------

::

    retentionPatterns:
      - name: Application audit logs
        logPrefix: /application/audit/
        showAlways: true

If a log group contains some sort of audit required for long term archive, Compliance can be achieved by specifiying the logGroup pattern and omitting the *retentionInDays* parameter.
In this scenario log groups without retention periods are considered Compliant, and are configured to be shown on each execution.


Show all remaining log groups
-----------------------------

::

    retentionPatterns:
      - name: API Gateway access logs
        logPrefix: /aws/api-gateway/
        retentionInDays: 30

      - name: Lambda API logs
        logPrefix: /aws/lambda/
        retentionInDays: 30

      - name: API Gateway Execution Logs
        logPrefix: API-Gateway-Execution-Logs
        retentionInDays: 30

      - name: All remaining log groups
        showAlways: true
        retentionInDays: 90

A normal operation of ``cwlrm`` will only process the specified
log groups (as selected by the logPrefix) - in some cases you may
want to apply a default to the entire account, this can be done
through the omission of the ``logPrefix`` attribute.  Any log group
matching the previous conditions will


.. _pyscaffold-notes:

Note
====

This project has been set up using PyScaffold 4.0.1. For details and usage
information on PyScaffold see https://pyscaffold.org/.
