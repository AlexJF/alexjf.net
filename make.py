#! /usr/bin/env python
# encoding: utf-8

import argparse
import os

from subprocess import check_output
from shutil import rmtree


SSH_TARGET_DIR = "/home/alex/www/public_html/alexjf_https"


def setup(ctx):
    """ Install all web dependencies """
    shell_with_npm("npm install")
    shell_with_npm("cd themes/alexjf/ && bower install")


def html(ctx):
    """ Generate html sources (with base configuration) """
    shell_with_npm("{pelican} {input} -o {output} -s {baseconf} {extra}", ctx)


def regenerate(ctx):
    """ Regenerate html sources (with base configuration) """
    ctx["extra"] += " -r "
    html(ctx)


def publish(ctx):
    """ Generate html sources (with publish configuration) """
    shell_with_npm("{pelican} {input} -o {output} -s {publishconf} {extra}", ctx)


def serve(ctx):
    """ Start HTML server """
    shell_with_npm("cd {output} && {python} -m pelican.server {serve_port}", ctx)


def rsync_upload(ctx):
    """ Upload using rsync (Unix-only) """
    shell("rsync -e 'ssh -p {ssh_port}' -P -rvzc --delete {output}/ {ssh_user}@{ssh_host}:{ssh_target_dir} --cvs-exclude", ctx)


def winscp_upload(ctx):
    """ Upload using winscp (Windows-only) """
    shell("winscp /command \"option batch abort\" \"option confirm off\" \"open sftp://{ssh_user}@{ssh_host}:{ssh_port}\" \"synchronize remote -delete -criteria=size \"\"{output}\"\" \"\"{ssh_target_dir}\"\"\" \"exit\"", ctx)


def unison_upload(ctx):
    """ Upload using unison (Windows-client-only) """
    shell("unison {output}/ ssh://{ssh_user}@{ssh_host}/{ssh_target_dir} -batch -force \"{output}/\" -ui \"text\" -sshargs \"-P {ssh_port}\"", ctx)


def clean(ctx):
    """ Clean output directory and cache """
    if os.path.exists("output"):
        rmtree(ctx["output"])

    if os.path.exists("cache"):
        rmtree(ctx["cache"])


def shell_with_npm(command, ctx={}):
    env_copy = dict(os.environ)
    env_copy["PATH"] += os.pathsep + shell("npm bin").strip()

    return shell(command, ctx, env_copy)


def shell(command, ctx={}, env=None):
    return check_output(command.format(**ctx), shell=True, universal_newlines=True, env=env)


TASKS = {
    "setup": setup,
    "html": html,
    "regenerate": regenerate,
    "publish": publish,
    "serve": serve,
    "clean": clean,
    "rsync_upload": rsync_upload,
    "winscp_upload": winscp_upload,
    "unison_upload": unison_upload,
}


def main():
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


if __name__ == "__main__":
    main()
