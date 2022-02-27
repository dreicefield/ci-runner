#!/usr/bin/env python3

import logging
import subprocess
from typing import Dict


class Agent:
    name: str
    image: str
    environment: Dict[str, str]

    def __init__(self, name: str, image: str, environment: Dict[str, str]) -> None:
        self.name = name
        self.image = image
        self.environment = environment

    def run(self) -> None:
        logging.info("Starting agent '%s' based on image '%s'", self.name, self.image)
        subprocess.run(
            [
                "docker",
                "run",
                "-d",
                "--rm",
                "-it",
                "--name",
                self.name,
                self.image,
                "/bin/sleep",
                "infinity",
            ]
        )

    def cleanup(self) -> None:
        logging.info("Stopping agent '%s'", self.name)
        subprocess.run(["docker", "stop", self.name])


def get_agent_by_label(name: str, label: str) -> Agent:
    # TODO: lookup label in config file?
    return Agent("ci-agent", "ubuntu:20.04", {})
