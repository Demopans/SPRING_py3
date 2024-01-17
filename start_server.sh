#!/bin/bash

function print_help() {
    echo "Usage: ./start_server.sh [OPTIONS]"
    echo "Start the Flask server with optional debugging and port specification."
    echo ""
    echo "Options:"
    echo "  -d, --debug      Run the server in debug mode."
    echo "  -p, --port       Set the port of the server. Requires a number as an argument."
    echo "  -h, --help       Display this help and exit."
    echo ""
    echo "Examples:"
    echo "  ./start_server.sh -d          Start the server in debug mode."
    echo "  ./start_server.sh -p 8080     Start the server on port 8080."
    echo "  ./start_server.sh -d -p 8080  Start the server in debug mode on port 8080."
}


command="python3 flask_server.py"
debug_mode=""
port=""

while [[ $# -gt 0 ]]
do
    key="$1"

    case $key in
        -d|--debug)
            debug_mode=" --debug"
            shift
            ;;
        -p|--port)
            port=" --port $2"
            shift
            shift
            ;;
        -h|--help)
            print_help
            exit 0
            ;;
        *)
            # unknown option
            ;;
    esac
done

command="$command$debug_mode$port"
echo "Running command: $command"
eval $command
