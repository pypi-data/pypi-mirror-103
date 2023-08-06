import os
import getpass
from python_script_manager.package import PSMReader
from ..utils import (
    command_process_step,
    process_ok,
    process_step,
    success_message,
    hl,
    take_input,
    detect_venv
)
from .utils import (
    create_wsgi_py,
    create_service_file,
    create_nginx_file
)
from ..__main__ import main

@main.command("deployproject")
def deployproject_command():
    psm = PSMReader()
    prj_name = psm.get_config().get('PROJECT_NAME', None)
    processes = []
    process_ok(processes)

    # Creating wsgi.py
    process_step(f"Creating {hl('wsgi.py')}...", create_wsgi_py(prj_name))
    processes.append(f"Created {hl('wsgi.py')}")
    process_ok(processes)

    # Creating service file
    venv_name = detect_venv()
    project_path = os.getcwd()
    username = getpass.getuser()
    process_step(f"Creating {hl(f'/etc/systemd/system/{prj_name}.service')}...",
                 create_service_file(project_path, prj_name, username, venv_name))
    processes.append(
        f"Created {hl(f'/etc/systemd/system/{prj_name}.service')}")
    process_ok(processes)

    # Starting project
    command_process_step("Starting project...", f"systemctl start {prj_name}")
    processes.append("Started project")
    process_ok(processes)

    # Enabling project
    command_process_step("Enabling project...", f"systemctl enable {prj_name}")
    processes.append("Enabled project")
    process_ok(processes)

    # Taking domain name as input
    domain_name = take_input("Enter your domain name(without any subdomain): ")

    # Creating nginx file
    process_step(f"Creating {hl(f'/etc/nginx/sites-available/{prj_name}')}...",
                 create_nginx_file(project_path, prj_name, domain_name))
    processes.append(
        f"Created {hl(f'/etc/nginx/sites-available/{prj_name}')}")
    process_ok(processes)

    # Link nginx file
    command_process_step("Linking nginx file...", f"ln -s /etc/nginx/sites-available/{prj_name} /etc/nginx/sites-enabled")
    processes.append("Linked nginx file")
    process_ok(processes)

    # Restart nginx
    command_process_step("Restarting nginx...", "systemctl restart nginx")
    processes.append("Restarted nginx")
    process_ok(processes)

    # Allowing Nginx
    command_process_step("Allowing nginx...", "ufw allow 'Nginx Full'")
    processes.append("Allowed nginx")
    process_ok(processes)

    # Show success message
    success_message(f"Successfully deployed {hl(prj_name)}")