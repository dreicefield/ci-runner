#!/usr/bin/env python3

import click
import coloredlogs
import logging
import networkx as nx
from pathlib import Path
from typing import List
import yaml

from ci.model.stage import Stage
from ci.model.step import Step
from ci.model.graph import StageGraph
from ci.model.agent import Agent, get_agent_by_label


def stage_callback(stage: Stage, arguments) -> None:
    logger = logging.getLogger(stage.name)
    logger.info("Starting")
    stage.run(logger)
    logger.info("Done")


def build_steps_from_yaml(agent: Agent, y_steps: dict) -> None:
    steps = []
    for y_step in y_steps:
        step = Step(y_step[:20], agent, y_step, {})
        steps.append(step)
    return steps


def build_stages_from_yaml(g, agent: Agent, y_stages: dict) -> None:
    # name = y_stage["stage"]

    stage_predecessor = None
    stage_logging_level = 101
    for y_stage in y_stages:
        if "steps" in y_stage:
            steps = build_steps_from_yaml(agent, y_stage["steps"])
            stage_name = y_stage["stage"]
            stage_logging_level += 1
            stage = Stage(stage_name, agent, steps, {"STAGE_NAME": stage_name})

            logging.debug("add_node %s", stage_name)
            g.add_node(stage_name, stage=stage)
            if stage_predecessor:
                logging.debug("add_edge %s <- %s", stage_name, stage_predecessor)
                g.add_edge(stage_name, stage_predecessor)
        elif "parallel" in y_stage:
            for y_parallel_stage in y_stage["parallel"]:

                steps = build_steps_from_yaml(agent, y_parallel_stage["steps"])
                parallel_stage_name = y_parallel_stage["stage"]
                parallel_stage = Stage(
                    parallel_stage_name, agent, steps.copy(), {"STAGE_NAME": stage_name}
                )

                logging.debug("add_node %s", parallel_stage_name)
                stage_logging_level += 1
                g.add_node(parallel_stage_name, stage=parallel_stage)
                if stage_predecessor:
                    logging.debug(
                        "add_edge %s <- %s", parallel_stage_name, stage_predecessor
                    )
                    g.add_edge(parallel_stage_name, stage_predecessor)
                del steps

        else:
            logging.error("Only steps|paralle blocks supported under stage")
        stage_predecessor = stage_name


def build_graph(agent, pipeline) -> StageGraph:
    g = nx.DiGraph()
    build_stages_from_yaml(g, agent, pipeline["stages"])

    for cycle in nx.simple_cycles(g):
        logging.error("Found cycles in the pipeline: %s", cycle)
        raise nx.exception.HasACycle

    return StageGraph(g)


@click.command("jenkins")
@click.option("--file", required=True, help="Jenkinsfile as YAML")
def jenkins(file: str):
    """Runs jenkinsfile"""
    y = yaml.safe_load(Path(file).read_text())

    # define default pipeline agent
    agent = get_agent_by_label("default", "default")
    if "agent" in y["pipeline"]:
        agent = get_agent_by_label("default", y["pipeline"]["agent"]["node"]["label"])

    g = build_graph(agent, y["pipeline"])

    agent.run()
    g.walk_groups(stage_callback)
    agent.cleanup()
