# DNSentinel

A comprehensive solution for DNS management with support for dynamic IPs.

## Tech Stack

<div align="center">
    <img src="https://skillicons.dev/icons?i=python,flask,mysql,docker" alt="Tech Stack" />
</div>

## Features

- Connect with Cloudflare API / Google Domains API
- Dynamic DNS updates for changing IP addresses
- Program tasks for periodic updates
- Web dashboard for monitoring and configuration
- Logging and alerting
- Deployable as local service in your network

## Installation

```bash
git clone https://github.com/astronautmarkus/DNSentinel.git
cd DNSentinel
# Install dependencies
pip install -r requirements.txt
# Configure environment variables as needed
```

## Env example

```env
.env.example
```

Copy this file to `.env` and modify the values accordingly.

```bash
cp .env.example .env
nano .env
```

Edit as needed.


## Usage

```bash
python main.py
# or with Docker
docker-compose up
```

Access the dashboard at `http://127.0.0.1:5000` (development).

In development mode, access the dashboard at `0.0.0.0:5010`.

## License

Check <a href="LICENSE">LICENSE</a> for more information.

> Created with a lot of Monster Energy and a need that few understand. <a href="astronautmarkus.dev" target="_blank">astronautmarkus.dev</a>
