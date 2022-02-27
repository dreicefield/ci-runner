#!/usr/bin/env python3

from typing import Dict, List

from ci.model.step import Step
from ci.model.agent import Agent


class Stage:
    name: str
    agent: Agent
    steps: List[Step]
    environmnet: Dict[str, str]

    def __init__(
        self, name: str, agent: Agent, steps: List[Step], environment: Dict[str, str]
    ) -> None:
        self.name = name
        self.agent = agent
        self.steps = steps
        self.environment = environment

    def run(self, logger) -> None:
        for step in self.steps:
            step.run(logger)
