# ios.cmds
#
# Copyright (C) Robert Franklin <rcf34@cam.ac.uk>



"""Cisco IOS configuration commands module.

This module parses Cisco IOS configuration files into a dictionary.
"""



# --- imports ---



from deepops import deepsetdefault, deepget
from netaddr import IPNetwork

from net_contextdiff.config import IndentedContextualCommand

from .utils import (
    interface_canonicalize,
    ip_acl_ext_rule_canonicalize,
    ipv6_acl_rule_canonicalize,
    expand_set )



# cmds = []
#
# This is a list of classes, one for each IOS configuration mode
# command.  The command classes are defined at the global level and
# added to this list.
#
# The CiscoIOSConfig class adds these to the object upon instantiation,
# by the _add_commands() method.
#
# This was done to make it clearer how the commands are implemented.

cmds = []



# --- configuration command classes ---



# _Cmd is created to be a shorthand for the IndentedContextualCommand
# class as we'll be using it a lot

_Cmd = IndentedContextualCommand



# SYSTEM



class _Cmd_Comment(_Cmd):
    cmd = r"!.*"

cmds.append(_Cmd_Comment)


class _Cmd_Hostname(_Cmd):
    cmd = r"hostname (?P<hostname>\S+)"

    def store(self, cfg, hostname):
        cfg["hostname"] = hostname

cmds.append(_Cmd_Hostname)



# INTERFACE ...



class _Cmd_Int(_Cmd):
    cmd = r"interface (?P<int_name>\S+)"
    enter_context = "interface"

    def store(self, cfg, int_name):
        int_name = interface_canonicalize(int_name)

        i = deepsetdefault(cfg, "interface", int_name)

        # IOS has an odd behaviour that, when an interface is created in
        # configure mode, it will default to shutdown or not, depending
        # on its type; in startup configurations, however, they are
        # always not shutdown
        #
        # we default to not shutdown, unless this has been explicitly
        # overridden: this has the effect of 'no shutdown'ing the
        # interface, if it is being created
        i.setdefault("shutdown", False)

        return i

cmds.append(_Cmd_Int)


class _CmdContext_Int(_Cmd):
    context = "interface"


class _Cmd_Int_CDPEna(_CmdContext_Int):
    cmd = r"(?P<no>no )?cdp enable"

    def store(self, cfg, no):
        # we allow CDP to be 'no cdp enable' to clear the CDP status
        cfg["cdp-enable"] = not no

cmds.append(_Cmd_Int_CDPEna)


class _Cmd_Int_ChnGrp(_CmdContext_Int):
    cmd = r"channel-group (?P<ch_grp>\d+)(?P<mode> .+)?"

    def store(self, cfg, ch_grp, mode):
        cfg["channel-group"] = int(ch_grp), mode

cmds.append(_Cmd_Int_ChnGrp)


class _Cmd_Int_Desc(_CmdContext_Int):
    cmd = r"description (?P<desc>.+)"

    def store(self, cfg, desc):
        cfg["description"] = desc

cmds.append(_Cmd_Int_Desc)


class _Cmd_Int_Encap(_CmdContext_Int):
    cmd = r"encapsulation (?P<encap>dot1q \d+( native)?)"

    def store(self, cfg, encap):
        # lower case the encapsulation definition as IOS stores 'dot1q'
        # as 'dot1Q'
        cfg["encapsulation"] = encap.lower()

cmds.append(_Cmd_Int_Encap)


class _Cmd_Int_IPAccGrp(_CmdContext_Int):
    cmd = r"ip access-group (?P<acl_name>\S+) (?P<dir_>in|out)"

    def store(self, cfg, acl_name, dir_):
        cfg.setdefault("ip-access-group", {})[dir_] = acl_name

cmds.append(_Cmd_Int_IPAccGrp)


class _Cmd_Int_IPAddr(_CmdContext_Int):
    cmd = r"ip address (?P<addr>\S+ \S+)"

    def store(self, cfg, addr):
        cfg["ip-address"] = addr

cmds.append(_Cmd_Int_IPAddr)


class _Cmd_Int_IPAddrSec(_CmdContext_Int):
    cmd = r"ip address (?P<addr>\S+ \S+) secondary"

    def store(self, cfg, addr):
        # secondary address - record it in a list
        cfg.setdefault("ip-address-secondary", set()).add(addr)

cmds.append(_Cmd_Int_IPAddrSec)


class _Cmd_Int_IP6Addr(_CmdContext_Int):
    cmd = r"ipv6 address (?P<addr>\S+)"

    def store(self, cfg, addr):
        # IPv6 addresses involve letters so we lower case for
        # consistency
        cfg.setdefault("ipv6-address", set()).add(addr.lower())

cmds.append(_Cmd_Int_IP6Addr)


class _Cmd_Int_IPFlowMon(_CmdContext_Int):
    cmd = r"ip flow monitor (?P<flowmon>\S+) (?P<dir_>input|output)"

    def store(self, cfg, flowmon, dir_):
        deepsetdefault(cfg, "ip-flow-monitor")[dir_] = flowmon

cmds.append(_Cmd_Int_IPFlowMon)


class _Cmd_Int_IPHlprAddr(_CmdContext_Int):
    cmd = r"ip helper-address (?P<addr>(global )?\S+)"

    def store(self, cfg, addr):
        cfg.setdefault("ip-helper-address", set()).add(addr)

cmds.append(_Cmd_Int_IPHlprAddr)


class _Cmd_Int_IPIGMPVer(_CmdContext_Int):
    cmd = r"ip igmp version (?P<ver>\S+)"

    def store(self, cfg, ver):
        cfg["ip-igmp-version"] = ver

cmds.append(_Cmd_Int_IPIGMPVer)


class _Cmd_Int_IPMcastBdry(_CmdContext_Int):
    cmd = r"ip multicast boundary (?P<acl>\S+)"

    def store(self, cfg, acl):
        cfg["ip-multicast-boundary"] = acl

cmds.append(_Cmd_Int_IPMcastBdry)


class _Cmd_Int_IPPIMMode(_CmdContext_Int):
    cmd = r"ip pim (?P<mode>(sparse|dense|sparse-dense)-mode)"

    def store(self, cfg, mode):
        cfg.setdefault("ip-pim", {})["mode"] = mode

cmds.append(_Cmd_Int_IPPIMMode)


class _Cmd_Int_IPPIMBSRBdr(_CmdContext_Int):
    cmd = r"ip pim bsr-border"

    def store(self, cfg):
        cfg.setdefault("ip-pim", {})["bsr-border"] = True

cmds.append(_Cmd_Int_IPPIMBSRBdr)


class _Cmd_Int_IPProxyARP(_CmdContext_Int):
    cmd = r"(?P<no>no )?ip proxy-arp"

    def store(self, cfg, no):
        cfg["ip-proxy-arp"] = not no

cmds.append(_Cmd_Int_IPProxyARP)


class _Cmd_Int_IPVerifyUni(_CmdContext_Int):
    cmd = r"ip verify unicast (?P<opt>.+)"

    def store(self, cfg, opt):
        cfg["ip-verify-unicast"] = opt

cmds.append(_Cmd_Int_IPVerifyUni)


class _Cmd_Int_ServPol(_CmdContext_Int):
    cmd = r"service-policy (?P<policy>.+)"

    def store(self, cfg, policy):
        cfg.setdefault("service-policy", set()).add(policy)

cmds.append(_Cmd_Int_ServPol)


class _Cmd_Int_Shutdown(_CmdContext_Int):
    cmd = r"(?P<no>no )?shutdown"

    def store(self, cfg, no):
        cfg["shutdown"] = not no

cmds.append(_Cmd_Int_Shutdown)


class _Cmd_Int_StandbyIP(_CmdContext_Int):
    cmd = r"standby (?P<grp>\d+) ip (?P<addr>\S+)"

    def store(self, cfg, grp, addr):
        deepsetdefault(
            cfg, "standby", "group", int(grp))["ip"] = addr

cmds.append(_Cmd_Int_StandbyIP)


class _Cmd_Int_StandbyIPSec(_CmdContext_Int):
    cmd = r"standby (?P<grp>\d+) ip (?P<addr>\S+) secondary"

    def store(self, cfg, grp, addr):
        deepsetdefault(
            cfg, "standby", "group", int(grp), "ip-sec", last=set()).add(addr)

cmds.append(_Cmd_Int_StandbyIPSec)


class _Cmd_Int_StandbyIP6(_CmdContext_Int):
    cmd = r"standby (?P<grp>\d+) ipv6 (?P<addr>\S+)"

    def store(self, cfg, grp, addr):
        deepsetdefault(
            cfg, "standby", "group", int(grp), "ipv6", last=set()).add(addr)

cmds.append(_Cmd_Int_StandbyIP6)


class _Cmd_Int_StandbyPreempt(_CmdContext_Int):
    cmd = r"standby (?P<grp>\d+) preempt"

    def store(self, cfg, grp):
        deepsetdefault(
            cfg, "standby", "group", int(grp))["preempt"] = True

cmds.append(_Cmd_Int_StandbyPreempt)


class _Cmd_Int_StandbyPri(_CmdContext_Int):
    cmd = r"standby (?P<grp>\d+) priority (?P<pri>\d+)"

    def store(self, cfg, grp, pri):
        deepsetdefault(
            cfg, "standby", "group", int(grp))["priority"] = int(pri)

cmds.append(_Cmd_Int_StandbyPri)


class _Cmd_Int_StandbyTimers(_CmdContext_Int):
    cmd = r"standby (?P<grp>\d+) timers (?P<timers>\d+ \d+)"

    def store(self, cfg, grp, timers):
        deepsetdefault(
            cfg, "standby", "group", int(grp))["timers"] = timers

cmds.append(_Cmd_Int_StandbyTimers)


class _Cmd_Int_StandbyTrk(_CmdContext_Int):
    cmd = r"standby (?P<grp>\d+) track (?P<obj>\d+)( (?P<extra>.+))?"

    def store(self, cfg, grp, obj, extra):
        deepsetdefault(
            cfg, "standby", "group", int(grp), "track")[obj] = extra

cmds.append(_Cmd_Int_StandbyTrk)


class _Cmd_Int_StandbyVer(_CmdContext_Int):
    cmd = r"standby version (?P<ver>\d)"

    def store(self, cfg, ver):
        deepsetdefault(cfg, "standby")["version"] = int(ver)

cmds.append(_Cmd_Int_StandbyVer)


class _Cmd_Int_SwPortTrkNtv(_CmdContext_Int):
    cmd = r"switchport trunk native vlan (?P<vlan>\d+)"

    def store(self, cfg, vlan):
        cfg["swport-trunk-native"] = int(vlan)

cmds.append(_Cmd_Int_SwPortTrkNtv)


class _Cmd_Int_SwPortTrkAlw(_CmdContext_Int):
    cmd = r"switchport trunk allowed vlan (add )?(?P<vlans>[0-9,-]+)"

    def store(self, cfg, vlans):
        cfg.setdefault("switchport-trunk-allow", set()).update(
            expand_set(vlans))

cmds.append(_Cmd_Int_SwPortTrkAlw)


class _Cmd_Int_VRF(_CmdContext_Int):
    cmd = (r"vrf forwarding (?P<name>\S+)")

    def store(self, cfg, name):
        cfg["vrf-forwarding"] = name

cmds.append(_Cmd_Int_VRF)


class _Cmd_Int_XConn(_CmdContext_Int):
    cmd = r"xconnect (?P<remote>[0-9.]+ \d+ .+)"

    def store(self, cfg, remote):
        cfg["xconnect"] = remote

cmds.append(_Cmd_Int_XConn)



# IP ACCESS-LIST STANDARD



class _Cmd_ACLStdRule(_Cmd):
    cmd = r"access-list (?P<num>\d{1,2}|1[3-9]\d{2}) (?P<rule>.+)"

    def store(self, cfg, num, rule):
        deepsetdefault(
            cfg, "ip-access-list-standard", num, last=[]).append(rule)

cmds.append(_Cmd_ACLStdRule)


class _Cmd_IPACL_Std(_Cmd):
    cmd = r"ip access-list standard (?P<acl_name>.+)"
    enter_context = "ip-acl_std"

    def store(self, cfg, acl_name):
        return deepsetdefault(
                   cfg, "ip-access-list-standard", acl_name, last=[])

cmds.append(_Cmd_IPACL_Std)


class _Cmd_IPACL_Std_Rule(_Cmd):
    context = "ip-acl_std"
    cmd = r"(?P<rule>(permit|deny) +.+)"

    def store(self, cfg, rule):
        cfg.append(rule)

cmds.append(_Cmd_IPACL_Std_Rule)


class _Cmd_ACLExtRule(_Cmd):
    cmd = r"access-list (?P<num>1\d{2}|2[0-6]\d{2}) (?P<rule>.+)"

    def store(self, cfg, num, rule):
        deepsetdefault(
            cfg, "ip-access-list-extended", num, last=[]
            ).append(ip_acl_ext_rule_canonicalize(rule))

cmds.append(_Cmd_ACLExtRule)


class _Cmd_IPACL_Ext(_Cmd):
    cmd = r"ip access-list extended (?P<name>.+)"
    enter_context = "ip-acl_ext"

    def store(self, cfg, name):
        return deepsetdefault(cfg, "ip-access-list-extended", name, last=[])

cmds.append(_Cmd_IPACL_Ext)


class _Cmd_IPACL_Ext_Rule(_Cmd):
    context = "ip-acl_ext"
    cmd = r"(?P<rule>(permit|deny) +.+)"

    def store(self, cfg, rule):
        cfg.append(ip_acl_ext_rule_canonicalize(rule))

cmds.append(_Cmd_IPACL_Ext_Rule)



# IPV6 ACCESS-LIST ...



class _Cmd_IP6ACL(_Cmd):
    cmd = r"ipv6 access-list (?P<name>.+)"
    enter_context = "ipv6-acl"

    def store(self, cfg, name):
        return deepsetdefault(cfg, "ipv6-access-list", name, last=[])

cmds.append(_Cmd_IP6ACL)


class _Cmd_IP6ACL_Rule(_Cmd):
    context = "ipv6-acl"
    cmd = r"(?P<rule>(permit|deny) +.+)"

    def store(self, cfg, rule):
        cfg.append(ipv6_acl_rule_canonicalize(rule))

cmds.append(_Cmd_IP6ACL_Rule)



# IP[V6] PREFIX-LIST ...



class _Cmd_IPPfx(_Cmd):
    cmd = r"ip prefix-list (?P<list_>\S+) (seq \d+ )?(?P<rule>.+)"

    def store(self, cfg, list_, rule):
        deepsetdefault(cfg, "ip-prefix-list", list_, last=[]).append(rule)

cmds.append(_Cmd_IPPfx)


class _Cmd_IP6Pfx(_Cmd):
    cmd = r"ipv6 prefix-list (?P<list_>\S+) (seq \d+ )?(?P<rule>.+)"

    def store(self, cfg, list_, rule):
        deepsetdefault(
            cfg, "ipv6-prefix", list_, last=[]).append(rule.lower())

cmds.append(_Cmd_IP6Pfx)



# IP[V6] ROUTE ...



class _Cmd_IPRoute(_Cmd):
    cmd = r"ip route (?P<route>.+)"

    def store(self, cfg, route):
        cfg.setdefault("ip-route", set()).add(route)

cmds.append(_Cmd_IPRoute)


class _Cmd_IP6Route(_Cmd):
    cmd = r"ipv6 route (?P<route>.+)"

    def store(self, cfg, route):
        # IPv6 addresses involve letters so we lower case for
        # consistency
        cfg.setdefault("ipv6-route", set()).add(route.lower())

cmds.append(_Cmd_IP6Route)



# [NO] SPANNING-TREE ...



class _Cmd_NoSTP(_Cmd):
    cmd = r"no spanning-tree vlan (?P<tags>[-0-9,]+)"

    def store(self, cfg, tags):
        cfg.setdefault(
            "no-spanning-tree-vlan", set()).update(expand_set(tags))

cmds.append(_Cmd_NoSTP)


class _Cmd_STPPriority(_Cmd):
    cmd = r"spanning-tree vlan (?P<tags>[-0-9,]+) priority (?P<pri>\d+)"

    def store(self, cfg, tags, pri):
        cfg_stp_pri = cfg.setdefault("spanning-tree-vlan-priority", {})
        for tag in expand_set(tags):
            cfg_stp_pri[int(tag)] = int(pri)

cmds.append(_Cmd_STPPriority)



# TRACK ...



class _Cmd_TrackRoute(_Cmd):
    cmd = (r"track (?P<obj>\d+)"
           r" (?P<proto>ip|ipv6) route"
           r" (?P<net>[0-9a-fA-F.:]+/\d+|[0-9.]+ [0-9.]+)"
           r" (?P<extra>metric .+|reachability)")
    enter_context = "track"

    def store(self, cfg, obj, proto, net, extra):
        # the 'net' can be in 'network netmask' or CIDR format, but the
        # netaddr.IPNetwork() object requires a slash between the
        # network and netmask, so we just change the space to a slash
        net = IPNetwork(net.replace(" ", "/"))

        # reconstruct a normalised version of the criterion
        criterion = ("%s route %s %s" % (proto, net, extra))

        # create the new track object and store the criterion in it
        t = deepsetdefault(cfg, "track", int(obj))
        t["criterion"] = criterion

        # return the track object for the new context
        return t

cmds.append(_Cmd_TrackRoute)


class _Cmd_TrackOther(_Cmd):
    cmd = r"track (?P<obj>\d+) (?P<other>(interface .+|list .+|stub-object))"
    enter_context = "track"

    def store(self, cfg, obj, other):
        t = deepsetdefault(cfg, "track", int(obj))
        t["criterion"] = other

        return t

cmds.append(_Cmd_TrackOther)


class _Cmd_Track(_Cmd):
    cmd = r"track (?P<obj>\d+)"
    enter_context = "track"

    def store(self, cfg, obj):
        # if there is no criterion, we're modifying an existing object,
        # which must have already been defined, so we deliberately don't
        # create it with deepsetdefault() but just deepget() it with
        # default_error set, to force an error here, if it doesn't exist
        return deepget(cfg, "track", int(obj), default_error=True)

cmds.append(_Cmd_Track)


class _CmdContext_Track(_Cmd):
    context = "track"


class _Cmd_Track_Delay(_CmdContext_Track):
    cmd = r"delay (?P<delay>.+)"

    def store(self, cfg, delay):
        cfg["delay"] = delay

cmds.append(_Cmd_Track_Delay)


class _Cmd_Track_IPVRF(_CmdContext_Track):
    cmd = r"ip vrf (?P<vrf_name>\S+)"

    def store(self, cfg, vrf_name):
        cfg["ip-vrf"] = vrf_name

cmds.append(_Cmd_Track_IPVRF)


class _Cmd_Track_Obj(_CmdContext_Track):
    cmd = r"object (?P<obj>.+)"

    def store(self, cfg, obj):
        deepsetdefault(cfg, "object", last=set()).add(obj)

cmds.append(_Cmd_Track_Obj)



# VLAN ...



class _Cmd_VLAN(_Cmd):
    cmd = r"vlan (?P<tag>\d+)"
    enter_context = "vlan"

    def store(self, cfg, tag):
        # create the VLAN configuration entry, setting an 'exists' key
        # as we might stop other information in here that isn't in the
        # VLAN definition itself in IOS (e.g. STP priority) in future
        v = deepsetdefault(cfg, "vlan", int(tag))
        v["exists"] = True

        return v

cmds.append(_Cmd_VLAN)


class _CmdContext_VLAN(_Cmd):
    context = "vlan"

class _Cmd_VLAN_Name(_CmdContext_VLAN):
    cmd = r"name (?P<name>\S+)"

    def store(self, cfg, name):
        cfg["name"] = name

cmds.append(_Cmd_VLAN_Name)
