import argparse
import logging
import sys
import yaml
import boto3

from log_retention_compliance import __version__

__author__ = "Steve Mactaggart"
__copyright__ = "Steve Mactaggart"
__license__ = "MIT"

_logger = logging.getLogger(__name__)

# Prices last updated 2021-04-27 (see updatepricing.py for how to update)
REGION_COSTS = {
    'ap-northeast-1': 0.033,
    'af-south-1': 0.036,
    'eu-central-1': 0.0324,
    'us-west-1': 0.033,
    'eu-south-1': 0.032,
    'us-east-1': 0.03,
    'eu-west-2': 0.0315,
    'sa-east-1': 0.0408,
    'ap-northeast-2': 0.0314,
    'eu-north-1': 0.028,
    'ca-central-1': 0.033,
    'eu-west-1': 0.03,
    'ap-south-1': 0.03,
    'us-west-2': 0.03,
    'ap-southeast-1': 0.03,
    'ap-southeast-2': 0.033,
    'ap-east-1': 0.03,
    'ap-northeast-3': 0.033,
    'us-east-2': 0.03,
    'eu-west-3': 0.0315,
    'me-south-1': 0.03
}


# ---- Python API ----
# The functions defined in this section can be imported by users in their
# Python scripts/interactive interpreter, e.g. via
# `from log_retention_compliance.skeleton import fib`,
# when using this Python module as a library.

def retention_name(rule_retention):
    return "{} days".format(rule_retention) if rule_retention else "Forever"


def format_bytes(size):
    # 2**10 = 1024
    power = 2**10
    n = 0
    power_labels = {0 : '', 1: 'kilo', 2: 'mega', 3: 'giga', 4: 'tera'}
    while size > power:
        size /= power
        n += 1
    return size, power_labels[n]+'bytes'


class LogManager:

    processed_log_groups = []
    config = None
    region_cost = None

    def __init__(self) -> None:
        super().__init__()
        self.client = boto3.client('logs')
        self.region = boto3.session.Session().region_name

        if not self.region_cost:
            if self.region not in REGION_COSTS:
                print("[WARNING] Unable to resolve CloudWatch logs pricing for '{}', defaulting to 'us-east-1' - "
                      "cost calculations may not be accurate.".format(self.region))
                self.region_cost = REGION_COSTS['us-east-1']
            else:
                self.region_cost = REGION_COSTS[self.region]

    def calculate_cost(self, rule_bytes):
        return self.region_cost * rule_bytes / (1024 * 1204 * 1024)

    def read_config(self, configfile):

        with open(configfile) as file:
            # The FullLoader parameter handles the conversion from YAML
            # scalar values to Python the dictionary format
            self.config = yaml.load(file, Loader=yaml.FullLoader)

        _logger.info("Loaded {} log group retention rules".format(len(self.config["retentionPatterns"])))

    def execute(self, update=False, show_all=False, show_cost=True, show_individual_cost=True):

        compliant = True

        total_bytes = 0
        paginator = self.client.get_paginator('describe_log_groups')
        for rule in self.config["retentionPatterns"]:

            rule_name = rule["name"]
            rule_retention = rule.get("retentionInDays")
            source_prefix_list = rule.get("logPrefix")
            override = rule.get("override")
            show_compliant = rule.get("showAlways") or show_all

            print("Processing {} ({}) - set retention to {}".format(rule_name,
                                                                    source_prefix_list,
                                                                    retention_name(rule_retention)))

            rule_bytes = 0

            if not isinstance(source_prefix_list, list):
                source_prefix_list = [source_prefix_list]

            for group_prefix in source_prefix_list:
                if group_prefix:
                    pages = paginator.paginate(
                        logGroupNamePrefix=group_prefix
                    )
                else:
                    pages = paginator.paginate()

                for response in pages:
                    for log_group in response["logGroups"]:
                        name = log_group["logGroupName"]
                        current_retention = log_group.get("retentionInDays")
                        stored_bytes = log_group.get("storedBytes")

                        _logger.info("Retrieved group {} [current retention {}] - {} bytes".format(name,
                                                                                                   retention_name(current_retention),
                                                                                                   stored_bytes))

                        if name in self.processed_log_groups:
                            continue

                        rule_bytes += stored_bytes
                        total_bytes += stored_bytes

                        self.processed_log_groups.append(name)

                        log_bytes_calc = format_bytes(stored_bytes)
                        log_cost = self.calculate_cost(stored_bytes)
                        cost = ""
                        if show_individual_cost:
                            cost = " ({:.2f} {} - ${:.2f}/month)".format(log_bytes_calc[0], log_bytes_calc[1], log_cost)

                        if not rule_retention:
                            if show_compliant:
                                print("   - [Compliant] {} retention {}{}".format(name,
                                                                                  retention_name(current_retention),
                                                                                  cost))
                        elif current_retention == rule_retention:
                            if show_compliant:
                                print("   - [Compliant] {} retention {}{}".format(name,
                                                                                  retention_name(current_retention),
                                                                                  cost))
                        else:
                            if not current_retention or override:
                                compliant = False
                                print("   - {}Updating retention on {} from {} to {}{}".format("" if update else "[Not Compliant] ",
                                                                                               name,
                                                                                               retention_name(current_retention),
                                                                                               retention_name(rule_retention),
                                                                                               cost))
                                if update:
                                    self.client.put_retention_policy(
                                        logGroupName=name,
                                        retentionInDays=rule_retention
                                    )
                            else:
                                print("   - [Compliant] Retention modified on {} from {} to {}{}".format(name,
                                                                                                         retention_name(current_retention),
                                                                                                         retention_name(rule_retention),
                                                                                                         cost))

            if show_cost:
                rule_bytes_calc = format_bytes(rule_bytes)
                rule_cost = self.calculate_cost(rule_bytes)
                print("Total log groups size {:.2f} {} - ${:.2f}/month".format(rule_bytes_calc[0],
                                                                               rule_bytes_calc[1],
                                                                               rule_cost))

            print()

        if show_cost:
            total_bytes_calc = format_bytes(total_bytes)
            total_cost = self.calculate_cost(total_bytes)
            print("Total CloudWatch logs size {:.2f} {} - ${:.2f}/month".format(total_bytes_calc[0],
                                                                                total_bytes_calc[1],
                                                                                total_cost))

        return compliant

# ---- CLI ----
# The functions defined in this section are wrappers around the main Python
# API allowing them to be called directly from the terminal as a CLI
# executable/script.


def parse_args(args):
    """Parse command line parameters

    Args:
      args (List[str]): command line parameters as list of strings
          (for example  ``["--help"]``).

    Returns:
      :obj:`argparse.Namespace`: command line parameters namespace
    """
    parser = argparse.ArgumentParser(description="CloudWatch logs retention manager")
    parser.add_argument(
        "--version",
        action="version",
        version="log-retention-compliance {ver}".format(ver=__version__),
    )
    parser.add_argument("-u", "--update", dest="update", help="update settings in AWS", default=False, action="store_true")
    parser.add_argument("-c", "--config", dest="configfile", help="location of config.yaml", default="config.yml")
    parser.add_argument("-s", "--show_all", dest="show_all", help="show all log groups in filter", default=False, action="store_true")
    parser.add_argument("-sc", "--show_cost", dest="show_cost", help="total cost per groups", default=False, action="store_true")
    parser.add_argument("-ic", "--show_individual_cost", dest="show_individual_cost", help="show storage cost for each log group in filter", default=False, action="store_true")

    parser.add_argument(
        "-v",
        "--verbose",
        dest="loglevel",
        help="set loglevel to INFO",
        action="store_const",
        const=logging.INFO,
    )
    parser.add_argument(
        "-vv",
        "--very-verbose",
        dest="loglevel",
        help="set loglevel to DEBUG",
        action="store_const",
        const=logging.DEBUG,
    )
    return parser.parse_args(args)


def setup_logging(loglevel):
    """Setup basic logging

    Args:
      loglevel (int): minimum loglevel for emitting messages
    """
    logformat = "[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
    logging.basicConfig(
        level=loglevel, stream=sys.stdout, format=logformat, datefmt="%Y-%m-%d %H:%M:%S"
    )


def main(args):
    """Wrapper allowing :func:`fib` to be called with string arguments in a CLI fashion

    Instead of returning the value from :func:`fib`, it prints the result to the
    ``stdout`` in a nicely formated message.

    Args:
      args (List[str]): command line parameters as list of strings
          (for example  ``["--verbose", "42"]``).
    """
    args = parse_args(args)
    setup_logging(args.loglevel)

    runner = LogManager()

    runner.read_config(args.configfile)
    compliant = runner.execute(update=args.update,
                               show_all=args.show_all,
                               show_cost=args.show_cost,
                               show_individual_cost=args.show_individual_cost)

    if not args.update and not compliant:
        exit(1)


def run():
    """Calls :func:`main` passing the CLI arguments extracted from :obj:`sys.argv`

    This function can be used as entry point to create console scripts with setuptools.
    """
    main(sys.argv[1:])


if __name__ == "__main__":
    # ^  This is a guard statement that will prevent the following code from
    #    being executed in the case someone imports this file instead of
    #    executing it as a script.
    #    https://docs.python.org/3/library/__main__.html

    # After installing your project with pip, users can also run your Python
    # modules as scripts via the ``-m`` flag, as defined in PEP 338::
    #
    #     python -m log_retention_compliance.skeleton 42
    #
    run()
