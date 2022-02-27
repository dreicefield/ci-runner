#!/usr/bin/env python3

from jinja2 import Template
from pathlib import Path
import tempfile
from typing import Dict, List
import re
import subprocess
import shutil


BASH_TEMPLATE = """#/usr/bin/env bash
set -Eeuo pipefail

{{script}}
"""


class Step:
    name: str
    agent: str
    script: str
    environmnet: Dict[str, str]
    rc: int

    def __init__(
        self, name: str, agent: str, script: str, environment: Dict[str, str]
    ) -> None:
        self.name = name
        self.script = script
        self.agent = agent
        self.environment = environment

        self.name = name.replace(" ", "")
        self.name = re.sub("[^A-Za-z0-9]+", "", name)
        self.bash_script = Path(tempfile.mkdtemp()) / f"{self.name}.sh"

        template = Template(BASH_TEMPLATE).render(script=script)
        self.bash_script.write_text(template)
        self.bash_script.chmod(0o777)

    def run(self, logger) -> None:

        logfile = Path(self.bash_script.as_posix().replace(".sh", ".log"))
        with logfile.open("w") as f:
            if self.agent:
                logger.debug(
                    "running step '%s' on agent %s", self.name, self.agent.name
                )
                subprocess.run(
                    [
                        "docker",
                        "cp",
                        self.bash_script.as_posix(),
                        f"{self.agent.name}:/tmp/{self.name}.sh",
                    ],
                    check=True,
                )
                result = subprocess.run(
                    [
                        "docker",
                        "exec",
                        "-t",
                        self.agent.name,
                        "/bin/bash",
                        "--login",
                        "-c",
                        f"'/tmp/{self.name}.sh'",
                    ],
                    stderr=subprocess.STDOUT,
                    stdout=f,
                )
            else:
                logger.debug("running step on localhost")
                self.result = subprocess.run(
                    ["/bin/bash", self.bash_script.as_posix()],
                    stderr=subprocess.STDOUT,
                    stdout=f,
                )
        self.rc = result.returncode
        if self.rc != 0:
            logger.error("Step: %s", self.name)
            logger.error(logfile.read_text())
        else:
            logger.info("Step: %s", self.name)
            logger.info(logfile.read_text())

    def cleanup(self) -> None:
        shutil.rmtree(self.bash_script.parent)
