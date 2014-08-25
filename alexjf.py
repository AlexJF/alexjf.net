from flask import Flask

import subprocess

app = Flask(__name__)


@app.route("/git-push")
def git_push():
    subprocess.call("git pull origin master", shell=True)
    subprocess.call("make publish", shell=True)


if __name__ == '__main__':
    app.run(host="0.0.0.0")
