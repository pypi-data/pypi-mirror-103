import os
import getpass
from python_script_manager.package import PSMReader
from ..utils import (
    process_ok,
    process_step,
    success_message,
    hl,
)
from .utils import (
    create_app_ini,
    create_flask_dockerfile,
    create_docker_compose_yml,
    create_nginx_conf,
    create_nginx_dockerfile
)
from ..__main__ import main

@main.command("deploysetup")
def deploysetup_command():
    psm = PSMReader()
    prj_name = psm.get_config().get('PROJECT_NAME', None)
    processes = []
    process_ok(processes)
    
    # Creating app.ini
    process_step(f"Creating {hl('app.ini')}...", create_app_ini)
    processes.append(f"Created {hl('app.ini')}")
    process_ok(processes)

    # Creating Dockerfile for flask
    process_step(f"Creating {hl('Dockerfile')} for {hl('flask')}...", create_flask_dockerfile)
    processes.append(f"Created {hl('Dockerfile')} for {hl('flask')}")
    process_ok(processes)

    # Creating docker-compose.yml file
    process_step(f"Creating {hl('docker-compose.yml')}...", create_docker_compose_yml(prj_name))
    processes.append(f"Created {hl('docker-compose.yml')}")
    process_ok(processes)

    # Creating nginx.conf file
    process_step(f"Creating {hl('nginx.conf')}...", create_nginx_conf)
    processes.append(f"Created {hl('nginx.conf')}")
    process_ok(processes)

    # Creating Dockerfile for nginx
    process_step(f"Creating {hl('Dockerfile')} for {hl('nginx')}...", create_nginx_dockerfile)
    processes.append(f"Created {hl('Dockerfile')} for {hl('nginx')}")
    process_ok(processes)

    # Show success message
    success_message(f"Successfully made deployment setup for {hl(prj_name)}")