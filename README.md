# AI-Network-Troubleshooting-PoC

Use the provided Makefile to manage Docker services for grafana, influxdb, and telegraf. Commands follow the pattern make `<operation>-<service>`. For example:

- **Build and run service**: `make build-<service>` (e.g., `make build-grafana`)
- **Start service**: `make run-<service>` (e.g., `make run-influxdb`)
- **View service logs**: `make logs-<service>` (e.g., `make logs-telegraf`)
- **Access service CLI**: `make cli-<service>` (e.g., `make cli-grafana`)
- **Build and run all services**: `make all`

Replace `<service>` with the service name (grafana, influxdb, telegraf).

### webex details

Get room id
<https://developer.webex.com/docs/api/v1/rooms/list-rooms>
