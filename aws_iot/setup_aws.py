"""Helper script to pre-create devices and policies in AWS IoT."""
import boto3
import json

from settings import PROFILE_NAME, THINGS, CERTIFICATE_CERT, CERTIFICATE_KEY

IOT_POLICY = {'Version': '2012-10-17',
              'Statement': [{'Effect': 'Allow',
                             'Action': ['iot:*'],
                             'Resource': ['*']},]}

session = boto3.session.Session(profile_name=PROFILE_NAME)
iot = session.client('iot')


def generate_cert(cert_file_name, private_key_filename):
    response = iot.create_keys_and_certificate(setAsActive=True)

    with open(cert_file_name, 'w') as f:
        f.write(response['certificatePem'])

    with open(private_key_filename, 'w') as f:
        f.write(response['keyPair']['PrivateKey'])

    return response['certificateArn']


def create_new_policy(policy_name):
    iot.create_policy(policyName=policy_name,
                      policyDocument=json.dumps(IOT_POLICY))


def attach_policy_to_cert(policy_name, cert_arn):
    iot.attach_principal_policy(policyName=policy_name, principal=cert_arn)


def create_new_thing(thing_name):
    iot.create_thing(thingName=thing_name)


def attach_thing_to_cert(thing_name, cert_arn):
    iot.attach_thing_principal(thingName=thing_name, principal=cert_arn)


if __name__ == "__main__":
    iot_cert_arn = generate_cert(CERTIFICATE_CERT, CERTIFICATE_KEY)
    iot_policy = create_new_policy("iot_policy")

    # Attach Policy to Cert
    attach_policy_to_cert(iot_policy, iot_cert_arn)

    for thing in THINGS:
        create_new_thing(thing.upper())
        # Attach thing to Cert
        attach_thing_to_cert(thing.upper(), iot_cert_arn)
