#!/usr/bin/env python3
# Example script for internal use in PoC, do not use it for production systems

import sys, yaml
from winrm.protocol import Protocol
from base64 import b64encode

data = yaml.safe_load(sys.stdin)

ips = data['staticIps']
username = data['vmIdentity']
password = data['vmPassword']
command = data['powerShellCommand']
arguments = data.get('powerShellArguments', '')

encoded_ps = b64encode(command.encode('utf_16_le')).decode('ascii')

powershell_command = 'powershell {0} -encodedcommand {1}'.format(arguments, encoded_ps)

results = {}
exit_code = 0

for ip in ips:
    p = Protocol(
        endpoint='https://{0}:5986/wsman'.format(ip),
        transport='ntlm', # the only authentication we support at the moment
        username=r'{0}\{1}'.format(ips, username),
        password=password,
        server_cert_validation='ignore') # there will be self-signed certificates only, so let's ignore validation

    shell_id = p.open_shell()
    command_id = p.run_command(shell_id, powershell_command)
    std_out, std_err, status_code = p.get_command_output(shell_id, command_id)

    p.cleanup_command(shell_id, command_id)
    p.close_shell(shell_id)
    results[ip] = {"result": std_out.decode('ascii'), "error": std_err.decode('ascii')}
    # some command returned an error and this is first error
    # save it as exit code to let user know that there is some problem
    if status_code > 0 and exit_code == 0:
        exit_code = status_code

yaml.safe_dump({"results": results}, sys.stdout)
sys.exit(exit_code)
