# ZKTeco C3 for Home Assistant

Custom integration for ZKTeco C3 access control panels.

## Features

- Creates Home Assistant lock entities for ZKTeco C3 doors
- Supports 1 to 4 doors
- Configurable IP, port, communication password and open duration
- Local control over TCP port 4370

## Installation with HACS

1. Open HACS
2. Go to Custom repositories
3. Add this repository URL
4. Select category: Integration
5. Install
6. Restart Home Assistant
7. Go to Settings → Devices & Services → Add Integration
8. Search for ZKTeco C3

## Configuration

You will need:

- Controller IP
- TCP port, usually 4370
- Communication password
- Door count
- Door names

## Notes

Do not expose the ZKTeco C3 controller or this integration to the internet.
