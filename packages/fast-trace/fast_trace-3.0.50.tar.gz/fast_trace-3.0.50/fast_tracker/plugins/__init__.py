#!/usr/local/bin python3
# -*- coding: utf-8 -*-

"""
    created by FAST-DEV 2021/4/6
"""
import inspect
import logging
from fast_tracker.loggings import logger
import pkgutil
import re
import traceback

import pkg_resources

from packaging import version

from fast_tracker import config

import fast_tracker


def install():
    disable_patterns = config.disable_plugins
    if isinstance(disable_patterns, str):
        disable_patterns = [re.compile(p.strip()) for p in disable_patterns.split(',') if p.strip()]
    else:
        disable_patterns = [re.compile(p.strip()) for p in disable_patterns if p.strip()]
    # for循环将plugins文件夹下面的所有实现的plugin都install进来
    for importer, modname, ispkg in pkgutil.iter_modules(fast_tracker.plugins.__path__):
        if any(pattern.match(modname) for pattern in disable_patterns):
            logger.info('plugin %s is disabled and thus won\'t be installed', modname)
            continue
        logger.debug('installing plugin %s', modname)
        plugin = importer.find_module(modname).load_module(modname)

        supported = pkg_version_check(plugin)
        if not supported:
            logger.debug('check version for plugin %s\'s corresponding package failed, thus '
                         'won\'t be installed', modname)
            continue

        if not hasattr(plugin, 'install') or inspect.ismethod(getattr(plugin, 'install')):
            logger.warning('no `install` method in plugin %s, thus the plugin won\'t be installed', modname)
            continue

        # noinspection PyBroadException
        try:
            plugin.install()
        except Exception:
            logger.warning('failed to install plugin %s', modname)
            traceback.print_exc() if logger.isEnabledFor(logging.DEBUG) else None


_operators = {
    '<': lambda cv, ev: cv < ev,
    '<=': lambda cv, ev: cv < ev or cv == ev,
    '==': lambda cv, ev: cv == ev,
    '>=': lambda cv, ev: cv > ev or cv == ev,
    '>': lambda cv, ev: cv > ev,
    '!=': lambda cv, ev: cv != ev
}


class VersionRuleException(Exception):
    def __init__(self, message):
        self.message = message


def pkg_version_check(plugin):
    supported = True

    # no version rules was set, no checks
    if not hasattr(plugin, "version_rule"):
        return supported

    pkg_name = plugin.version_rule.get("name")
    rules = plugin.version_rule.get("rules")

    try:
        current_pkg_version = pkg_resources.get_distribution(pkg_name).version
    except pkg_resources.DistributionNotFound:
        # when failed to get the version, we consider it as supported.
        return supported

    current_version = version.parse(current_pkg_version)
    # pass one rule in rules (OR)
    for rule in rules:
        if rule.find(" ") == -1:
            if check(rule, current_version):
                return supported
        else:
            # have to pass all rule_uint in this rule (AND)
            rule_units = rule.split(" ")
            results = [check(unit, current_version) for unit in rule_units]
            if False in results:
                # check failed, try to check next rule
                continue
            else:
                return supported

    supported = False
    return supported


def check(rule_unit, current_version):
    idx = 2 if rule_unit[1] == '=' else 1
    symbol = rule_unit[0:idx]
    expect_pkg_version = rule_unit[idx:]

    expect_version = version.parse(expect_pkg_version)
    f = _operators.get(symbol) or None
    if not f:
        raise VersionRuleException("version rule {} error. only allow >,>=,==,<=,<,!= symbols".format(rule_unit))

    return f(current_version, expect_version)
