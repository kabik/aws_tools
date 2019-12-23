import sys
import json
import subprocess
import shlex

def exec(command):
    print(command)
    print(shlex.split(command))
    process = subprocess.Popen(shlex.split(command), stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    out, err = process.communicate()
    out = out.decode('utf-8')

    if err:
        print(err)

    return out


def main():
    COMMAND_FORMAT = 'aws sts --profile {} get-session-token --serial-number arn:aws:iam::{}:mfa/{} --token-code {}'
    PROFILE = ''
    ACCOUNT = ''
    MAIL = ''

    print('MFA token > ', end='')
    token = input()

    command = COMMAND_FORMAT.format(PROFILE, ACCOUNT, MAIL, token)
    cred_str = exec(command)
    cred_json = json.loads(cred_str)

    command_access_key_id = 'export AWS_ACCESS_KEY_ID={}'.format(cred_json['Credentials']['AccessKeyId'])
    command_secret_access_key = 'export AWS_SECRET_ACCESS_KEY={}'.format(cred_json['Credentials']['SecretAccessKey'])
    command_session_token = 'export AWS_SESSION_TOKEN={}'.format(cred_json['Credentials']['SessionToken'])

    print(command_access_key_id)
    print(command_secret_access_key)
    print(command_session_token)


if __name__ == "__main__":
    main()
