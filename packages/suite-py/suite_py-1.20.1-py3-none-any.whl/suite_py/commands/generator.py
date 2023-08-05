# -*- coding: utf-8 -*-
from datetime import datetime
import os
from os import listdir
from os.path import isfile, join
import stat
import subprocess

from jinja2 import Environment, DebugUndefined, FileSystemLoader
import yaml

from suite_py.lib import logger
from suite_py.lib.handler import prompt_utils
from suite_py.lib.handler.drone_handler import DroneHandler
from suite_py.lib.handler.git_handler import GitHandler
from suite_py.lib.handler.github_handler import GithubHandler

NOW = datetime.now().strftime("%Y%m%d%H%M")


class Generator:
    def __init__(self, project, config, tokens):
        self._project = project
        self._config = config
        self._tokens = tokens
        self._artemide_path = os.path.join(config.user["projects_home"], "artemide")
        self._drone_values_path = f"{self._artemide_path}/templates/drone/values/"
        self._deploy_scripts_values_path = (
            f"{self._artemide_path}/templates/scripts/values/"
        )
        self._github = GithubHandler(tokens)

    def run(self):
        logger.warning(
            "This command requires shellcheck and shfmt, please install these tools before continuing"
        )
        logger.warning(
            "see https://github.com/koalaman/shellcheck#installing and https://github.com/mvdan/sh#shfmt for installation"
        )
        # move to artemide root directory
        os.chdir(self._artemide_path)

        env = Environment(
            loader=FileSystemLoader(self._artemide_path),
            undefined=DebugUndefined,
            trim_blocks=True,
            lstrip_blocks=True,
        )
        env.filters["to_yaml"] = to_yaml
        env.add_extension("jinja2.ext.do")

        template_type = prompt_utils.ask_choices(
            "What files do you want to generate?", ["drone", "deploy_scripts"]
        )
        commit_message = f"Autogenerated update {template_type} from suite-py {NOW}"

        autobranch = prompt_utils.ask_confirm(
            "Do you want to create branch and PR automatically?", default=False
        )

        if autobranch:
            autopush = True
        else:
            autopush = prompt_utils.ask_confirm(
                "Do you want to push automatically?", default=False
            )

        choice = prompt_utils.ask_questions_input(
            "What project do you want to work on? Enter `all` to select them all: ",
            self._project,
        )

        if choice == "all":
            projects = self._get_all_templated_projects(template_type)
        else:
            projects = choice.split(" ")

        skipped = []
        for project in projects:
            logger.info(f"{project}: Checking if there are no uncommitted files")
            git = GitHandler(project, self._config)
            git.check_repo_cloned()
            if git.is_dirty():
                if not prompt_utils.ask_confirm(
                    f"{project}: There are changes already present, do you want to continue anyway?",
                    default=False,
                ):
                    logger.error(f"{project}: skipping the project")
                    skipped.append(project)
                    continue

            branch_name = _configure_branch(git, template_type, autobranch, autopush)

            logger.info(f"{project}: Creation in progress")
            # launch generate
            if template_type == "drone":
                self._generate_drone(
                    project, f"{self._drone_values_path}{project}.yml", env
                )
            elif template_type == "deploy_scripts":
                _generate_build_script(
                    git.get_path(),
                    f"{self._deploy_scripts_values_path}{project}.yml",
                    env,
                )
                _generate_deploy_script(
                    git.get_path(),
                    f"{self._deploy_scripts_values_path}{project}.yml",
                    env,
                )
            logger.info(f"{project}: Creation completed")

            if autobranch or autopush:
                # controllo che sia cambiato effettivamente qualcosa
                if git.is_dirty(untracked=True):
                    self._git_operations(
                        git, autobranch, autopush, branch_name, commit_message
                    )
                else:
                    logger.warning(
                        f"{project}: no git operations to do. No files modified"
                    )

            logger.warning(f"Skipped projects: {skipped}")

    def _get_all_templated_projects(self, template_type):
        if template_type == "drone":
            values_path = self._drone_values_path
        elif template_type == "deploy_scripts":
            values_path = self._deploy_scripts_values_path

        return [
            f.replace(".yml", "")
            for f in listdir(values_path)
            if isfile(join(values_path, f))
        ]

    def _git_operations(self, git, autobranch, autopush, branch_name, message):
        if autobranch:
            logger.info(f"{git.get_repo()}: creating branch {branch_name}")
            git.checkout(branch_name, new=True)
            git.add()
            git.commit(message)
            git.push(branch_name)
            pr = self._github.create_pr(git.get_repo(), branch_name, message)
            logger.info(f"Pull request with number {pr.number} created! {pr.html_url}")
        elif autopush:
            if git.current_branch_name() != "master":
                git.add()
                git.commit(message)
                git.push(branch_name)
            else:
                logger.warning(
                    f"{git.get_repo()} is on master, skipping automatic push"
                )

    def _generate_drone(self, project, values_file, env):
        values = yaml.safe_load(open(values_file))
        template = env.get_template(f"templates/drone/{values['template']}.j2")
        rendered = template.render(values)

        _write_on_repo(
            os.path.join(self._config.user["projects_home"], project),
            rendered,
            ".drone.yml",
        )
        drone = DroneHandler(self._config, self._tokens, repo=project)
        drone.fmt()
        drone.validate()
        drone.sign()


def _configure_branch(git, template_type, autobranch, autopush):
    logger.info(f"{git.get_repo()}: Synchronizing the repo with the remote")
    if autobranch:
        git.sync()  # fa anche checkout su master
        return f"t/autogenerated_update_{template_type}_{NOW}"

    current_branch = git.current_branch_name()
    if autopush and git.remote_branch_exists(current_branch):
        git.fetch()
        git.pull()

    return current_branch


def _generate_build_script(project_path, values_file, env):
    file_name = "build"
    values = yaml.safe_load(open(values_file))

    val = {**values["info"], **values["build"]}
    template = env.get_template(f"templates/scripts/build/{val['template']}")
    rendered = template.render(val)

    _write_on_repo(os.path.join(project_path, "deploy"), rendered, file_name)
    _format_script(f"{project_path}/deploy/{file_name}")
    _validate_script(f"{project_path}/deploy/{file_name}")


def _generate_deploy_script(project_path, values_file, env):
    values = yaml.safe_load(open(values_file))

    for country, country_props in values["deploy"].items():
        val = {**values["info"], **country_props}
        template = env.get_template("templates/scripts/deploy/base.j2")
        rendered = template.render(val)
        file_name = f"deploy-{country}"
        _write_on_repo(os.path.join(project_path, "deploy"), rendered, file_name)
        _format_script(f"{project_path}/deploy/{file_name}")
        _validate_script(f"{project_path}/deploy/{file_name}")


def _write_on_repo(path, rendered, file_name):
    if not os.path.exists(path):
        os.mkdir(path, mode=0o755)

    fd = open(os.path.join(path, file_name), "w")
    fd.write(rendered)
    fd.close()


def _format_script(filepath):
    subprocess.run(["shfmt", "-i", "2", "-l", "-w", filepath], check=True)


def _validate_script(filepath):
    _make_executable(filepath)
    subprocess.run(["shellcheck", filepath], check=True)


def _make_executable(filepath):
    st = os.stat(filepath)
    os.chmod(filepath, st.st_mode | stat.S_IEXEC)


def to_yaml(d, indent=10):
    return yaml.dump(d, indent=indent)
