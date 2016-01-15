"""Helper script to pre-create devices and policies in AWS IoT.

For more information, see Secure Communication Between a Device and AWS IoT: http://docs.aws.amazon.com/iot/latest/developerguide/secure-communication.html
"""
import boto3
import json
import os

from settings import PROFILE_NAME, THINGS, CERTIFICATE_CERT, CERTIFICATE_KEY

# Permissions to assign to an AWS IoT Policy, this controls what operations the certificate owner can perform.
# This policy allows all AWS IoT operations on all resources.
IOT_POLICY = {'Version': '2012-10-17', 
              'Statement': [{'Effect': 'Allow', 
                             'Action': ['iot:*'], 
                             'Resource': ['*']}, ]}


def generate_and_save_cert(iot, cert_filename, private_key_filename):
    """Create, activate and save an AWS IoT certificate.

    :param iot: IoT session client
    :param str cert_filename: Name of the certificate file
    :param str private_key_filename: Name of the certificate's private key file
    """
    response = iot.create_keys_and_certificate(setAsActive=True)

    with open(cert_filename, 'w') as f:
        f.write(response['certificatePem'])

    with open(private_key_filename, 'w') as f:
        f.write(response['keyPair']['PrivateKey'])

    return response['certificateArn']


if __name__ == "__main__":
    session = boto3.session.Session(profile_name=PROFILE_NAME)
    iot = session.client('iot')

    # Get absolute filepaths
    certificate_cert = os.path.join(os.path.dirname(os.path.abspath(__file__)), CERTIFICATE_CERT)
    certificate_key = os.path.join(os.path.dirname(os.path.abspath(__file__)), CERTIFICATE_KEY)
    # Generate an X.509 certificate in AWS IoT
    iot_cert_arn = generate_and_save_cert(iot, certificate_cert, certificate_key)

    policy_name = "iot_policy"
    # The policy defines what operations the certificate owner can perform.
    iot.create_policy(policyName=policy_name, policyDocument=json.dumps(IOT_POLICY))

    iot.attach_principal_policy(policyName=policy_name, principal=iot_cert_arn)

    for thing in THINGS:
        # Create a Thing resource for each SN 171
        uppercase_name = thing.upper()
        iot.create_thing(thingName=uppercase_name)
        iot.attach_thing_principal(thingName=uppercase_name, principal=iot_cert_arn)
