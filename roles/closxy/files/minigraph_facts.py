#!/usr/bin/python
import sys
import yaml
import ipaddress


def create_ip_list(ipnetwork, startadress, devices):
    # returns a list of consecutive ip address part of same network
    ipobject = ipaddress.ip_network(unicode(ipnetwork))
    iplist = []
    if ipobject.prefixlen == 32 or ipobject.prefixlen == 128:
        ip = ipobject.network_address
        for device in range(devices):
            iplist.append(str(ip) + '/' + str(ipobject.prefixlen))
            ip = ipaddress.ip_address(int(ip) + 1)
        return iplist
    else:
        for ip in ipobject.hosts():
            iplist.append(str(ip) + '/' + str(ipobject.prefixlen))
            if len(iplist) > (startadress+devices):
                break
        return iplist[startadress:(startadress+devices)]


def create_iplist_diffnw(ipnetwork, tors, leafs):
    ipobject = ipaddress.ip_network(unicode(ipnetwork))
    ipobjlist = []
    iplist0 = []
    iplist1 = []
    for i in range(tors):
        devicesubnet = str(ipaddress.ip_address(int(ipobject.network_address) +
                            ipobject.num_addresses*i)) + '/' + str(ipobject.prefixlen)
        ipobjlist.append(ipaddress.ip_network(unicode(unicode(devicesubnet))))
    for ipobj in ipobjlist:
        b2biplist0 = []
        b2biplist1 = []
        if ipobj.version == 4:
            for idx, b2bip in enumerate(ipobj):
                if idx % 2 == 0:
                    ip = str(b2bip) + str('/31')
                    b2biplist0.append(ip)
                else:
                    ip = str(b2bip) + str('/31')
                    b2biplist1.append(ip)
                if len(b2biplist1) >= leafs:
                    break
        elif ipobj.version == 6:
            for idx, subnet in enumerate(ipobj.subnets(new_prefix=126), 1):
                hostlist = list(subnet.hosts())
                ipv6_0 = str(hostlist[0]) + str('/126')
                ipv6_1 = str(hostlist[1]) + str('/126')
                b2biplist0.append(ipv6_0)
                b2biplist1.append(ipv6_1)
                if idx >= leafs:
                    break
        iplist0.append(b2biplist0)
        iplist1.append(b2biplist1)
    return iplist0, iplist1


def modify_list(iplist, tors, leafs):
    # this function modifies the T0 b2b IP list to in a manner to configure
    # T1 devices. E.G. T0[[11,12][21,22]] will change to T1[[11,21][12,22]]
    modified_list = []
    for i in range(leafs):
        nestedlist = []
        for j in range(tors):
            nestedlist.append(iplist[j][i])
        modified_list.append(nestedlist)
    return modified_list

Tors = int(sys.argv[1])
Leafs = int(sys.argv[2])
Spines = int(sys.argv[3])
t0 = []
t1 = []
t2 = []
with open("roles/closxy/vars/main.yml", 'r') as ymlfile:
        vars = yaml.load(ymlfile)

mgmtnw = create_ip_list(vars['Tier0']['mgmtnetwork'], vars['Tier0']['mgmtstartaddr'], Tors)
mgmtnw6 = create_ip_list(vars['Tier0']['mgmtnetwork6'], int(vars['Tier0']['mgmtstartaddr6'], 16), Tors)
loopback = create_ip_list(vars['Tier0']['loopback'], vars['Tier0']['loopbackstartaddr'], Tors)
loopback6 = create_ip_list(vars['Tier0']['loopback6'], vars['Tier0']['loopbackstartaddr6'], Tors)
downlink = ipaddress.ip_network(unicode(vars['Tier0']['downaddr']))
iplist0, iplist1 = create_iplist_diffnw(vars['Tier0']['upaddr'], Tors, Leafs)
ipv6list0, ipv6list1 = create_iplist_diffnw(vars['Tier0']['upaddr6'], Tors, Leafs)
modified_iplist1 = modify_list(iplist1, Tors, Leafs)
modified_ipv6list1 = modify_list(ipv6list1, Tors, Leafs)
for Tor in range(Tors):
    t0.append({
        'hostname': 'T0-'+str(Tor + 1),
        'tierindex': Tor,
        'devtype': 'ToRRouter',
        'devtypeup': 'LeafRouter',
        'mgmtaddr': mgmtnw[Tor],
        'mgmtaddr6': mgmtnw6[Tor],
        'loopback': loopback[Tor],
        'loopback6': loopback6[Tor],
        'downaddr': str(downlink[Tor+1]) + '/' + str(downlink.prefixlen),
        'upaddr': iplist0[Tor],
        'upaddr6': ipv6list0[Tor]
        })


mgmtnw = create_ip_list(vars['Tier1']['mgmtnetwork'], vars['Tier1']['mgmtstartaddr'], Leafs)
mgmtnw6 = create_ip_list(vars['Tier1']['mgmtnetwork6'], int(vars['Tier1']['mgmtstartaddr6'], 16), Leafs)
loopback = create_ip_list(vars['Tier1']['loopback'], vars['Tier1']['loopbackstartaddr'], Leafs)
loopback6 = create_ip_list(vars['Tier1']['loopback6'], vars['Tier1']['loopbackstartaddr6'], Leafs)
iplist0, iplist1 = create_iplist_diffnw(vars['Tier1']['upaddr'], Leafs, Spines)
ipv6list0, ipv6list1 = create_iplist_diffnw(vars['Tier1']['upaddr6'], Leafs, Spines)
for Leaf in range(Leafs):
    t1.append({
        'hostname': 'T1-'+str(Leaf + 1),
        'tierindex': Leaf,
        'devtype': 'LeafRouter',
        'devtypedown': 'TorRouter',
        'devtypeup': 'SpineRouter',
        'mgmtaddr': mgmtnw[Leaf],
        'mgmtaddr6': mgmtnw6[Leaf],
        'loopback': loopback[Leaf],
        'loopback6': loopback6[Leaf],
        'downaddr': modified_iplist1[Leaf],
        'downaddr6': modified_ipv6list1[Leaf],
        'upaddr': iplist0[Leaf],
        'upaddr6': ipv6list0[Leaf]
        })


mgmtnw = create_ip_list(vars['Tier2']['mgmtnetwork'], vars['Tier2']['mgmtstartaddr'], Spines)
modified_iplist1 = modify_list(iplist1, Leafs, Spines)
modified_ipv6list1 = modify_list(ipv6list1, Leafs, Spines)
for Spine in range(Spines):
    t2.append({
        'hostname': 'T2-'+str(Spine + 1),
        'tierindex': Spine,
        'devtype': 'SpineRouter',
        'devtypedown': 'LeafRouter',
        'mgmtaddr': mgmtnw[Spine],
        'downaddr': modified_iplist1[Spine],
        'downaddr6': modified_ipv6list1[Spine]
        })

pod_vars = {'t0': t0, 't1': t1, 't2': t2}
with open("roles/closxy/vars/podset.yml",'w') as yaml_file:
    yaml.dump(pod_vars,yaml_file, default_flow_style=False)


