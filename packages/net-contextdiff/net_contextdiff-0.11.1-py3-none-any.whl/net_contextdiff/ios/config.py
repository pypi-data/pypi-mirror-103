# ios.config
#
# Copyright (C) Robert Franklin <rcf34@cam.ac.uk>



"""Cisco IOS configuration module.

This module parses Cisco IOS configuration files into a dictionary.
"""



# --- imports ---



import re

from deepops import deepsetdefault, deepget
from netaddr import IPNetwork

from net_contextdiff.config import IndentedContextualConfig

from .cmds import cmds
from .utils import ip_acl_std_canonicalize



# --- classes ----



class CiscoIOSConfig(IndentedContextualConfig):
    "This concrete class parses Cisco IOS configuration files."


    def _add_commands(self):
        """This method is called by the constructor to add commands for
        the IOS platform.

        The commands are stored in a global (to the module) level list
        of classes.
        """

        for cmd_class in cmds:
            self._add_command(cmd_class)


    def _post_parse_file(self):
        """Extend the inherited method to flush any pending IPv4
        standard ACL rules into the configuration.
        """

        super()._post_parse_file()

        # go through the pending IPv4 standard ACLs and store them (we
        # convert this to a list as _acl4_std_flush() will change the
        # dictionary during iteration and we only need the names)
        if "ip-access-list-standard" in self:
            ip_acl_std = self["ip-access-list-standard"]
            for name in ip_acl_std:
                ip_acl_std[name] = ip_acl_std_canonicalize(ip_acl_std[name])
