#!/usr/bin/env python3

import click
import getpass
import multiprocessing as mp
import os

from polypuppet import Config
from polypuppet.agent.agent import Agent
from polypuppet.agent.setup import setup_server, setup_agent
from polypuppet.server.server import main as server_main
from polypuppet.messages import info, error


@click.group()
def cli():
    pass


@cli.command()
@click.argument('certname')
def autosign(certname):
    agent = Agent()
    has_certname = agent.autosign(certname)
    if not has_certname:
        exit(1)


@cli.command()
@click.argument('username', required=False)
@click.argument('password', required=False)
def login(username, password):
    agent = Agent()
    if username is None:
        username = info.username()
    if password is None:
        password = info.password()
    response = agent.login(username, password)
    if response:
        info.logged_in()
    else:
        error.not_logged_in()


@cli.command()
@click.option('-d', '--daemon', is_flag=True, default=False)
def server(daemon):
    if daemon:
        process = mp.Process(target=server_main)
        process.start()
        os._exit(0)
    else:
        server_main()


@cli.command()
def stop():
    agent = Agent()
    agent.stop_server()


@cli.command()
@click.argument('key', required=False)
@click.argument('value', required=False)
@click.option('-k', '--keys-only', is_flag=True)
def config(key, value, keys_only):
    config = Config()
    if keys_only:
        for k in config.all():
            print(k)
    elif key is None:
        for k, v in config.all().items():
            print(k + '=' + v)
    elif key not in config:
        error.no_config_key(key)
    elif value is None:
        print(config[key])
    else:
        config[key] = value


@cli.command()
@click.argument('what', type=click.Choice(['agent', 'server']), required=True)
def setup(what):
    if what == 'server':
        setup_server()
    elif what == 'agent':
        setup_agent()


if __name__ == "__main__":
    cli()
