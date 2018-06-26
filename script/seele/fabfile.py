# -*- coding: utf-8 -*-

"""A Fabric fabfile with functionality to prepare, install, and configure
UnichainDB, including its storage backend (RethinkDB).
"""


from __future__ import with_statement, unicode_literals
import os
from os import environ  # a mapping (like a dict)
import sys

import time
import datetime
import json

from fabric.colors import red, green, blue, yellow, magenta, cyan
from fabric.api import sudo, cd, env, hosts, local, runs_once
from fabric.api import task, parallel
from fabric.contrib.files import sed
from fabric.operations import run, put, get, prompt
from fabric.context_managers import settings, hide

from configparser import ConfigParser

from hostlist_seele import public_dns_names,public_hosts,public_pwds,public_host_pwds, public_usernames, public_host_index

################################ Fabric Initial Config Data  ######################################

env['passwords'] = public_host_pwds
env['hosts']=env['passwords'].keys()
############################### decorator for function tips ##############################
import functools


def function_tips(start="green", end="green"):
    def wrapper(func):
        @functools.wraps(func)
        def function(*args, **kw):
            start_content = "[{}] run {} ...".format(env.host_string, func.__name__)
            end_content = "[{}] run {} finished".format(env.host_string, func.__name__)


            if start == "red":
                print(red(start_content))
            elif start == "green":
                print(green(start_content))
            elif start == "blue":
                print(blue(start_content))
            elif start == "yellow":
                print(yellow(start_content))
            elif start == "magenta":
                print(magenta(start_content))
            elif start == "cyan":
                print(cyan(start_content))
            else:
                print(start_content)

            cost_start = time.clock()

            outcome = func(*args, **kw)

            cost_time = time.clock() - cost_start

            if end == "red":
                print(red(end_content))
            elif end == "green":
                print(green(end_content))
            elif end == "blue":
                print(blue(end_content))
            elif end == "yellow":
                print(yellow(end_content))
            elif end == "magenta":
                print(magenta(end_content))
            elif end == "cyan":
                print(cyan(end_content))
            else:
                print(end_content)

            print(magenta("[{}] run {} cost time {:.6f}s.".format(env.host_string, func.__name__, cost_time)))

            return outcome

        return function

    return wrapper

# ----------------------------- init node start ---------------------------------
@task
@parallel
@function_tips()
def clear_all():
    with settings(warn_only=True):
        path = "go-seele"
        data_path = ".seele"
        sudo("rm -rf ~/{}".format(path))
        sudo("rm -rf ~/{}".format(data_path))

@task
@parallel
@function_tips()
def clear_data(clear_log=False):
    with settings(warn_only=True):
        data_path = ".seele"
        sudo("rm -rf ~/{}".format(data_path))
        print(green("not exist dir {} and create it!".format(clear_log)))
        if clear_log is True:
            print(green("not exist dir {} and create it!".format(clear_log)))
            clear_log()

@task
@parallel
@function_tips()
def clear_log(log_path=None):
    with settings(warn_only=True):
        if not log_path:
            log_path = "/tmp/seeleTemp/log"
        sudo("rm -rf {}".format(log_path))       

@task
@parallel
@function_tips()
def init_nodes(index=None, start=None):
    with settings(warn_only=True):
        path = "go-seele"
        if sudo("test -d {}".format(path)).failed:
            print(green("not exist dir {} and create it!".format(path)))
            run("mkdir -p ~/{}".format(path))
        else:
            print(red("exist {} and init it!").format(path))
            sudo("rm -rf ~/{}".format(path))
            run("mkdir -p ~/{}".format(path))
            return


@task
@parallel
@function_tips()
def install_from_binary(start=None,size=None):
    path = "go-seele"
    binary_name = 'node'
    # with settings(hide('running', 'stdout'), warn_only=True):
    with settings(warn_only=True):
        if not start:
            index = public_host_index[env.host_string]
        else:
            if start == '0':
                start = 1
            if not size or size == '0':
                size = 1
            start = int(start)
            end = start + int(size)
            index = []
            for i in range(start, end):
                index.append(i)
        # put should not used with cd
        run("cd ~/")
        run('mkdir -p {}'.format(path))
        put('bin/node','{}/{}'.format(path, binary_name))
        run('chmod +x {}/{}'.format(path, binary_name))
        for index,val in enumerate(public_host_index[env.host_string]):
            run("mkdir -p {}/{}".format(path, path+val))
            run('cp {}/{} {}/{}/{}'.format(path, binary_name, path, path+val, "node{}".format(val)))

@task
@function_tips()
def send_binary_file(file=None,start=None,size=None):
    path = "go-seele"
    # with settings(hide('running', 'stdout'), warn_only=True):
    with settings(warn_only=True):
        if not start:
            index = public_host_index[env.host_string]
        else:
            if start == '0':
                start = 1
            if not size or size == '0':
                size = 1
            start = int(start)
            end = start + int(size)
            index = []
            for i in range(start, end):
                index.append(i)
        if local("test -f bin/{}".format(file)).failed:
            print(red("file {} not exist in {}".format(file, "bin/")))
            return
            
        # put should not used with cd
        run("cd ~/")
        run('mkdir -p {}'.format(path))
        put('bin/{}'.format(file),'{}/{}'.format(path, file))
        run('chmod +x {}/{}'.format(path, file))
        for index,val in enumerate(public_host_index[env.host_string]):
            run("mkdir -p {}/{}".format(path, path+val))
            run('cp {}/{} {}/{}/{}'.format(path, file, path, path+val, "{}{}".format(file, val)))

@task
@parallel
@function_tips()
def send_config_file(host_index=None, index=None):
    path = "go-seele"
    config_path = "config"
    with settings(hide('running', 'stdout'), warn_only=True):
    # with settings(warn_only=True):
        index = public_host_index[env.host_string]
        run('cd ~/')
        accounts_file="accounts.json"
        if local("test -f ./config/{}".format(accounts_file)).failed:
            print(red("config {} in config lost".format(accounts_file)))
            return

        for index,val in enumerate(public_host_index[env.host_string]):
            run("mkdir -p {}/{}/{}".format(path, path+val, config_path))
            node_file = 'node'+val+'.json'
            if local('test -f config/{}'.format(node_file)).failed:
                print(red("config {} in config lost".format(node_file)))
                return
            put('config/{}'.format(accounts_file), '~/{}/{}/{}/'.format(path, path+val, config_path))
            put('config/{}'.format(node_file), '~/{}/{}/{}'.format(path, path+val, config_path))

@task
@parallel
@function_tips()
def start_node(index=None):
    with settings(warn_only=True):
        origin_index = public_host_index[env.host_string]
        if index is None:
            index_arr = origin_index
        else:
            index_arr = []
            index_arr.append(index)
        
        path = "go-seele"
        binary_name = 'node'
        config_path = "config"
        accounts_file="accounts.json"
        for i, val in enumerate(index_arr):
            with cd('~/{}/{}'.format(path, path+val)):
                if val in origin_index:
                    run('pwd')
                    node_file = 'node'+val+'.json'
                    run('(nohup ./{} start -c {}/{} --accounts {}/{} --miner stop  >/dev/null 2>&1 &) && sleep 2'.format(binary_name+val, config_path, node_file, config_path, accounts_file), pty=False)
           

@task
@parallel
@function_tips()
def stop_node(index=None):
    with settings(warn_only=True):
        origin_index = public_host_index[env.host_string]
        if index is None:
            index_arr = origin_index
        else:
            index_arr = []
            index_arr.append(index)
        
        path = "go-seele"
        binary_name = 'node'
        config_path = "config"
        for i, val in enumerate(index_arr):
            with cd('~/{}/{}'.format(path, path+val)):
                if val in origin_index:
                    run('pwd')
                    sudo("ps -ef|grep node{}|awk {{'print $2'}}|xargs kill -9".format(val))

@task
@parallel
@function_tips()
def restart_node(index=None):
    with settings(warn_only=True):
        stop_node()
        start_node()

@task
@parallel
@function_tips()
def seek_run_nodes(name=None):
    binary_name = 'node'
    if not name:
       name = binary_name
    run("ps -ef|grep {}".format(binary_name))
   
               

# ----------------------------- init node end -----------------------------------

# ------------------------------ file and dir seek  start ------------------------------
@task
# @parallel
@function_tips()
def seek_file_content(path=None, grep=None):
    print(path)
    with settings(warn_only=True):
        print(path)
        if not path or sudo("test -f {}".format(path)).failed:
            print(red("error input path !"))
            return

        if not grep:
            sudo("cat {}".format(path))
        else:
            sudo("grep '{}' {} 2>/dev/null".format(grep, path))


@task
@parallel
@function_tips()
def seek_file_list(path=None, order="desc"):
    with settings(warn_only=True):
        if not path or sudo("test -d {}".format(path)).failed:
            print(red("path error!"))
            return
        if order == "asc":
            sudo("ls -lht {}".format(path))
        else:
            sudo("ls -lhtr {}".format(path))

# ------------------------------ file and dir seek  end ------------------------------

################################ First Install Start######################################

#set on node
@task
@function_tips()
def set_node(host, password):
    env['passwords'][host]=password
    env['hosts']=env['passwords'].keys()
    print(env)


@task
@function_tips()
def set_host(host_index):
    """A helper task to change env.hosts from the
    command line. It will only "stick" for the duration
    of the fab command that called it.

    Args:
        host_index (int): 0, 1, 2, 3, etc.
    Example:
        fab set_host:4 fab_task_A fab_task_B
        will set env.hosts = [public_dns_names[4]]
        but only for doing fab_task_A and fab_task_B
    """
    env.hosts = [public_dns_names[int(host_index)]]
    env.password = [public_pwds[int(host_index)]]



# ------------------------------------------- other deals -----------------------------------
# count the special process count
@task
@parallel
@function_tips()
def count_process_with_name(name):
    with settings(hide('running', 'stdout'), warn_only=True):
        print(blue("{} count process with name {} start ...".format(env.host_string, name)))
        user = env.user
        cmd = "echo '{}`s process name {}, count is ' `ps -e |grep -w {} | wc -l`".format(user,name,name)
        result = sudo("{}".format(cmd) )
        print(green("{}".format(result)))


@task
@parallel
def kill_process_with_name(name):
    with settings(hide('running', 'stdout'), warn_only=True):
        print(blue("{} kill process with name {} start ...".format(env.host_string, name)))
        sudo("killall -9 {} 2>/dev/null".format(name))
        print(green("{} kill process with name {} over".format(env.host_string, name)))


@task
@parallel
@function_tips()
def kill_process_with_port(port):
    with settings(hide('running', 'stdout'), warn_only=True):
        print(blue("{} kill process with port {} start ...".format(env.host_string, port)))
        try:
            sudo("kill -9 `netstat -nlp | grep :{} | awk '{{print $7}}' | awk '!a[$0]++' | \
awk -F'/' '{{ print $1 }}'` 2>/dev/null".format(port))
        except:
            raise
        print(green("{} kill process with port {} over".format(env.host_string, port)))

