# RepoOGN-WEB-files

# RepoOGN-WEB-files

A web-based monitoring and statistics platform for the **Open Gliding Network (OGN)**. This application provides real-time status updates, receiver information, and flight statistics for OGN receiver stations globally.

## Overview

This repository contains the web assets and backend CGI scripts used to serve the OGN monitoring interface. It allows users to track the status of receiver stations, view connectivity details, and access network-wide statistics.

## Architecture

The application follows a classic CGI (Common Gateway Interface) architecture:

- **Frontend**: Static HTML files (`.html`) located in the root directory serve as the primary user interfaces. These files interact with backend scripts to display dynamic content.
- **Backend**: A collection of Python (`.py`) and PHP (`.php`) scripts located in the `CGI-BIN` directory. These scripts handle data processing, API communication, and database queries.
- **Data Storage**: A local SQLite database is used to store and manage station and receiver information.
- **External Integrations**:
    - **Receiver Data**: Fetches real-time receiver lists from `http://ogn.peanutpod.de/receivers.json`.
    - **APRS Status**: Monitors APRS server connectivity via `glidernet.org` (e.g., `glidern1.glidernet.org`).

## Directory Structure

```text
RepoOGN-WEB-files/
├── CGI-BIN/                # Backend CGI scripts (Python & PHP)
│   ├── gif/                # Icons and images for CGI outputs
│   ├── config.py.template  # Template for Python configuration
│   ├── dtfuncs.py          # Date/time utility functions
│   ├── gbydate.py/php      # Scripts for date-based queries
│   ├── glive.py/php        # Live status scripts
│   ├── gstats.py/php       # Statistics scripts
│   ├── ksta.py             # Station name mapping utilities
│   └── parserfuncs.py      # Data parsing utilities
├── gif/                    # Images used by main HTML pages
├── favicon.ico             # Site favicon
├── gbydate.html            # Date-based query interface
├── glive.html              # Live status dashboard
├── gmet.html               # Metrics/Statistics page
├── gstats.html             # General statistics page
├── gwx.html                # Weather/Network status page
├── main                    # Main entry point (likely a redirect or index)
├── package.json            # Project dependencies
└── README.md               # Project documentation
```

## Key Features & Pages

| Page | Description |
|------|-------------|
| `glive.html` | **Live Status**: Real-time dashboard showing the current status of OGN receiver stations, including connectivity and last heartbeat. |
| `gstats.html` | **Statistics**: Provides aggregated network statistics and data insights. |
| `gmet.html` | **Metrics**: Detailed metrics and performance data for the network. |
| `gwx.html` | **Network Status**: Overview of network health and connectivity. |
| `ognChile.html` / `ognSpain.html` | **Regional Views**: Specialized interfaces for monitoring specific geographic regions. |

## Technical Details

### Backend Implementation
The backend relies heavily on Python CGI scripts. For example, `gstats.py` performs the following:
1. Fetches JSON data from external OGN/APRS sources.
2. Connects to a local SQLite database to retrieve station metadata.
3. Processes and formats the combined data into HTML tables for web display.

### Database Schema (Inferred)
The system utilizes a SQLite database with a `RECEIVERS` table containing:
- `idrec`: Unique identifier for the receiver.
- `descri`: Description of the station.
- Other metadata used for filtering and display.

## Deployment & Maintenance

The repository includes scripts for managing utility functions and deployment:
- `sscommit.sh`: A deployment script that synchronizes shared utility functions (from a central `/nfs/OGN/src/funcs/` location) into the `CGI-BIN` directory before committing changes.
- `sslink.sh`: Creates symbolic links to shared utility functions, allowing for easier maintenance of common code across different parts of the OGN infrastructure.

---
*This documentation was generated to provide an overview of the RepoOGN-WEB-files repository.*
