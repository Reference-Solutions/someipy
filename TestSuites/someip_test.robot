*** Settings ***
Library           ./TestKeywords/someip_library.py    # Custom Python library to use the someipy functionalities
Library           BuiltIn
Library           Collections

*** Variables ***
${SOMEIP_SERVER_IP}      192.168.10.30  # The IP address of the SOME/IP server
${SOMEIP_SERVER_PORT}    30490          # The port on which the server is listening for UDP events
${SOMEIP_MESSAGE}        b'\x12\x34\x56\x78\x9A\xBC\xDE\xF0'  # Example SOME/IP message to send
${RESPONSE_TIMEOUT}      5                # Timeout for receiving response

*** Test Cases ***

Validate SOME/IP Connection
    [Documentation]    Validates the UDP connection to the SOME/IP server.
    SomeIP Connection Validation    ${SOMEIP_SERVER_IP}    ${SOMEIP_SERVER_PORT}

Send SOME/IP Message
    [Documentation]    Sends a SOME/IP message to the server and validates the sending process.
    Set Server Info    ${SOMEIP_SERVER_IP}    ${SOMEIP_SERVER_PORT}
    SomeIP Send Message    ${SOMEIP_MESSAGE}

Receive SOME/IP Response
    [Documentation]    Receives a SOME/IP response after sending a message.
    ${response}    SomeIP Receive Response    timeout=${RESPONSE_TIMEOUT}
    Log    ${response}

Receive and Log SOME/IP Events
    [Documentation]    Receives UDP SOME/IP events and logs them as test data.
    ${events}          SomeIP Receive Events UDP    ${SOMEIP_SERVER_IP}    ${SOMEIP_SERVER_PORT}
    Log List           ${events}    level=INFO
