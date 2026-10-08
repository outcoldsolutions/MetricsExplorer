<img src="docs/Logo.png" alt="Metrics Explorer project icon" height="300">

# Metrics Explorer

Rich telemetry is key to operational observability, but having too many metrics makes finding the right one a hassle.

Metrics Explorer makes that easier. In a Splunk dashboard, it helps you:

1. find available metrics,
2. filter metrics to what you want,
3. see the dimensions and sources for each metric, and
4. build a `mstats` search.

Once metrics and dimensions are selected, the dashboard's output is a base search that can be used directly in Search or refined with a tool like the [Outcold Solutions AI Agent](https://www.outcoldsolutions.com/docs/ai-agent/).

The app collects no data and stores nothing. Every panel is a search over metrics you already index.

## Requirements

- Splunk Enterprise or Splunk Cloud Platform 10.0 or later.
- Read access to the metrics indexes you want to explore.

## Installation

Install from Splunkbase, or download `metricsexplorer-<version>.tgz` from the
[GitHub releases](https://github.com/outcoldsolutions/MetricsExplorer/releases) and install it with
**Apps > Manage Apps > Install app from file**. The "Source code" archives GitHub attaches to each
release are not installable apps.

## Quick start

1. Install the app and open **Metrics Explorer**.
2. Enter a metric name (wildcards allowed), an index (wildcards allowed) and a time range, then select **Submit**.
3. Click a row in **Metric names** to show that metric's **Topology**.
4. Click a metric, source, host, index or dimension cell in **Topology** to add it to **Basic criteria**. The charts, the **SPL** panel and **Open in Search** follow the criteria.
5. Open the **Recent samples** tab for the raw samples behind a metric.

## Permissions

The app's objects are readable by every role and editable by `admin`, `sc_admin` and `power`.

## Support

Contact Scott Raiford on the [Splunk user Slack](https://splk.it/slack), or open a
[GitHub issue](https://github.com/outcoldsolutions/MetricsExplorer/issues).

## License

This software is released under the MIT license.
See `LICENSE` for details.

All trademarks are property of their respective owners.

## About the project

<img src="docs/outcold.png" alt="Outcold Solutions logo" height="150">

This project began as an internal tool used by [Outcold Solutions](https://outcoldsolutions.com/) to identify useful metrics in new data sets. It's now released to the Splunk community as open-source software to help others in getting useful insight from their metrics.

Contributions are welcome, as described in `CONTRIBUTING`.
