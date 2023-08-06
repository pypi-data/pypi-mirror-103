"""Helper functions for rundeckpy"""

import os
import sys
import logging
import collections


logger = logging.getLogger(__name__)

# pylint: disable=no-member
# Pylint does not understand dynamicly created classes


def set_logging_level():
    """Sets logging level as defined by plugin configuration 'RD_CONFIG_LOG_LEVEL'
    If configuration is not provided it defaults to job execution 'RD_JOB_LOGLEVEL'.
    """
    config = get_config()
    job = get_job()
    log_level = "ERROR"
    if "logging_level" in config._fields:
        log_level = config.logging_level
    if job.loglevel == "DEBUG":
        log_level = "DEBUG"
    logging.basicConfig(level=log_level)
    logger.info("Log level set to %s", log_level)
    return log_level


def get_env(prefix):
    """Returns a named tuple with environment variables that have a given prefix"""
    env_vars = {}
    for var, value in os.environ.items():
        if var.startswith(prefix):
            var_name = var.replace(prefix, "").lower()
            env_vars[var_name] = value
    EnvironmentVars = collections.namedtuple("EnvironmentVars", env_vars.keys())
    return EnvironmentVars(**env_vars)


def get_config():
    """Returns a named tuple with environment variables with prefix RD_CONFIG"""
    return get_env("RD_CONFIG_")


def get_node():
    """Returns a named tuple with environment variables with prefix RD_NODE"""
    return get_env("RD_NODE_")


def get_job():
    """Returns a named tuple with environment variables with prefix RD_JOB"""
    return get_env("RD_JOB_")


def get_options():
    """Returns a named tuple with environment variables with prefix OPTION"""
    return get_env("RD_OPTION_")


def get_conditions():
    """Returns a named tuple with environment variables with prefix OPTION_CONDITIONAL"""
    return get_env("RD_CONFIG_CONDITIONS_")


def evaluate(expression: str, operator: str) -> bool:
    """
    Returns the result of a given expression.

            Parameters:
                expression (str) : one expression per line.
                                   Supported in line operators '==' '!=' '@all@' '@any@'
                operator (str): operator used between lines.
                                Supported operators 'AND' 'OR'

            Returns:
                result (bool)
    """
    should_go_on = []
    for line in expression.splitlines():
        if "==" in line:
            sides = line.split("==", 1)
            result = bool(sides[0].strip().lower() == sides[1].strip().lower())
            should_go_on.append(result)
            logger.debug("Line: %s Result: %s", line, result)
        elif "!=" in line:
            sides = line.split("!=", 1)
            result = bool(sides[0].strip().lower() != sides[1].strip().lower())
            should_go_on.append(result)
            logger.debug("Line: %s Result: %s", line, result)
        elif "@all@" in line:
            sides = line.split("@all@", 1)
            left = [x.strip().lower() for x in sides[0].split(",")]
            right = [x.strip().lower() for x in sides[1].split(",")]
            result = all(item in right for item in left)
            should_go_on.append(result)
            logger.debug("Line: %s Result: %s", line, result)
        elif "@any@" in line:
            sides = line.split("@any@", 1)
            left = [x.strip().lower() for x in sides[0].split(",")]
            right = [x.strip().lower() for x in sides[1].split(",")]
            result = any(item in left for item in right)
            should_go_on.append(result)
            logger.debug("Line: %s Result: %s", line, result)
        else:
            raise ValueError(f"Expression {line} does not contain supported operator.")
    if operator == "AND":
        result = all(should_go_on)
        logger.debug("AND in list %s results %s", should_go_on, result)
        return result
    if operator == "OR":
        result = any(should_go_on)
        logger.debug("OR in list %s results %s", should_go_on, result)
        return result
    raise ValueError(f"Unsuported operator {operator}.")


def check_conditions():
    """Check conditionals set in evironment variables and exits if not satisfied.
    Function requires the following enviroment variables:
    RD_CONFIG_CONDITIONS_RUN_WHEN
    RD_CONFIG_CONDITIONS_OPERATOR
    RD_CONFIG_CONDITIONS_EXPRESSION
    RD_CONFIG_CONDITIONS_GO_ON"""
    logger.debug("Start check conditions.")
    # Load data
    conditions = get_conditions()
    logger.debug("Loaded conditions. %s", conditions)
    # Data validation
    if not str(conditions.run_when) or str(conditions.operator) not in ["AND", "OR"]:
        raise ValueError("One of the required conditions fields was not provided.")
    # Logic
    should_go_on = True
    if conditions.run_when == "Evaluate":
        should_go_on = evaluate(conditions.expression, conditions.operator)
    if conditions.run_when == "Never":
        should_go_on = False
    if should_go_on is False:
        if conditions.not_met_go_on == "true":
            logger.info("Condition failed but not_met_go_on is True. Exiting")
            sys.exit(0)
        else:
            sys.exit("Conditions not met and Node step not_met_go_on is False")
