#! /usr/bin/env python
# encoding: utf-8

import argparse
import os

from subprocess import call
from shutil import rmtree


SSH_TARGET_DIR = "~/www/public_html/alexjf_new_testwin"


def main():
    TASKS = {
        "setup": setup,
        "html": html,
        "regenerate": regenerate,
        "publish": publish,
        "serve": serve,
        "clean": clean,
        "rsync_upload": rsync_upload,
        "winscp_upload": winscp_upload,
    }

    epilog = "Tasks:\n"

    for task_name, task in TASKS.items():
        epilog += "\t{} - {}\n".format(task_name, task.__doc__)

    parser = argparse.ArgumentParser(
            description="AlexJF build system", 
            epilog=epilog, 
            formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("tasks", metavar="task", nargs="+", 
            help="Tasks to execute (in-order)")
    parser.add_argument("-i", "--input", default="content", help="Input directory")
    parser.add_argument("-o", "--output", default="output", help="Output directory")
    parser.add_argument("-c", "--cache", default="cache", help="Cache directory")
    parser.add_argument("-bc", "--baseconf", default="pelicanconf.py", help="Base configuration file")
    parser.add_argument("-pc", "--publishconf", default="publishconf.py", help="Publish configuration file")
    parser.add_argument("-p", "--serve-port", type=int, default=8000, help="Change port where HTML server listens on")
    parser.add_argument("-d", "--debug", action="store_true", help="Activate debug logging")
    parser.add_argument("-e", "--extra", nargs="*", default=[])

    parser.add_argument("-su", "--ssh-user", default=os.getenv("SOVEREIGN_USER", None), help="SSH user of server to publish to")
    parser.add_argument("-sh", "--ssh-host", default=os.getenv("SOVEREIGN_HOST", None), help="SSH host of server to publish to")
    parser.add_argument("-sp", "--ssh-port", type=int, default=os.getenv("SOVEREIGN_PORT", 22), help="SSH port of server to publish to")
    parser.add_argument("-sd", "--ssh-target-dir", default=SSH_TARGET_DIR, help="SSH port of server to publish to")

    parser.add_argument("--pelican", default="pelican", help="Pelican exec")
    parser.add_argument("--python", default="python", help="Python exec")

    args = vars(parser.parse_args())

    if args["debug"]:
        args["extra"] += ["-D"]
        print("args: {}".format(repr(args)))

    args["extra"] = " ".join(args["extra"])

    for task in args["tasks"]:
        TASKS[task](args)


def setup(ctx):
    """ Install all web dependencies """
    shell("cd themes/alexjf/ && bower install", ctx)


def html(ctx):
    """ Generate html sources (with base configuration) """
    shell("{pelican} {input} -o {output} -s {baseconf} {extra}", ctx)


def regenerate(ctx):
    """ Regenerate html sources (with base configuration) """
    ctx["extra"] += ["-r"]
    html(ctx)


def publish(ctx):
    """ Generate html sources (with publish configuration) """
    shell("{pelican} {input} -o {output} -s {publishconf} {extra}", ctx)


def serve(ctx):
    """ Start HTML server """
    shell("cd {output} && {python} -m pelican.server {serve_port}", ctx)


def rsync_upload(ctx):
    """ Upload using rsync (Unix-only) """
    shell("rsync -e 'ssh -p {ssh_port}' -P -rvzc --delete {output}/ {ssh_user}@{ssh_host}:{ssh-target-dir} --cvs-exclude", ctx)


def winscp_upload(ctx):
    """ Upload using winscp (Windows-only) """
    shell("winscp {ssh_user}@{ssh_host} /defaults /keepuptodate // {output} {ssh_target_dir}", ctx)


def clean(ctx):
    """ Clean output directory and cache """
    rmtree(ctx["output"])
    rmtree(ctx["cache"])


def shell(command, ctx):
    call(command.format_map(ctx), shell=True)

if __name__ == "__main__":
    main()
