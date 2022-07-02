#!/usr/bin/python

# Copyright: (c) 2020, Ricardo Pescuma Domenecci
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: jenkins_slave

short_description: Manage jenkins slaves configuration using Jenkins REST API.

version_added: "2.9"

author:
    - Ricardo Pescuma Domenecci (@pescuma)

options:
    name:
        description:
            - Name that uniquely identifies an agent within this Jenkins installation.
        required: true
        type: str

    state:
        description:
            - What to do with the slave
            - "C(query): only query current state, make no changes"
            - "C(absent): remove the slave"
            - "C(present): makes sure the slave exists. It can be online, offline, connected or disconnected. "
            - "C(online): makes sure the slave is online, aka not temporarily offline. Does no connect or disconnect to the slave."
            - "C(offline): makes the slave temporarily offline"
            - "C(connected): tries to activelly connect to the slave, if the launch_method allows it."
            - "C(disconnected): tries to activelly disconnect to the slave, if the launch_method allows it."
        required: false
        type: str
        choices: ['query', 'absent', 'present', 'online', 'offline', 'connected', 'disconnected']
        default: present

    server_url:
        description:
            - URL of the Jenkins server
        required: false
        type: str
        default: http://localhost:8080

    server_username:
        description:
            - Username to authenticate with the Jenkins server
        required: false
        type: str

    server_password:
        description:
            - Password to authenticate with the Jenkins server
            - One of I(server_password) or I(server_token) can be provided
        required: false
        type: str

    server_token:
        description:
            - API Token to authenticate with the Jenkins server
            - One of I(server_password) or I(server_token) can be provided
        required: false
        type: str

    server_validate_certs:
        description:
            - Validate Jenkins server certificates
        required: false
        type: bool
        default: true

    server_timeout:
        description:
            - Timeout to wait for Jenkins server responses
        required: false
        type: int
        default: forever

    offline_reason:
        description:
            - Reason to show in Jenkins for taking this node offline
        required: false
        type: str

    disconnected_reason:
        description:
            - Reason to show in Jenkins for disconnecting this node
        required: false
        type: str

    wait_jobs_finish:
        description:
            - Wait running jobs on node to finish after taking it offline or before disconnecting it
        required: false
        type: bool
        default: true

    wait_jobs_finish_max_time:
        description:
            - Max time (in seconds) to wait for jobs to finish
            - C(0) means forever
        required: false
        type: int
        default: forever

    description:
        description:
            - Optional human-readable description for this agent.
        required: false
        type: str

    executors:
        description:
            - The maximum number of concurrent builds that Jenkins may perform on this node.
        required: false
        type: int
        default: 1 when creating, current value when changing node

    root_dir:
        description:
            - "Remote root directory"
            - An agent needs to have a directory dedicated to Jenkins. Specify the path to this directory on the agent. It is best to use an absolute path, such as /var/jenkins or c:\\jenkins. This should be a path local to the agent machine. There is no need for this path to be visible from the master.
        required: false
        type: str

    labels:
        description:
            - Labels (or tags) are used to group multiple agents into one logical group. 
        required: false
        type: str

    usage:
        description:
            - Controls how Jenkins schedules builds on this node.
            - "C(normal): Use this node as much as possible"
            - "C(exclusive): Only build jobs with label expressions matching this node"
        required: false
        type: str
        choices: ['normal', 'exclusive']
        default: normal when creating, current value when changing node

    launch_method:
        description:
            - Controls how Jenkins starts this agent. 
            - "C(jnlp): Launch agent by connecting it to the master (Java Web Start)"
            - "C(command): Launch agent via execution of command on the master"
            - "C(ssh): Launch agent agents via SSH"
            - "C(wmi): Let Jenkins control this Windows agent as a Windows service (Windows Management Instrumentation)"
        required: false
        type: str
        choices: ['jnlp', 'command', 'ssh', 'wmi']
        default: jnlp when creating, current value when changing node

    jnlp_workdir_enabled:
        description:
            - Allows disabling Remoting Work Directory for the agent. In such case the agent will be running in the legacy mode without logging enabled by default.
            - Only used if I(launch_method='jnlp')
        required: false
        type: bool
        default: no when creating, current value when changing node

    jnlp_workdir_path:
        description:
            - "Custom WorkDir path"
            - If defined, a custom Remoting work directory will be used instead of the Agent Root Directory. This option has no environment variable resolution so far, it is recommended to use only absolute paths.
            - Only used if I(launch_method='jnlp')
        required: false
        type: str
        default: empty when creating, current value when changing node

    jnlp_internal_dir:
        description:
            - "Internal data directory"
            - Defines a storage directory for the internal data. This directory will be created within the Remoting working directory.
            - Only used if I(launch_method='jnlp')
        required: false
        type: str
        default: remoting when creating, current value when changing node

    jnlp_fail_if_workspace_missing:
        description:
            - If defined, Remoting will fail at startup if the target work directory is missing. The option may be used to detect infrastructure issues like failed mount.
            - Only used if I(launch_method='jnlp')
        required: false
        type: bool
        default: no when creating, current value when changing node

    jnlp_tunnel:
        description:
            - "Tunnel connection through"
            - This tunneling option allows you to route this connection to another host/port.
            - Only used if I(launch_method='jnlp')
        required: false
        type: str
        default: empty when creating, current value when changing node

    jnlp_jvm_options:
        description:
            - If the agent JVM should be launched with additional VM arguments, such as "-Xmx256m", specify those here.
            - Only used if I(launch_method='jnlp')
        required: false
        type: str
        default: empty when creating, current value when changing node

    command_launch_command:
        description:
            - Single command to launch an agent program, which controls the agent computer and communicates with the master. Jenkins assumes that the executed program launches the agent.jar program on the correct machine.
            - Only used if I(launch_method='command')
        required: false
        type: str
        default: empty when creating, current value when changing node

    wmi_admin_username:
        description:
            - Provide the name of the Windows user who has the administrative access on this computer, such as 'Administrator'. This information is necessary to start a process remotely.
            - Only used if I(launch_method='wmi')
        required: false
        type: str
        default: empty when creating, current value when changing node

    wmi_admin_password:
        description:
            - Password for the user expecified in I(wmi_admin_username)
            - Only used if I(launch_method='wmi')
        required: false
        type: str
        default: empty when creating, current value when changing node

    wmi_host:
        description:
            - Provide the host name of the Windows host if different to the name of the Agent.
            - Only used if I(launch_method='wmi')
        required: false
        type: str
        default: empty when creating, current value when changing node

    wmi_service_run_as:
        description:
            - Sometimes the administrator account that can install a service remotely might not be the user account you want to run your Jenkins agent (one reason you might want to do this is to run your builds/tests in more restricted account because you don't trust them. Another reason you might want to do this is to run agents in some domain user account.) This option lets you do this.
            - "C(local_system): Use Local System User"
            - "C(user): Log on using a different account"
            - "C(administrator): Use Administrator account given above"
            - Only used if I(launch_method='wmi')
        required: false
        type: str
        choices: ['local_system', 'user', 'administrator']
        default: local_system when creating, current value when changing node

    wmi_service_username:
        description:
            - Username to run the service 
            - Only used if I(launch_method='wmi') and I(wmi_service_run_as='user')
        required: false
        type: str
        default: empty when creating, current value when changing node

    wmi_service_password:
        description:
            - Password for the user expecified in I(wmi_service_username)
            - Only used if I(launch_method='wmi') and I(wmi_service_run_as='user')
        required: false
        type: str
        default: empty when creating, current value when changing node

    wmi_java_path:
        description:
            - "Path to java executable"
            - Path to the Java executable to be used on this node. Defaults to "java", assuming JRE is installed and available on system PATH (e.g. C:\\Program Files\\Java\\jre7\\bin\\java.exe)
            - Only used if I(launch_method='wmi')
        required: false
        type: str
        default: empty when creating, current value when changing node

    wmi_jvm_options:
        description:
            - Additional VM arguments
            - Only used if I(launch_method='wmi')
        required: false
        type: str
        default: empty when creating, current value when changing node

    ssh_host:
        description:
            - Agent's Hostname or IP to connect.
            - Only used if I(launch_method='ssh')
        required: false
        type: str
        default: empty when creating, current value when changing node

    ssh_port:
        description:
            - The TCP port on which the agent's SSH daemon is listening, usually 22.
            - Only used if I(launch_method='ssh')
        required: false
        type: int
        default: 22 when creating, current value when changing node

    ssh_credentials_id:
        description:
            - Select the credentials to be used for logging in to the remote host. This must have been previously created.
            - Only used if I(launch_method='ssh')
        required: false
        type: str
        default: empty when creating, current value when changing node

    ssh_host_verification:
        description:
            - Controls how Jenkins verifies the SSH key presented by the remote host whilst connecting.
            - "C(known_hosts): Known hosts file"
            - "C(key): Manually provided key"
            - "C(manually_trusted): Manually trusted key"
            - "C(none): Non verifying"
            - Only used if I(launch_method='ssh')
        required: false
        type: str
        choices: ['known_hosts', 'key', 'manually_trusted', 'none']
        default: known_hosts when creating, current value when changing node

    ssh_host_key:
        description:
            - The SSH key expected for this connection. This key should be in the form `algorithm value` where algorithm is one of ssh-rsa or ssh-dss, and value is the Base 64 encoded content of the key.
            - Only used if I(launch_method='ssh') and I(ssh_host_verification='key')
        required: false
        type: str
        default: empty when creating, current value when changing node

    ssh_host_manually_trusted_require_initial_verification:
        description:
            - Require a user with Computer.CONFIGURE permission to authorise the key presented during the first connection to this host before the connection will be allowed to be established.
            - Only used if I(launch_method='ssh') and I(ssh_host_verification='manually_trusted')
        required: false
        type: bool
        default: no when creating, current value when changing node

    ssh_java_path:
        description:
            - This java Path will be used to start the jvm. (/mycustomjdkpath/bin/java ) If empty Jenkins will search java command in the agent 
            - Only used if I(launch_method='ssh')
        required: false
        type: str
        default: empty when creating, current value when changing node

    ssh_jvm_options:
        description:
            - Additional arguments for the JVM, such as -Xmx or GC options
            - Only used if I(launch_method='ssh')
        required: false
        type: str
        default: empty when creating, current value when changing node

    ssh_command_prefix:
        description:
            - "Prefix Start Agent Command"
            - What you enter here will be prepended to the launch command.
            - Only used if I(launch_method='ssh')
        required: false
        type: str
        default: empty when creating, current value when changing node

    ssh_command_suffix:
        description:
            - "Suffix Start Agent Command"
            - What you enter here will be appended to the launch command.
            - Only used if I(launch_method='ssh')
        required: false
        type: str
        default: empty when creating, current value when changing node

    ssh_connection_timeout:
        description:
            - "Connection Timeout in Seconds"
            - Set the timeout value for ssh agent launch in seconds. If empty, it will be reset to default value.
            - Only used if I(launch_method='ssh')
        required: false
        type: str
        default: empty when creating, current value when changing node

    ssh_retries:
        description:
            - "Maximum Number of Retries"
            - Set the number of times the SSH connection will be retried if the initial connection results in an error. If empty, it will be reset to default value.
            - Only used if I(launch_method='ssh')
        required: false
        type: int
        default: empty when creating, current value when changing node

    ssh_wait_between_retries:
        description:
            - "Seconds To Wait Between Retries"
            - Set the number of seconds to wait between retry attempts of the initial SSH connection.
            - Only used if I(launch_method='ssh')
        required: false
        type: int
        default: empty when creating, current value when changing node

    ssh_tcp_no_delay:
        description:
            - "Use TCP_NODELAY flag on the SSH connection"
            - Enable/Disables the TCP_NODELAY flag on the SSH connection. If set, disable the Nagle algorithm. This means that segments are always sent as soon as possible, even if there is only a small amount of data. When not set, data is buffered until there is a sufficient amount to send out, thereby avoiding the frequent sending of small packets, which results in poor utilization of the network.
            - Only used if I(launch_method='ssh')
        required: false
        type: bool
        default: yes when creating, current value when changing node

    ssh_workdir:
        description:
            - "Remoting Work directory"
            - The Remoting work directory is an internal data storage, which may be used by Remoting to store caches, logs and other metadata. For more details see Remoting Work directory If remoting parameter "-workDir PATH" or "-jar-cache PATH" is set in Suffix Start Agent Command this field will be ignored. If empty, the Remote root directory is used as Remoting Work directory
            - Only used if I(launch_method='ssh')
        required: false
        type: str
        default: empty when creating, current value when changing node

    availability:
        description:
            - Controls when Jenkins starts and stops this agent.
            - "C(always): Keep this agent online as much as possible"
            - "C(on_demand): Bring this agent online when in demand, and take offline when idle"
        required: false
        type: str
        choices: ['always', 'on_demand']
        default: always when creating, current value when changing node

    on_demand_in_demand_delay:
        description:
            - The number of minutes for which jobs must have been waiting in the queue before Jenkins will attempt to bring this agent online.
            - Only used if I(availability='on_demand')
        required: false
        type: int
        default: 0 when creating, current value when changing node

    on_demand_idle_delay:
        description:
            - The number of minutes that this agent must remain idle before Jenkins will take it offline.
            - Only used if I(availability='on_demand')
        required: false
        type: int
        default: 1 when creating, current value when changing node

requirements:
  - "python-jenkins >= 0.4.12"
'''

EXAMPLES = '''
# Query the state of a slave
- name: Query slave state
  jenkins_slave:
    name: slave_name
    state: query

# Creates (if needed) a jnlp slave. The secret that must be used to connect is stored in return.jnlp_secret
- name: Create a jnlp slave
  jenkins_slave:
    name: slave_name
    state: online
    launch_method: jnlp
  register: return

# Creates (if needed) a wmi slave. Because this module only works on linux, you may need to delegate the work
- name: Create a wmi slave
  jenkins_slave:
    name: slave_name
    state: online
    launch_method: wmi
  delegate_to: localhost

# Sets a slave as temporarily offline
- name: Take slave offline
  jenkins_slave:
    name: slave_name
    state: offline
    offline_reason: Testing ansible
'''

RETURN = '''
name:
    description: Name that uniquely identifies an agent within this Jenkins installation.
    type: str
    returned: always

state:
    description: Current state of the slave
    type: str
    returned: always

offline_reason:
    description: Reason to show in Jenkins for taking this node offline
    type: str
    returned: if I(state=offline)

disconnected_reason:
    description: Reason to show in Jenkins for disconnecting this node
    type: str
    returned: if I(state=disconnected)

description:
    description: Optional human-readable description for this agent.
    type: str
    returned: always

executors:
    description: The maximum number of concurrent builds that Jenkins may perform on this node.
    type: int
    returned: always

root_dir:
    description: Remote root directory
    type: str
    returned: always

labels:
    description: Labels (or tags) are used to group multiple agents into one logical group. 
    type: str
    returned: always

usage:
    description: Controls how Jenkins schedules builds on this node.
    type: str
    sample: normal, exclusive
    returned: always

launch_method:
    description: Controls how Jenkins starts this agent. 
    type: str
    sample: jnlp, command, ssh, wmi
    returned: always

jnlp_workdir_enabled:
    description: Allows disabling Remoting Work Directory for the agent. In such case the agent will be running in the legacy mode without logging enabled by default.
    type: bool
    returned: if I(launch_method='jnlp')

jnlp_workdir_path:
    description: Custom WorkDir path
    type: str
    returned: if I(launch_method='jnlp')

jnlp_internal_dir:
    description: Internal data directory
    type: str
    returned: if I(launch_method='jnlp')

jnlp_fail_if_workspace_missing:
    description: If defined, Remoting will fail at startup if the target work directory is missing. The option may be used to detect infrastructure issues like failed mount.
    type: bool
    returned: if I(launch_method='jnlp')

jnlp_tunnel:
    description: Tunnel connection through
    type: str
    returned: if I(launch_method='jnlp')

jnlp_jvm_options:
    description: If the agent JVM should be launched with additional VM arguments, such as "-Xmx256m", specify those here.
    type: str
    returned: if I(launch_method='jnlp')

jnlp_secret:
    description: The secret that must be used to connect to this jnlp slave
    type: str
    returned: if I(launch_method='jnlp')

command_launch_command:
    description: Single command to launch an agent program, which controls the agent computer and communicates with the master. Jenkins assumes that the executed program launches the agent.jar program on the correct machine.
    type: str
    returned: if I(launch_method='command')

wmi_admin_username:
    description: Provide the name of the Windows user who has the administrative access on this computer, such as 'Administrator'. This information is necessary to start a process remotely.
        - Only used if I(launch_method='wmi')
    type: str
    returned: if I(launch_method='wmi')

wmi_admin_password:
    description: Password for the user expecified in I(wmi_admin_username)
    type: str
    returned: if I(launch_method='wmi')

wmi_host:
    description: Provide the host name of the Windows host if different to the name of the Agent.
    type: str
    returned: if I(launch_method='wmi')

wmi_service_run_as:
    description: Sometimes the administrator account that can install a service remotely might not be the user account you want to run your Jenkins agent (one reason you might want to do this is to run your builds/tests in more restricted account because you don't trust them. Another reason you might want to do this is to run agents in some domain user account.) This option lets you do this.
    type: str
    sample: local_system, user, administrator
    returned: if I(launch_method='wmi')

wmi_service_username:
    description: Username to run the service 
    type: str
    returned: if I(launch_method='wmi') and I(wmi_service_run_as='user')

wmi_service_password:
    description: Password for the user expecified in I(wmi_service_username)
    type: str
    returned: if I(launch_method='wmi') and I(wmi_service_run_as='user')

wmi_java_path:
    description: "Path to java executable"
    required: false
    type: str
    returned: if I(launch_method='wmi')

wmi_jvm_options:
    description: Additional VM arguments
    type: str
    returned: if I(launch_method='wmi')

ssh_host:
    description: Agent's Hostname or IP to connect.
    type: str
    returned: if I(launch_method='ssh')

ssh_port:
    description: The TCP port on which the agent's SSH daemon is listening, usually 22.
    type: int
    returned: if I(launch_method='ssh')

ssh_credentials_id:
    description: Select the credentials to be used for logging in to the remote host. This must have been previously created.
        - Only used if I(launch_method='ssh')
    required: false
    type: str
    default: empty when creating, current value when changing node
    returned: if I(launch_method='ssh')

ssh_host_verification:
    description: Controls how Jenkins verifies the SSH key presented by the remote host whilst connecting.
    type: str
    sample: known_hosts, key, manually_trusted, none
    returned: if I(launch_method='ssh')

ssh_host_key:
    description: The SSH key expected for this connection. This key should be in the form `algorithm value` where algorithm is one of ssh-rsa or ssh-dss, and value is the Base 64 encoded content of the key.
    type: str
    returned: if I(launch_method='ssh') and I(ssh_host_verification='key')

ssh_host_manually_trusted_require_initial_verification:
    description: Require a user with Computer.CONFIGURE permission to authorise the key presented during the first connection to this host before the connection will be allowed to be established.
    type: bool
    returned: if I(launch_method='ssh') and I(ssh_host_verification='manually_trusted')

ssh_java_path:
    description: This java Path will be used to start the jvm. (/mycustomjdkpath/bin/java ) If empty Jenkins will search java command in the agent 
    type: str
    returned: if I(launch_method='ssh')

ssh_jvm_options:
    description: Additional arguments for the JVM, such as -Xmx or GC options
    type: str
    returned: if I(launch_method='ssh')

ssh_command_prefix:
    description: Prefix Start Agent Command
    type: str
    returned: if I(launch_method='ssh')

ssh_command_suffix:
    description: Suffix Start Agent Command
    type: str
    returned: if I(launch_method='ssh')

ssh_connection_timeout:
    description: Connection Timeout in Seconds
    type: str
    returned: if I(launch_method='ssh')

ssh_retries:
    description: Maximum Number of Retries
    type: int
    returned: if I(launch_method='ssh')

ssh_wait_between_retries:
    description: Seconds To Wait Between Retries
    type: int
    returned: if I(launch_method='ssh')

ssh_tcp_no_delay:
    description: Use TCP_NODELAY flag on the SSH connection
    type: bool
    returned: if I(launch_method='ssh')

ssh_workdir:
    description: Remoting Work directory
    type: str
    returned: if I(launch_method='ssh')

availability:
    description: Controls when Jenkins starts and stops this agent.
    type: str
    sample: always, on_demand

on_demand_in_demand_delay:
    description: The number of minutes for which jobs must have been waiting in the queue before Jenkins will attempt to bring this agent online.
    type: int
    returned: if I(availability='on_demand')

on_demand_idle_delay:
    description: The number of minutes that this agent must remain idle before Jenkins will take it offline.
    type: int
    returned: if I(availability='on_demand')

'''

import traceback
from string import Template
import json

from ansible.module_utils.basic import AnsibleModule, missing_required_lib
from ansible.module_utils._text import to_native

JENKINS_IMP_ERR = None
try:
    import jenkins
    python_jenkins_installed = True
except ImportError:
    JENKINS_IMP_ERR = traceback.format_exc()
    python_jenkins_installed = False


def run_module():
    module_args = dict(
        server_url = dict(required=False, type="str", default="http://localhost:8080"),
        server_username = dict(required=False, type="str", default=None),
        server_password = dict(required=False, no_log=True, type="str", default=None),
        server_token = dict(required=False, no_log=True, type="str", default=None),
        server_validate_certs = dict(required=False, type="bool", default=True),
        server_timeout = dict(required=False, type="int", default=None),

        name = dict(required=True, type='str'),
        state = dict(required=False, choices=[
                'query',
                'absent',
                'present',
                'online',
                'offline',
                'connected',
                'disconnected'
                ],
            default='online'),
        offline_reason = dict(required=False, type="str", default=None),
        disconnected_reason = dict(required=False, type="str", default=None),
        wait_jobs_finish = dict(required=False, type="bool", default=True),
        wait_jobs_finish_max_time = dict(required=False, type="int", default=0),

        description = dict(required=False, type="str", default=None),
        executors = dict(required=False, type="int", default=None),
        root_dir = dict(required=False, type="str", default=None),
        labels = dict(required=False, type="str", default=None),
        usage = dict(required=False, choices=[ 'normal', 'exclusive'], default=None),
        launch_method = dict(required=False, choices=[ 
                'jnlp', 
                'command',
                'ssh',
                'wmi'
                ],
            default=None),
        jnlp_workdir_enabled = dict(required=False, type="bool", default=None),
        jnlp_workdir_path = dict(required=False, type="str", default=None),
        jnlp_internal_dir = dict(required=False, type="str", default=None),
        jnlp_fail_if_workspace_missing = dict(required=False, type="bool", default=None),
        jnlp_tunnel = dict(required=False, type="str", default=None),
        jnlp_jvm_options = dict(required=False, type="str", default=None),
        command_launch_command = dict(required=False, type="str", default=None),
        wmi_admin_username = dict(required=False, type="str", default=None),
        wmi_admin_password = dict(required=False, no_log=True, type="str", default=None),
        wmi_host = dict(required=False, type="str", default=None),
        wmi_service_run_as = dict(required=False, choices=[ 
                'local_system', 
                'user',
                'administrator'
                ],
            default=None),
        wmi_service_username = dict(required=False, type="str", default=None),
        wmi_service_password = dict(required=False, no_log=True, type="str", default=None),
        wmi_java_path = dict(required=False, type="str", default=None),
        wmi_jvm_options = dict(required=False, type="str", default=None),
        ssh_host = dict(required=False, type="str", default=None),
        ssh_port = dict(required=False, type="int", default=None),
        ssh_credentials_id = dict(required=False, type="str", default=None),
        ssh_host_verification = dict(required=False, choices=[ 
                'known_hosts', 
                'key',
                'manually_trusted',
                'none'
                ],
            default=None),
        ssh_host_key = dict(required=False, type="str", default=None),
        ssh_host_manually_trusted_require_initial_verification = dict(required=False, type="bool", default=None),
        ssh_java_path = dict(required=False, type="str", default=None),
        ssh_jvm_options = dict(required=False, type="str", default=None),
        ssh_command_prefix = dict(required=False, type="str", default=None),
        ssh_command_suffix = dict(required=False, type="str", default=None),
        ssh_connection_timeout = dict(required=False, type="int", default=None),
        ssh_retries = dict(required=False, type="int", default=None),
        ssh_wait_between_retries = dict(required=False, type="int", default=None),
        ssh_tcp_no_delay = dict(required=False, type="bool", default=None),
        ssh_workdir = dict(required=False, type="str", default=None),
        availability = dict(required=False, choices=[ 
                'always', 
                'on_demand'
                ],
            default=None),
        on_demand_in_demand_delay = dict(required=False, type="int", default=None),
        on_demand_idle_delay = dict(required=False, type="int", default=None)
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    if not python_jenkins_installed:
        module.fail_json(
            msg=missing_required_lib("python-jenkins",
                                     url="https://python-jenkins.readthedocs.io/en/latest/install.html"),
            exception=JENKINS_IMP_ERR)


    args_escaped = dict()

    for key in module.params:
        if key.startswith('server_'):
            continue
        val = module.params[key]
        if val == None:
            val = 'null'
        elif isinstance(val, str):
            val = '"' + val.replace('\\', '\\\\').replace('"', '\\"') + '"'
        elif isinstance(val, bool):
            val = str(val).lower()
        else:
            val = str(val)

        args_escaped[key] = val

    script = Template("""
import jenkins.model.*
import hudson.model.*
import hudson.node_monitors.*
import jenkins.slaves.*
import hudson.slaves.*
import hudson.util.*
import java.util.concurrent.*
import groovy.json.*


args = [
	state: $state,
	offline_reason: $offline_reason,
	disconnected_reason: $disconnected_reason,
	wait_jobs_finish: $wait_jobs_finish,
	wait_jobs_finish_max_time: $wait_jobs_finish_max_time,
	name: $name,

	description: $description,
	executors: $executors,
	root_dir: $root_dir,
	labels: $labels,
	usage: $usage,
	launch_method: $launch_method,
	jnlp_workdir_enabled: $jnlp_workdir_enabled,
	jnlp_workdir_path: $jnlp_workdir_path,
	jnlp_internal_dir: $jnlp_internal_dir,
	jnlp_fail_if_workspace_missing: $jnlp_fail_if_workspace_missing,
	jnlp_tunnel: $jnlp_tunnel,
	jnlp_jvm_options: $jnlp_jvm_options,
	command_launch_command: $command_launch_command,
	wmi_admin_username: $wmi_admin_username,
	wmi_admin_password: $wmi_admin_password,
	wmi_host: $wmi_host,
	wmi_service_run_as: $wmi_service_run_as,
	wmi_service_username: $wmi_service_username,
	wmi_service_password: $wmi_service_password,
	wmi_java_path: $wmi_java_path,
	wmi_jvm_options: $wmi_jvm_options,
	ssh_host: $ssh_host,
	ssh_port: $ssh_port,
	ssh_credentials_id: $ssh_credentials_id,
	ssh_host_verification: $ssh_host_verification,
	ssh_host_key: $ssh_host_key,
	ssh_host_manually_trusted_require_initial_verification: $ssh_host_manually_trusted_require_initial_verification,
	ssh_java_path: $ssh_java_path,
	ssh_jvm_options: $ssh_jvm_options,
	ssh_command_prefix: $ssh_command_prefix,
	ssh_command_suffix: $ssh_command_suffix,
	ssh_connection_timeout: $ssh_connection_timeout,
	ssh_retries: $ssh_retries,
	ssh_wait_between_retries: $ssh_wait_between_retries,
	ssh_tcp_no_delay: $ssh_tcp_no_delay,
	ssh_workdir: $ssh_workdir,
	availability: $availability,
	on_demand_in_demand_delay: $on_demand_in_demand_delay,
	on_demand_idle_delay: $on_demand_idle_delay
]

args.description = to_string_arg(args.description)
args.executors = to_int_arg(args.executors, 1)
args.root_dir = to_string_arg(args.root_dir)
args.labels = to_string_arg(args.labels)
args.usage = to_choice_arg(args.usage, 'normal')
args.launch_method = to_choice_arg(args.launch_method, 'jnlp')
args.jnlp_workdir_enabled = to_bool_arg(args.jnlp_workdir_enabled, true)
args.jnlp_workdir_path = to_string_arg(args.jnlp_workdir_path)
args.jnlp_internal_dir = to_string_arg(args.jnlp_internal_dir, 'remoting')
args.jnlp_fail_if_workspace_missing = to_bool_arg(args.jnlp_fail_if_workspace_missing, false)
args.jnlp_tunnel = to_string_arg(args.jnlp_tunnel)
args.jnlp_jvm_options = to_string_arg(args.jnlp_jvm_options)
args.command_launch_command = to_string_arg(args.command_launch_command)
args.wmi_admin_username = to_string_arg(args.wmi_admin_username)
args.wmi_admin_password = to_string_arg(args.wmi_admin_password)
args.wmi_host = to_string_arg(args.wmi_host)
args.wmi_service_run_as = to_choice_arg(args.wmi_service_run_as, 'local_system')
args.wmi_service_username = to_string_arg(args.wmi_service_username)
args.wmi_service_password = to_string_arg(args.wmi_service_password)
args.wmi_java_path = to_string_arg(args.wmi_java_path)
args.wmi_jvm_options = to_string_arg(args.wmi_jvm_options)
args.ssh_host = to_string_arg(args.ssh_host)
args.ssh_port = to_int_arg(args.ssh_port, 22)
args.ssh_credentials_id = to_string_arg(args.ssh_credentials_id)
args.ssh_host_verification = to_choice_arg(args.ssh_host_verification, 'known_hosts')
args.ssh_host_key = to_string_arg(args.ssh_host_key)
args.ssh_host_manually_trusted_require_initial_verification = to_bool_arg(args.ssh_host_manually_trusted_require_initial_verification, false)
args.ssh_java_path = to_string_arg(args.ssh_java_path)
args.ssh_jvm_options = to_string_arg(args.ssh_jvm_options)
args.ssh_command_prefix = to_string_arg(args.ssh_command_prefix)
args.ssh_command_suffix = to_string_arg(args.ssh_command_suffix)
args.ssh_connection_timeout = to_int_arg(args.ssh_connection_timeout, null)
args.ssh_retries = to_int_arg(args.ssh_retries, null)
args.ssh_wait_between_retries = to_int_arg(args.ssh_wait_between_retries, null)
args.ssh_tcp_no_delay = to_bool_arg(args.ssh_tcp_no_delay, true)
args.ssh_workdir = to_string_arg(args.ssh_workdir)
args.availability = to_choice_arg(args.availability, 'always')
args.on_demand_in_demand_delay = to_int_arg(args.on_demand_in_demand_delay, 0)
args.on_demand_idle_delay = to_int_arg(args.on_demand_idle_delay, 1)


def process() {		
	node = getNode(args.name)

	changed = false

	switch(args.state) {
		case 'query': 
			break
		
		case 'absent':
			changed = removeNode(node)
			break

		case 'present':
		case 'online':
		case 'offline':
		case 'connected':
		case 'disconnected':
			if (node == null)
				changed = createNode()
			else
				changed = changeNode(node)
			break
		
		default:
			throw new Exception("Unknown state: " + args.state)
	}

	result = getCurrentState()
	result.changed = changed
	
	return result
}


def createNode() {
	Jenkins.instance.addNode(createNodeObject())
	
	applyState()

	return true
}


def changeNode(node) {
	current = getCurrentState(node)
	changed = false
	
	for (e in current) {
		arg = args[e.key]
		cur = current[e.key]

		if (arg instanceof Map)
			arg_replaceDefault(arg, cur)
	}

	if (args.root_dir.set && current.root_dir != args.root_dir.val) {
		changed = true
	}

	if (isLauncherChange(current)) {
		changed = true
	}

	if (isAvailabilityChange(current)) {
		changed = true
	}

	if (isUsageChange(current)) {
		changed = true
	}

	if (args.description.set && current.description != args.description.val) {
		changed = true
	}

	if (args.executors.set && current.executors != args.executors.val) {
		changed = true
	}

	if (args.labels.set && current.labels != args.labels.val) {
		changed = true
	}

	if (changed) {
		Jenkins.instance.addNode(createNodeObject())
	}

	if (applyState()) {
		changed = true
	}
		
	return changed
}


def isUsageChange(current) {
	if (!args.usage.set)
		return false
		
	if (arg_different(args.usage, current.usage))
		return true
	
	return false;
}


def isAvailabilityChange(current) {
	if (!args.availability.set)
		return false
		
	if (arg_different(args.availability, current.availability))
		return true
	
	if (current.availability == 'on_demand') {
		if (arg_different(args.on_demand_in_demand_delay, current.on_demand_in_demand_delay))
			return true
		if (arg_different(args.on_demand_idle_delay, current.on_demand_idle_delay))
			return true
	}

	return false
}


def isLauncherChange(current) {
	if (!args.launch_method.set)
		return false
		
	if (arg_different(args.launch_method, current.launch_method))
		return true
	
	if (current.launch_method == 'jnlp') {
		if (arg_different(args.jnlp_workdir_enabled, current.jnlp_workdir_enabled))
			return true
		if (current.jnlp_workdir_enabled) {
			if (arg_different(args.jnlp_workdir_path, current.jnlp_workdir_path))
				return true
		}
		if (arg_different(args.jnlp_internal_dir, current.jnlp_internal_dir))
			return true
		if (arg_different(args.jnlp_fail_if_workspace_missing, current.jnlp_fail_if_workspace_missing))
			return true
		if (arg_different(args.jnlp_tunnel, current.jnlp_tunnel))
			return true
		if (arg_different(args.jnlp_jvm_options, current.jnlp_jvm_options))
			return true
	}

	if (current.launch_method == 'command') {
		if (arg_different(args.command_launch_command, current.command_launch_command))
			return true
	}
	
	if (current.launch_method == 'wmi') {
		if (arg_different(args.wmi_host, current.wmi_host))
			return true
		if (arg_different(args.wmi_admin_username, current.wmi_admin_username))
			return true
		if (arg_different(args.wmi_admin_password, current.wmi_admin_password))
			return true
		if (arg_different(args.wmi_java_path, current.wmi_java_path))
			return true
		if (arg_different(args.wmi_jvm_options, current.wmi_jvm_options))
			return true
		if (args.wmi_service_run_as.set) {
			if (arg_different(args.wmi_service_run_as, current.wmi_service_run_as))
				return true
			if (current.wmi_service_run_as == 'user') {
				if (arg_different(args.wmi_service_username, current.wmi_service_username))
					return true
				if (arg_different(args.wmi_service_password, current.wmi_service_password))
					return true
			}
		}
	}
	
	if (current.launch_method == 'ssh') {
		if (arg_different(args.ssh_host, current.ssh_host))
			return true
		if (arg_different(args.ssh_port, current.ssh_port))
			return true
		if (arg_different(args.ssh_credentials_id, current.ssh_credentials_id))
			return true
		if (args.ssh_host_verification.set) {
			if (arg_different(args.ssh_host_verification, current.ssh_host_verification))
				return true
			if (current.ssh_host_verification == 'key') {
				if (arg_different(args.ssh_host_key, current.ssh_host_key))
					return true
			}
			if (current.ssh_host_verification == 'manually_trusted') {
				if (arg_different(args.ssh_host_manually_trusted_require_initial_verification, current.ssh_host_manually_trusted_require_initial_verification))
					return true
			}
		}
		if (arg_different(args.ssh_java_path, current.ssh_java_path))
			return true
		if (arg_different(args.ssh_jvm_options, current.ssh_jvm_options))
			return true
		if (arg_different(args.ssh_command_prefix, current.ssh_command_prefix))
			return true
		if (arg_different(args.ssh_command_suffix, current.ssh_command_suffix))
			return true
		if (arg_different(args.ssh_connection_timeout, current.ssh_connection_timeout))
			return true
		if (arg_different(args.ssh_retries, current.ssh_retries))
			return true
		if (arg_different(args.ssh_wait_between_retries, current.ssh_wait_between_retries))
			return true
		if (arg_different(args.ssh_tcp_no_delay, current.ssh_tcp_no_delay))
			return true
		if (arg_different(args.ssh_workdir, current.ssh_workdir))
			return true
	}
	
	return false
}


def removeNode(node) {
	if (node == null)
		return false
	
	if (args.wait_jobs_finish)
		makeTemporarilyOffline(node, 'Slave is going to be removed')
	
	node.computer.doDoDelete()
	return true
}


def getCurrentState(node = null) {
	if (node == null)
		node = getNode(args.name)

	result = [:]
	
	computer = node != null ? node.computer : null
	
	if (node == null) {
		result.state = 'absent'
		
	} else {
		if (computer.temporarilyOffline)
			result.state = 'offline'
		else if (!computer.launchSupported)
			result.state = 'online'
		else if (computer.offline)
			result.state = 'disconnected'
		else
			result.state = 'connected'
		
		if (result.state == 'offline')
			result.offline_reason = computer.offlineCauseReason
		
		if (result.state == 'disconnected')
			result.disconnected_reason = computer.offlineCauseReason
		
		result.name = node.nodeName
		result.description = node.nodeDescription ?: ''
		result.executors = node.numExecutors
		result.root_dir = node.remoteFS ?: ''
		result.labels = node.labelString ?: ''
		result.usage = node.mode  == Node.Mode.EXCLUSIVE ? 'exclusive' : 'normal'
		
		launcher = node.launcher
		
		if (launcher instanceof JNLPLauncher) {
			wds = launcher.workDirSettings
			
			result.launch_method = 'jnlp'
			result.jnlp_workdir_enabled = !wds.disabled
			if (result.jnlp_workdir_enabled)
				result.jnlp_workdir_path = wds.workDirPath ?: ''
			result.jnlp_internal_dir = wds.internalDir ?: ''
			result.jnlp_fail_if_workspace_missing = wds.failIfWorkDirIsMissing
			result.jnlp_tunnel = launcher.@tunnel ?: ''
			result.jnlp_jvm_options = launcher.@vmargs ?: ''
			result.jnlp_secret = computer.jnlpMac
			
		} else if (isInstanceOf(launcher, 'hudson.slaves.CommandLauncher')) {
			result.launch_method = 'command'
			
			result.command_launch_command = launcher.command ?: ''
			
		} else if (isInstanceOf(launcher, 'hudson.os.windows.ManagedWindowsServiceLauncher')) {
			result.launch_method = 'wmi'
			result.wmi_host = launcher.@host ?: ''
			result.wmi_admin_username = launcher.@userName ?: ''
			result.wmi_admin_password = launcher.@password?.plainText ?: ''
			result.wmi_java_path = launcher.@javaPath ?: ''
			result.wmi_jvm_options = launcher.@vmargs ?: ''
			
			account = launcher.account
			
			if (isInstanceOf(account, 'hudson.os.windows.ManagedWindowsServiceAccount$$Administrator')) {
				result.wmi_service_run_as = 'administrator'
				
			} else if (isInstanceOf(account, 'hudson.os.windows.ManagedWindowsServiceAccount$$AnotherUser')) {
				result.wmi_service_run_as = 'user'
				result.wmi_service_username = account.@userName ?: ''
				result.wmi_service_password = account.@password?.plainText ?: ''
				
			} else if (isInstanceOf(account, 'hudson.os.windows.ManagedWindowsServiceAccount$$LocalSystem')) {
				result.wmi_service_run_as = 'local_system'
				
			} else {
				throw new Exception("Unknown windows account type: " + account.getClass())
			}
			
		} else if (isInstanceOf(launcher, 'hudson.plugins.sshslaves.SSHLauncher')) {
			result.launch_method = 'ssh'
			result.ssh_host = launcher.host ?: ''
			result.ssh_port = launcher.port
			result.ssh_credentials_id = launcher.credentialsId ?: ''
			
			verificationStrategy = launcher.sshHostKeyVerificationStrategy
			if (isInstanceOf(verificationStrategy, 'hudson.plugins.sshslaves.verifiers.KnownHostsFileKeyVerificationStrategy')) {
				result.ssh_host_verification = 'known_hosts'
				
			} else if (isInstanceOf(verificationStrategy, 'hudson.plugins.sshslaves.verifiers.ManuallyProvidedKeyVerificationStrategy')) {
				result.ssh_host_verification = 'key'
				result.ssh_host_key = verificationStrategy.key
				
			} else if (isInstanceOf(verificationStrategy, 'hudson.plugins.sshslaves.verifiers.ManuallyTrustedKeyVerificationStrategy')) {
				result.ssh_host_verification = 'manually_trusted'
				result.ssh_host_manually_trusted_require_initial_verification = verificationStrategy.requireInitialManualTrust
				
			} else if (isInstanceOf(verificationStrategy, 'hudson.plugins.sshslaves.verifiers.NonVerifyingKeyVerificationStrategy')) {
				result.ssh_host_verification = 'none'
				
			} else {
				throw new Exception("Unknown ssh host key verification strategy type: " + account.getClass())
			}
			
			result.ssh_java_path = launcher.@javaPath ?: ''
			result.ssh_jvm_options = launcher.jvmOptions ?: ''
			result.ssh_command_prefix = launcher.prefixStartSlaveCmd ?: ''
			result.ssh_command_suffix = launcher.suffixStartSlaveCmd ?: ''
			result.ssh_connection_timeout = launcher.launchTimeoutSeconds
			result.ssh_retries = launcher.maxNumRetries
			result.ssh_wait_between_retries = launcher.retryWaitTime
			result.ssh_tcp_no_delay = launcher.tcpNoDelay
			result.ssh_workdir = launcher.workDir ?: ''
			
		} else {
			throw new Exception("Unknown launcher type: " + launcher.getClass())
		}
		
		if (node.retentionStrategy instanceof RetentionStrategy.Always) {
			result.availability = 'always'
			
		} else if (node.retentionStrategy instanceof RetentionStrategy.Demand) {
			rsd = (RetentionStrategy.Demand) node.retentionStrategy
			
			result.availability = 'on_demand'
			result.on_demand_in_demand_delay = rsd.inDemandDelay
			result.on_demand_idle_delay = rsd.idleDelay

		} else {
			throw new Exception("Unknown retention strategy type: " + node.retentionStrategy.getClass())
		}
	}
	
	return result;
}


def createNodeObject() {
	launcher = createLauncher()
	mode = createMode()
	retentionStrategy = createRetentionStrategy()

	node = new DumbSlave(args.name, args.root_dir.val, launcher)
	node.nodeDescription = args.description.val
	node.numExecutors = args.executors.val
	node.labelString = args.labels.val
	node.mode = mode
	node.retentionStrategy = retentionStrategy

	return node
}


def createLauncher() {
	switch (args.launch_method.val) {
		case 'jnlp':
			return createJnlpLauncher()
		case 'command':
			return createCommandLauncher()
		case 'wmi':
			return createWmiLauncher()
		case 'ssh':
			return createSshLauncher()
		default:
			throw new Exception("Unknown launch_method: " + args.launch_method.val)
	}
}


def createRetentionStrategy() {
	switch (args.availability.val) {
		case 'always':
			return new RetentionStrategy.Always()
		case 'on_demand':
			return new RetentionStrategy.Demand(args.on_demand_in_demand_delay.val, args.on_demand_idle_delay.val)
		default:
			throw new Exception("Unknown availability: " + args.availability.val)
	}
}


def createMode() {
	switch(args.usage.val) {
		case 'exclusive':
			return Node.Mode.EXCLUSIVE 
		case 'normal':
			return Node.Mode.NORMAL
		default:
			throw new Exception("Unknown usage: " + args.usage.val)
	}
}


def createJnlpLauncher() {
	result = new JNLPLauncher(args.jnlp_tunnel.val, args.jnlp_jvm_options.val)
	
	result.workDirSettings = new RemotingWorkDirSettings(
		!args.jnlp_workdir_enabled.val, 
		args.jnlp_workdir_path.val,
		args.jnlp_internal_dir.val,
		args.jnlp_fail_if_workspace_missing.val
	)
	
	return result
}


def createCommandLauncher() {
	try {
		cls = Class.forName('hudson.slaves.CommandLauncher')
		ctor = cls.getConstructor(String.class)
		return ctor.newInstance(args.command_launch_command.val)
		
	} catch (ClassNotFoundException e) {
		throw new Exception("You must install Command Agent Launcher plugin to be able to use launch_method='command'")
	}
}


def createWmiLauncher() {
	try {
		switch(args.wmi_service_run_as.val) {
			case 'administrator':
				cls = Class.forName('hudson.os.windows.ManagedWindowsServiceAccount$$Administrator')
				ctor = cls.getConstructor()
				account = ctor.newInstance()
				break
			
			case 'user':
				cls = Class.forName('hudson.os.windows.ManagedWindowsServiceAccount$$AnotherUser')
				ctor = cls.getConstructor(String.class, Secret.class)
				account = ctor.newInstance(args.wmi_service_username.val, Secret.fromString(args.wmi_service_password.val))
				break
			
			case 'local_system':
				cls = Class.forName('hudson.os.windows.ManagedWindowsServiceAccount$$LocalSystem')
				ctor = cls.getConstructor()
				account = ctor.newInstance()
				break
			
			default:
				throw new Exception("Unknown wmi_service_run_as: " + args.wmi_service_run_as.val)
		}
		
		cls = Class.forName('hudson.os.windows.ManagedWindowsServiceLauncher')
		ctor = cls.getConstructor(String.class, String.class, String.class, Class.forName('hudson.os.windows.ManagedWindowsServiceAccount'),
								  String.class, String.class)
		return ctor.newInstance(args.wmi_admin_username.val, args.wmi_admin_password.val, args.wmi_host.val, account,
								args.wmi_jvm_options.val, args.wmi_java_path.val)
		
	} catch (ClassNotFoundException e) {
		throw new Exception("You must install WMI Windows Agents plugin to be able to use launch_method='wmi'")
	}
}


def createSshLauncher() {
	try {
		switch(args.ssh_host_verification.val) {
			case 'known_hosts':
				cls = Class.forName('hudson.plugins.sshslaves.verifiers.KnownHostsFileKeyVerificationStrategy')
				ctor = cls.getConstructor()
				verificationStrategy = ctor.newInstance()
				break
			
			case 'key':
				cls = Class.forName('hudson.plugins.sshslaves.verifiers.ManuallyProvidedKeyVerificationStrategy')
				ctor = cls.getConstructor(String.class)
				verificationStrategy = ctor.newInstance(args.ssh_host_key.val)
				break
			
			case 'manually_trusted':
				cls = Class.forName('hudson.plugins.sshslaves.verifiers.ManuallyTrustedKeyVerificationStrategy')
				ctor = cls.getConstructor(boolean.class)
				verificationStrategy = ctor.newInstance(args.ssh_host_manually_trusted_require_initial_verification.val)
				break
			
			case 'none':
				cls = Class.forName('hudson.plugins.sshslaves.verifiers.NonVerifyingKeyVerificationStrategy')
				ctor = cls.getConstructor()
				verificationStrategy = ctor.newInstance()
				break
			
			default:
				throw new Exception("Unknown ssh_host_verification: " + args.ssh_host_verification.val)
		}
		
		cls = Class.forName('hudson.plugins.sshslaves.SSHLauncher')
		ctor = cls.getConstructor(String.class, int.class, String.class, String.class, String.class, 
								  String.class, String.class, Integer.class, Integer.class, 
								  Integer.class, Class.forName('hudson.plugins.sshslaves.verifiers.SshHostKeyVerificationStrategy'))
		result = ctor.newInstance(args.ssh_host.val, args.ssh_port.val, args.ssh_credentials_id.val, args.ssh_jvm_options.val, args.ssh_java_path.val,
								  args.ssh_command_prefix.val, args.ssh_command_suffix.val, args.ssh_connection_timeout.val, args.ssh_retries.val, 
								  args.ssh_wait_between_retries.val, verificationStrategy)

		result.tcpNoDelay = args.ssh_tcp_no_delay.val
		result.workDir = args.ssh_workdir.val
		
		return result
		
	} catch (ClassNotFoundException e) {
		throw new Exception("You must install SSH Slaves plugin to be able to use launch_method='ssh'")
	}
}


def applyState() {
	node = getNode(args.name)
	current = getCurrentState(node)
	
	if (args.state == 'present')
		return false
	
	if (current.state == 'online') {
		switch (args.state) {
			case 'online':
				return false

			case 'offline':
				makeTemporarilyOffline(node)
				return true

			case 'connected':
				throw new Exception("A node with launch_method='" + current.launch_method + "' can not actively be connected or disconnected")

			case 'disconnected':
				throw new Exception("A node with launch_method='" + current.launch_method + "' can not actively be connected or disconnected ")

			default:
				throw new Exception("Invalid state: " + current.state + " / " + args.state)
		}
		
	} else if (current.state == 'offline') {
		computer = node.computer
		
		switch (args.state) {
			case 'online':
				stopTemporarilyOffline(node)
				return true

			case 'offline':
				if (current.offline_reason != args.offline_reason) {
					makeTemporarilyOffline(node)
					return true
				}
				return false

			case 'connected':
				if (!computer.launchSupported)
					throw new Exception("A node with launch_method='" + current.launch_method + "' can not actively be connected or disconnected ")

				connect(node)
				return true

			case 'disconnected':
				if (!computer.launchSupported)
					throw new Exception("A node with launch_method='" + current.launch_method + "' can not actively be connected or disconnected ")

				disconnect(node)
				return true

			default:
				throw new Exception("Invalid state: " + current.state + " / " + args.state)
		}
		
	} else if (current.state == 'connected') {
		switch (args.state) {
			case 'online':
				return false

			case 'offline':
				makeTemporarilyOffline(node)
				return true

			case 'connected':
				return false

			case 'disconnected':
				disconnect(node)
				return true

			default:
				throw new Exception("Invalid state: " + current.state + " / " + args.state)
		}
		
	} else if (current.state == 'disconnected') {
		switch (args.state) {
			case 'online':
				return false

			case 'offline':
				makeTemporarilyOffline(node)
				return true

			case 'connected':
				connect(node)
				return true

			case 'disconnected':
				if (current.disconnected_reason != args.disconnected_reason) {
					disconnect(node)
					return true
				}
				return false

			default:
				throw new Exception("Invalid state: " + current.state + " / " + args.state)
		}
	}
	
	throw new Exception("Invalid state: " + current.state + " / " + args.state)
}

def connect(node, reason = null) {
	computer = node.computer

	if (computer.temporarilyOffline)
		stopTemporarilyOffline(node)

	future = computer.connect(true)
	future.get()
}

def createOfflineCause(reason) {
	return new OfflineCause.UserCause((User) User.current(), reason == '' ? null : reason)	
}

def disconnect(node) {
	computer = node.computer
	
	if (args.wait_jobs_finish && (computer.online || !computer.idle))
		makeTemporarilyOffline(node, 'Slave is disconnecting')
	
	future = computer.disconnect(createOfflineCause(args.disconnected_reason))
	future.get()
	
	if (computer.temporarilyOffline) {
		stopTemporarilyOffline(node)

		if (args.disconnected_reason != '')
			// Do it again to set reason
			computer.disconnect(createOfflineCause(args.disconnected_reason))
	}
}

def makeTemporarilyOffline(node, reason = null) {
	computer = node.computer
	
	computer.setTemporarilyOffline(true, createOfflineCause(reason ?: args.offline_reason))
	
	if (args.wait_jobs_finish) {
		waits = 0
		
		while (!computer.idle) {
			sleep(1000)
			
			waits++;
			
			if (args.wait_jobs_finish_max_time > 0 && waits > args.wait_jobs_finish_max_time)
				break;
		}
	}
}

def stopTemporarilyOffline(node) {
	computer = node.computer
	
	computer.setTemporarilyOffline(false, null)
}


def getNode(name) {
	for (node in Jenkins.instance.nodes)
		if (node.nodeName == name)
			return node

	return null
}


def to_bool_arg(val, defval = null) {
	if (val == null || val == '')
		return [set: false, val: defval]
	else
		return [set: true, val: val.toBoolean()]
}

def to_int_arg(val, defval = null) {
	if (val == null || val == '')
		return [set: false, val: defval]
	else
		return [set: true, val: val.toInteger()]
}

def to_choice_arg(val, defval = null) {
	if (val == null || val == '')
		return [set: false, val: defval]
	else
		return [set: true, val: val.toString()]
}

def to_string_arg(val, defval = '') {
	if (val == null)
		return [set: false, val: defval]
	else
		return [set: true, val: val.toString()]
}


def arg_different(arg, val) {
	return arg.set && arg.val != val
}


def arg_replaceDefault(arg, val) {
	if (!arg.set)
		arg.val = val
}


def isInstanceOf(obj, name) {
	try {
		return obj.getClass() == Class.forName(name)
		
	} catch(ClassNotFoundException e) {
		return false
	}
}


result = process()

println new JsonBuilder(result).toPrettyString()

""").substitute(args_escaped)

    result = dict(
        changed=False
    )

    if module.check_mode:
        module.exit_json(**result)

    server = get_jenkins(module)

    try:
        content = server.run_script(script)
    except Exception as e:
        module.fail_json(msg='Error while talking to jenkins server: %s' % to_native(e), exception=traceback.format_exc())

    result = json.loads(content)

    module.exit_json(**result)


def get_jenkins(module):
    url = module.params['server_url']
    user = module.params['server_username']
    password = module.params['server_password']
    token = module.params['server_token']
    timeout = module.params['server_timeout']
    validate_certs = module.params['server_validate_certs']

    try:
        if (user and password):
            result = jenkins.Jenkins(url, user, password, timeout=timeout)
        elif (user and token):
            result = jenkins.Jenkins(url, user, token, timeout=timeout)
        elif (user and not (password or token)):
            result = jenkins.Jenkins(url, user, timeout=timeout)
        else:
            result = jenkins.Jenkins(url, timeout=timeout)

        result._session.verify = validate_certs

        return result
    except Exception as e:
        module.fail_json(msg='Unable to connect to Jenkins server, %s' % to_native(e), exception=traceback.format_exc())



def main():
    run_module()


if __name__ == '__main__':
    main()
