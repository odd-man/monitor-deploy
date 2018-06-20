# -*- coding: utf-8 -*-\n

import os.path

# import reg_utils # usage reg_utils.reg_nodes,...

from reg_utils import reg_nodes,reg_ip

conf_filename = "nodes-seele"

# cwd = current working directory
old_cwd = os.getcwd()

os.chdir('../../conf/seele')
conf_path = os.getcwd()

blockchain_nodes_path = conf_path + "/"  + conf_filename
existNodesConfig = os.path.isfile(blockchain_nodes_path)

if not existNodesConfig:
    info = 'You lose the file {} in "{}"'.format(conf_filename,conf_path)
    os.chdir(old_cwd)
    exit(info)

# for fabric use
public_dns_names = []
public_usernames = []
public_hosts = []
public_pwds = []
public_host_pwds = {}
public_host_index = {}


with open(blockchain_nodes_path) as f:
    for line in f.readlines():
        line = line.strip()
        if  not len(line) or line.startswith('#'):
            continue

        groups = reg_nodes(line)
        if groups:
            length = len(groups)
            if length < 4:
                exit('error format...')
            username = groups[0]
            host = groups[1]
            if not reg_ip(host):
                continue
            port = groups[2]
            pwd = groups[3]
            indexs = groups[4]

            if len(indexs) != 0:
                set_indexs = set(indexs.split(","))
                if len(set_indexs) != 0:
                    set_indexs.discard("")
                    set_indexs.discard(" ")
                if len(set_indexs) != 0:
                    # index = set_indexs
                    # index = [int(x) for x in sorted(set_indexs)]
                    index = [x for x in sorted(set_indexs)]
            hosts = "{}@{}:{}".format(username, host, port)
            public_dns_names.append(hosts)
            public_usernames.append(username)
            public_hosts.append(host)
            public_pwds.append(pwd)
            public_host_pwds[hosts] = pwd
            public_host_index[hosts] = index
    
    # print("{}".format(public_dns_names))
    # print("{}".format(public_usernames))
    # print("{}".format(public_hosts))
    # print("{}".format(public_pwds))
    # print("{}".format(public_host_index))

    set_public_hosts = set(public_hosts)
    if len(public_hosts) != len(set_public_hosts):
        raise Exception("Exist the repeat host, please check the {} file!".format(conf_filename))

    os.chdir(old_cwd)