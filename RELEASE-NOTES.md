# Metrics Explorer release notes

## 1.0.0

First release. Metrics Explorer inspects the metrics in any Splunk metrics index, by name, without
writing SPL.

- **Find metrics:** filter metric names by pattern and index over a time range, with counts of the
  matching names, the hosts emitting them, and their sources (`service.name` or
  `k8s.deployment.name`).
- **Topology:** for a metric, every combination of dimensions it carries, with the sources, hosts
  and indexes that emit each one.
- **Basic criteria:** click a metric, source, host, index or dimension in Topology to add it to the
  criteria; click a criteria row to remove it.
- **Charts:** sample count per minute, and the latest value of each selected metric split by the
  fields its criteria name.
- **SPL:** the `mstats` search the criteria build, in either `latest(_value) BY metric_name` or
  `latest(<metric_name>)` syntax, with an **Open in Search** button.
- **Recent samples:** raw samples from `mpreview`, capped by a sample limit, each linking to a
  search for that sample.
