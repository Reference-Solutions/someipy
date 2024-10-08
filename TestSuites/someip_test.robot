*** Settings ***
Library           ./TestKeywords/someip_library.py    # Custom Python library to use the someipy functionalities
Library           BuiltIn
Library           Collections

*** Variables ***
${SOMEIP_SERVER_IP}      192.168.10.30  # The IP address of the SOME/IP server
${SOMEIP_SERVER_PORT}    30490          # The port on which the server is listening for UDP events

*** Test Cases ***

Validate SOME/IP Connection
    [Documentation]    Validates the UDP connection to the SOME/IP server.
    SomeIP Connection Validation    ${SOMEIP_SERVER_IP}    ${SOMEIP_SERVER_PORT}

Receive and Log SOME/IP Events
    [Documentation]    Receives UDP SOME/IP events and logs them as test data.
    ${events}          SomeIP Receive Events UDP    ${SOMEIP_SERVER_IP}    ${SOMEIP_SERVER_PORT}
    Log List           ${events}    level=INFO
