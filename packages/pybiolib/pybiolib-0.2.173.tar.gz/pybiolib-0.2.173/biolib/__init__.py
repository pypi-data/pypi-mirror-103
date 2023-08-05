import importlib
import sys
import os
import logging
import argparse
import tempfile

from docker.errors import ImageNotFound
from importlib_metadata import version

from biolib import cli_utils
from biolib.app import BioLibApp, BioLib
from biolib.cli_utils import BiolibValidationError
from biolib.validators.validate_zip_file import validate_zip_file
__version__ = version('pybiolib')

biolib_logger = logging.getLogger('biolib')
IS_DEV = os.getenv('BIOLIB_DEV', '').upper() == "TRUE"


def configure_logging(default_log_level):
    # set log level
    env_log_level = os.getenv('BIOLIB_LOG')
    if env_log_level is None:
        BioLib.set_logging(default_log_level)
    else:
        env_log_level_upper = env_log_level.upper()
        if env_log_level_upper == 'TRACE':
            BioLib.set_logging(BioLib.TRACE_LOGGING)
        elif env_log_level_upper == 'DEBUG':
            BioLib.set_logging(logging.DEBUG)
        elif env_log_level_upper == 'INFO':
            BioLib.set_logging(logging.INFO)
        elif env_log_level_upper == 'WARNING' or env_log_level_upper == 'WARN':
            BioLib.set_logging(logging.WARNING)
        else:
            BioLib.set_logging(logging.ERROR)


def cli():
    configure_logging(default_log_level=logging.ERROR)

    # set auth
    BioLib.set_api_token(os.getenv('BIOLIB_TOKEN'))

    # set host
    BioLib.set_host(os.getenv('BIOLIB_HOST'))

    if len(sys.argv) > 2 and sys.argv[1] == 'run':
        app_splitted = sys.argv[2].split('/')
        if len(app_splitted) == 2:
            app_author = app_splitted[0]
            app_name = app_splitted[1]
            app = BioLibApp(author=app_author, name=app_name)
            stdin = None
            if not sys.stdin.isatty() and not IS_DEV:
                stdin = sys.stdin.read()
            app_args = sys.argv[3:]
            result = app(args=app_args, stdin=stdin, files=None)
            sys.stdout.buffer.write(result.stdout)
            sys.stderr.buffer.write(result.stderr)
        else:
            print(f'App name {sys.argv[2]} was incorrectly formatted. Please use this format: app_developer/app_name')

    elif len(sys.argv) > 2 and sys.argv[1] == 'run-dev':
        provided_app_path = sys.argv[2]
        app_path = cli_utils.validate_and_get_app_path(provided_app_path)
        biolib_logger.info(f'Running BioLib application in local directory {app_path}...')
        source_files_temp_dir = tempfile.TemporaryDirectory()
        source_files_zip_path = cli_utils.get_source_files_zip(app_path, source_files_temp_dir)
        try:
            validate_zip_file(source_files_zip_path, app_path)
            yaml_data = cli_utils.get_yaml_data(app_path)
            cli_utils.validate_yaml_config(yaml_data, source_files_zip_path)
            module = cli_utils.get_main_module_from_yaml(yaml_data, validate_local_docker_only=True)

            try:
                BioLib.docker_client.images.get(module['image'])
            except ImageNotFound:
                biolib_logger.error(
                    f"Could not find local docker image {module['image']} specified in .biolib/config.yml")
                sys.exit(1)

            app_args = sys.argv[3:]
            args = cli_utils.validate_and_get_args(app_args)
            files_dict, args = cli_utils.get_files_dict_and_file_args(files=None, args=args)

            BioLib.run_local_docker_app(files_dict, args, module, source_files_temp_dir)

        except Exception as exception:
            # Exit on BiolibValidationError as we have already printed the validation errors
            if isinstance(exception, BiolibValidationError):
                biolib_logger.error('Validation check failed for config file at .biolib/config.yml')
                sys.exit(1)
            raise exception

    else:
        parser = argparse.ArgumentParser()
        parser.add_argument('--version', action='version', version=__version__)

        subparsers = parser.add_subparsers(help='command', dest='command')

        # Add subparser for run to help message makes sense
        # The actual code for running applications is above this
        _parser_run = subparsers.add_parser('run', help='Run an application on BioLib')

        # Add subparser for run to help message makes sense
        # The actual code for running local applications is above this
        _parser_run_dev = subparsers.add_parser('run-dev', help='Run an application from a local directory')

        # add subparser for push
        parser_push = subparsers.add_parser('push', help='Push an application to BioLib')
        parser_push.add_argument('author_and_app_name')
        parser_push.add_argument('--path', default='.', required=False)

        # add subparser for build-enclave
        parser_build_enclave = subparsers.add_parser('build-enclave', help='Build a nitro enclave EIF file')
        parser_build_enclave.add_argument('--dev', required=False, action='store_true')

        parser_compute_process = subparsers.add_parser('start-compute-process', help='Start a compute process')
        parser_compute_process.add_argument('--enclave', required=False, action='store_true')
        parser_compute_process.add_argument('--port', required=False, type=port_number)

        # add subparser for run-compute-node
        parser_start = subparsers.add_parser('start', help='Start a compute node')
        parser_start.add_argument('--eif', required=False, type=file_path)
        parser_start.add_argument('--port', default='5000', required=False, type=port_number)
        parser_start.add_argument('--host', default='127.0.0.1', required=False)

        args = parser.parse_args()

        if args.command == 'push':
            # always use INFO logging for push
            configure_logging(default_log_level=logging.INFO)
            BioLib.push(args.author_and_app_name, args.path)
        elif args.command == 'build-enclave':
            BioLib.build_enclave(args.dev)
        elif args.command == 'start':
            BioLib.start_compute_node(args.port, args.host, args.eif)
        elif args.command == 'start-compute-process':
            BioLib.start_compute_process(socket_port=args.port, is_running_in_enclave=args.enclave)
        else:
            print('Unrecognized command, please run biolib --help to see available options.')
            sys.exit(1)


class IllegalArgumentError(ValueError):
    pass


def file_path(path):
    if path.startswith('/'):
        full_path = path
    else:
        full_path = os.path.normpath(os.path.join(os.getcwd(), path))
    if not os.path.exists(full_path):
        raise IllegalArgumentError(f'The path {full_path} does not exist')
    return full_path


def port_number(port):
    if not port.isdigit():
        raise IllegalArgumentError(f'Port number {port} is not a number. Ports can only be numbers')

    if not (0 < int(port) < 65000):  # pylint: disable=superfluous-parens
        raise IllegalArgumentError('Port can only be between 0 and 65000')

    return port


class ImportHook(object):

    # The argument 'path' is not used, but it must be defined since importlib expects this function interface
    def find_module(self, fullname, path=None):  # pylint: disable=unused-argument
        # import hook for all imports in the form blb.*
        if fullname.split('.')[0] == 'biolib':
            return self
        else:
            return None

    def load_module(self, fullname):
        fullname_splitted = fullname.split('.')
        assert fullname_splitted[0] == 'biolib'

        # don't override existing module
        if fullname in sys.modules:
            return sys.modules[fullname]

        # dynamically create new module
        if len(fullname_splitted) == 3:
            sys.modules[fullname] = BioLibApp(author=fullname_splitted[1], name=fullname_splitted[2])
            return sys.modules[fullname]
        elif len(fullname_splitted) == 2:
            spec = importlib.util.spec_from_file_location(fullname, __file__)
            mod = importlib.util.module_from_spec(spec)
            sys.modules[fullname] = mod
        else:
            raise Exception(f'Import `{fullname}` incorrectly formatted')
        return mod


sys.meta_path = [ImportHook()]

if IS_DEV and __name__ == '__main__':
    cli()
