# Balena Grafana Application

This is a Grafana monitoring dashboard application for balena devices.

## Features

- Grafana dashboard with admin interface
- Pre-configured with basic datasources
- Persistent data storage
- Health monitoring
- Easy deployment to balena devices

## Configuration

- Default admin username: `admin`
- Default admin password: `admin` (change this in production!)
- Web interface available on port 3000

## Deployment

1. Make sure you have balena CLI installed
2. Login to your balena account: `balena login`
3. Create or select your application
4. Push to balena: `balena push <app-name>`

## Environment Variables

You can configure the following environment variables in balena dashboard:

- `GF_SECURITY_ADMIN_PASSWORD`: Admin password (default: admin)
- `GF_USERS_ALLOW_SIGN_UP`: Allow user signup (default: false)
- `GF_SECURITY_ALLOW_EMBEDDING`: Allow embedding (default: true)

## Usage

1. After deployment, access Grafana at `http://<device-ip>:3000`
2. Login with admin/admin credentials
3. Start creating dashboards and adding data sources

## Security Notes

- Change the default admin password before production use
- Consider using environment variables for sensitive configuration
- Review security settings in grafana.ini as needed