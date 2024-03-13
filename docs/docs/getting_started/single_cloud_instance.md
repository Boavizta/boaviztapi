# Getting started (5 min)

This page presents basic queries that can be used to retrieve impacts of cloud instance (AWS use case).

You use `curl` in command line to query Boavizta demo (public) API.

💡 _You can format the results by using jq (`curl -X 'GET' '{{ endpoint }}/v1/cloud/aws?instance_type=a1.xlarge' | jq`)_

## Get available cloud instances

This query returns the list of available aws instances

Query:

```bash
# Query the available aws instances
curl -X 'GET' \
  '{{ endpoint }}/v1/cloud/instance/all_instances?provider=aws' \
  -H 'accept: application/json'
```


<details>
	<summary>Results</summary>

```json
[
    "a1.medium",
    "a1.large",
    "a1.xlarge",
    "a1.2xlarge",
    "a1.4xlarge",
    "a1.metal",
    "c1.medium",
    "c1.xlarge",
    "c3.large",
    "c3.xlarge",
    "c3.2xlarge",
    "c3.4xlarge",
    "c3.8xlarge",
    "c4.large",
    "c4.large.elasticsearch",
    "c4.xlarge",
    "c4.xlarge.elasticsearch",
    "c4.2xlarge",
    "c4.2xlarge.elasticsearch",
    "c4.4xlarge",
    "c4.4xlarge.elasticsearch",
    "c4.8xlarge",
    "c4.8xlarge.elasticsearch",
    "c5.large",
    "c5.large.elasticsearch",
    "c5.xlarge",
    "c5.xlarge.elasticsearch",
    "c5.2xlarge",
    "c5.2xlarge.elasticsearch",
    "c5.4xlarge",
    "c5.4xlarge.elasticsearch",
    "c5.9xlarge",
    "c5.9xlarge.elasticsearch",
    "c5.12xlarge",
    "c5.18xlarge",
    "c5.18xlarge.elasticsearch",
    "c5.24xlarge",
    "c5.metal",
    "c5a.large",
    "c5a.xlarge",
    "c5a.2xlarge",
    "c5a.4xlarge",
    "c5a.8xlarge",
    "c5a.12xlarge",
    "c5a.16xlarge",
    "c5a.24xlarge",
    "c5ad.large",
    "c5ad.xlarge",
    "c5ad.2xlarge",
    "c5ad.4xlarge",
    "c5ad.8xlarge",
    "c5ad.12xlarge",
    "c5ad.16xlarge",
    "c5ad.24xlarge",
    "c5d.large",
    "c5d.xlarge",
    "c5d.2xlarge",
    "c5d.4xlarge",
    "c5d.9xlarge",
    "c5d.12xlarge",
    "c5d.18xlarge",
    "c5d.24xlarge",
    "c5d.metal",
    "c5n.large",
    "c5n.xlarge",
    "c5n.2xlarge",
    "c5n.4xlarge",
    "c5n.9xlarge",
    "c5n.18xlarge",
    "c5n.metal",
    "c6a.large",
    "c6a.xlarge",
    "c6a.2xlarge",
    "c6a.4xlarge",
    "c6a.8xlarge",
    "c6a.12xlarge",
    "c6a.16xlarge",
    "c6a.24xlarge",
    "c6a.32xlarge",
    "c6a.48xlarge",
    "c6a.metal",
    "c6g.medium",
    "c6g.large",
    "c6g.large.elasticsearch",
    "c6g.xlarge",
    "c6g.xlarge.elasticsearch",
    "c6g.2xlarge",
    "c6g.2xlarge.elasticsearch",
    "c6g.4xlarge",
    "c6g.4xlarge.elasticsearch",
    "c6g.8xlarge",
    "c6g.8xlarge.elasticsearch",
    "c6g.12xlarge",
    "c6g.12xlarge.elasticsearch",
    "c6g.16xlarge",
    "c6g.metal",
    "c6gd.medium",
    "c6gd.large",
    "c6gd.xlarge",
    "c6gd.2xlarge",
    "c6gd.4xlarge",
    "c6gd.8xlarge",
    "c6gd.12xlarge",
    "c6gd.16xlarge",
    "c6gd.metal",
    "c6gn.medium",
    "c6gn.large",
    "c6gn.xlarge",
    "c6gn.2xlarge",
    "c6gn.4xlarge",
    "c6gn.8xlarge",
    "c6gn.12xlarge",
    "c6gn.16xlarge",
    "c6i.large",
    "c6i.xlarge",
    "c6i.2xlarge",
    "c6i.4xlarge",
    "c6i.8xlarge",
    "c6i.12xlarge",
    "c6i.16xlarge",
    "c6i.24xlarge",
    "c6i.32xlarge",
    "c6i.metal",
    "c6id.large",
    "c6id.xlarge",
    "c6id.2xlarge",
    "c6id.4xlarge",
    "c6id.8xlarge",
    "c6id.12xlarge",
    "c6id.16xlarge",
    "c6id.24xlarge",
    "c6id.32xlarge",
    "c6id.metal",
    "c6in.large",
    "c6in.xlarge",
    "c6in.2xlarge",
    "c6in.4xlarge",
    "c6in.8xlarge",
    "c6in.12xlarge",
    "c6in.16xlarge",
    "c6in.24xlarge",
    "c6in.32xlarge",
    "c6in.metal",
    "c7a.medium",
    "c7a.large",
    "c7a.xlarge",
    "c7a.2xlarge",
    "c7a.4xlarge",
    "c7a.8xlarge",
    "c7a.12xlarge",
    "c7a.16xlarge",
    "c7a.24xlarge",
    "c7a.32xlarge",
    "c7a.48xlarge",
    "c7a.metal-48xl",
    "c7g.medium",
    "c7g.large",
    "c7g.xlarge",
    "c7g.2xlarge",
    "c7g.4xlarge",
    "c7g.8xlarge",
    "c7g.12xlarge",
    "c7g.16xlarge",
    "c7g.metal",
    "c7gd.medium",
    "c7gd.large",
    "c7gd.xlarge",
    "c7gd.2xlarge",
    "c7gd.4xlarge",
    "c7gd.8xlarge",
    "c7gd.12xlarge",
    "c7gd.16xlarge",
    "c7gn.medium",
    "c7gn.large",
    "c7gn.xlarge",
    "c7gn.2xlarge",
    "c7gn.4xlarge",
    "c7gn.8xlarge",
    "c7gn.12xlarge",
    "c7gn.16xlarge",
    "c7i.large",
    "c7i.xlarge",
    "c7i.2xlarge",
    "c7i.4xlarge",
    "c7i.8xlarge",
    "c7i.12xlarge",
    "c7i.16xlarge",
    "c7i.24xlarge",
    "c7i.48xlarge",
    "cc2.8xlarge",
    "cr1.8xlarge",
    "d2.xlarge",
    "d2.2xlarge",
    "d2.4xlarge",
    "d2.8xlarge",
    "d3.xlarge",
    "d3.2xlarge",
    "d3.4xlarge",
    "d3.8xlarge",
    "d3en.xlarge",
    "d3en.2xlarge",
    "d3en.4xlarge",
    "d3en.6xlarge",
    "d3en.8xlarge",
    "d3en.12xlarge",
    "dc2.large",
    "dc2.8xlarge",
    "dl1.24xlarge",
    "ds2.xlarge",
    "ds2.8xlarge",
    "f1.2xlarge",
    "f1.4xlarge",
    "f1.16xlarge",
    "g2.2xlarge",
    "g2.8xlarge",
    "g3.4xlarge",
    "g3.8xlarge",
    "g3.16xlarge",
    "g3s.xlarge",
    "g4ad.xlarge",
    "g4ad.2xlarge",
    "g4ad.4xlarge",
    "g4ad.8xlarge",
    "g4ad.16xlarge",
    "g4dn.xlarge",
    "g4dn.2xlarge",
    "g4dn.4xlarge",
    "g4dn.8xlarge",
    "g4dn.12xlarge",
    "g4dn.16xlarge",
    "g4dn.metal",
    "g5.xlarge",
    "g5.2xlarge",
    "g5.4xlarge",
    "g5.8xlarge",
    "g5.12xlarge",
    "g5.16xlarge",
    "g5.24xlarge",
    "g5.48xlarge",
    "g5g.xlarge",
    "g5g.2xlarge",
    "g5g.4xlarge",
    "g5g.8xlarge",
    "g5g.16xlarge",
    "g5g.metal",
    "h1.2xlarge",
    "h1.4xlarge",
    "h1.8xlarge",
    "h1.16xlarge",
    "hpc7g.4xlarge",
    "hpc7g.8xlarge",
    "hpc7g.16xlarge",
    "hs1.8xlarge",
    "i2.large",
    "i2.xlarge",
    "i2.xlarge.elasticsearch",
    "i2.2xlarge",
    "i2.2xlarge.elasticsearch",
    "i2.4xlarge",
    "i2.8xlarge",
    "i3.large",
    "i3.large.elasticsearch",
    "i3.xlarge",
    "i3.xlarge.elasticsearch",
    "i3.2xlarge",
    "i3.2xlarge.elasticsearch",
    "i3.4xlarge",
    "i3.4xlarge.elasticsearch",
    "i3.8xlarge",
    "i3.8xlarge.elasticsearch",
    "i3.16xlarge",
    "i3.16xlarge.elasticsearch",
    "i3.metal",
    "i3en.large",
    "i3en.xlarge",
    "i3en.2xlarge",
    "i3en.3xlarge",
    "i3en.6xlarge",
    "i3en.12xlarge",
    "i3en.24xlarge",
    "i3en.metal",
    "i4g.large",
    "i4g.xlarge",
    "i4g.2xlarge",
    "i4g.4xlarge",
    "i4g.8xlarge",
    "i4g.16xlarge",
    "i4i.large",
    "i4i.xlarge",
    "i4i.2xlarge",
    "i4i.4xlarge",
    "i4i.8xlarge",
    "i4i.16xlarge",
    "i4i.32xlarge",
    "i4i.metal",
    "im4gn.large",
    "im4gn.xlarge",
    "im4gn.2xlarge",
    "im4gn.4xlarge",
    "im4gn.8xlarge",
    "im4gn.16xlarge",
    "inf1.xlarge",
    "inf1.2xlarge",
    "inf1.6xlarge",
    "inf1.24xlarge",
    "inf2.xlarge",
    "inf2.8xlarge",
    "inf2.24xlarge",
    "inf2.48xlarge",
    "is4gen.medium",
    "is4gen.large",
    "is4gen.xlarge",
    "is4gen.2xlarge",
    "is4gen.4xlarge",
    "is4gen.8xlarge",
    "db.m1.medium",
    "m1.medium",
    "db.m1.small",
    "m1.small",
    "db.m1.large",
    "m1.large",
    "db.m1.xlarge",
    "m1.xlarge",
    "db.m2.xlarge",
    "m2.xlarge",
    "db.m2.2xlarge",
    "m2.2xlarge",
    "db.m2.4xlarge",
    "m2.4xlarge",
    "cache.m3.medium",
    "db.m3.medium",
    "m3.medium",
    "m3.medium.elasticsearch",
    "db.m3.large",
    "m3.large",
    "m3.large.elasticsearch",
    "db.m3.xlarge",
    "m3.xlarge",
    "m3.xlarge.elasticsearch",
    "db.m3.2xlarge",
    "m3.2xlarge",
    "m3.2xlarge.elasticsearch",
    "cache.m4.large",
    "db.m4.large",
    "m4.large",
    "m4.large.elasticsearch",
    "cache.m4.xlarge",
    "db.m4.xlarge",
    "m4.xlarge",
    "m4.xlarge.elasticsearch",
    "cache.m4.2xlarge",
    "db.m4.2xlarge",
    "m4.2xlarge",
    "m4.2xlarge.elasticsearch",
    "cache.m4.4xlarge",
    "db.m4.4xlarge",
    "m4.4xlarge",
    "m4.4xlarge.elasticsearch",
    "cache.m4.10xlarge",
    "db.m4.10xlarge",
    "m4.10xlarge",
    "m4.10xlarge.elasticsearch",
    "db.m4.16xlarge",
    "m4.16xlarge",
    "m5.large",
    "cache.m5.large",
    "db.m5.large",
    "m5.large.elasticsearch",
    "m5.xlarge",
    "cache.m5.xlarge",
    "db.m5.xlarge",
    "m5.xlarge.elasticsearch",
    "m5.2xlarge",
    "cache.m5.2xlarge",
    "db.m5.2xlarge",
    "m5.2xlarge.elasticsearch",
    "m5.4xlarge",
    "cache.m5.4xlarge",
    "db.m5.4xlarge",
    "m5.4xlarge.elasticsearch",
    "db.m5.8xlarge",
    "m5.8xlarge",
    "m5.12xlarge",
    "cache.m5.12xlarge",
    "db.m5.12xlarge",
    "m5.12xlarge.elasticsearch",
    "m5.16xlarge",
    "db.m5.16xlarge",
    "m5.24xlarge",
    "cache.m5.24xlarge",
    "db.m5.24xlarge",
    "m5.metal",
    "m5a.large",
    "m5a.xlarge",
    "m5a.2xlarge",
    "m5a.4xlarge",
    "m5a.8xlarge",
    "m5a.12xlarge",
    "m5a.16xlarge",
    "m5a.24xlarge",
    "m5ad.large",
    "m5ad.xlarge",
    "m5ad.2xlarge",
    "m5ad.4xlarge",
    "m5ad.8xlarge",
    "m5ad.12xlarge",
    "m5ad.16xlarge",
    "m5ad.24xlarge",
    "m5d.large",
    "m5d.xlarge",
    "m5d.2xlarge",
    "m5d.4xlarge",
    "m5d.8xlarge",
    "m5d.12xlarge",
    "m5d.16xlarge",
    "m5d.24xlarge",
    "m5d.metal",
    "m5dn.large",
    "m5dn.xlarge",
    "m5dn.2xlarge",
    "m5dn.4xlarge",
    "m5dn.8xlarge",
    "m5dn.12xlarge",
    "m5dn.16xlarge",
    "m5dn.24xlarge",
    "m5dn.metal",
    "m5n.large",
    "m5n.xlarge",
    "m5n.2xlarge",
    "m5n.4xlarge",
    "m5n.8xlarge",
    "m5n.12xlarge",
    "m5n.16xlarge",
    "m5n.24xlarge",
    "m5n.metal",
    "m5zn.large",
    "m5zn.xlarge",
    "m5zn.2xlarge",
    "m5zn.3xlarge",
    "m5zn.6xlarge",
    "m5zn.12xlarge",
    "m5zn.metal",
    "m6a.large",
    "m6a.xlarge",
    "m6a.2xlarge",
    "m6a.4xlarge",
    "m6a.8xlarge",
    "m6a.12xlarge",
    "m6a.16xlarge",
    "m6a.24xlarge",
    "m6a.32xlarge",
    "m6a.48xlarge",
    "m6a.metal",
    "m6g.medium",
    "cache.m6g.large",
    "db.m6g.large",
    "m6g.large",
    "m6g.large.elasticsearch",
    "cache.m6g.xlarge",
    "db.m6g.xlarge",
    "m6g.xlarge",
    "m6g.xlarge.elasticsearch",
    "cache.m6g.2xlarge",
    "db.m6g.2xlarge",
    "m6g.2xlarge",
    "m6g.2xlarge.elasticsearch",
    "cache.m6g.4xlarge",
    "db.m6g.4xlarge",
    "m6g.4xlarge",
    "m6g.4xlarge.elasticsearch",
    "cache.m6g.8xlarge",
    "db.m6g.8xlarge",
    "m6g.8xlarge",
    "m6g.8xlarge.elasticsearch",
    "cache.m6g.12xlarge",
    "db.m6g.12xlarge",
    "m6g.12xlarge",
    "m6g.12xlarge.elasticsearch",
    "cache.m6g.16xlarge",
    "db.m6g.16xlarge",
    "m6g.16xlarge",
    "m6g.metal",
    "m6gd.medium",
    "m6gd.large",
    "m6gd.xlarge",
    "m6gd.2xlarge",
    "m6gd.4xlarge",
    "m6gd.8xlarge",
    "m6gd.12xlarge",
    "m6gd.16xlarge",
    "m6gd.metal",
    "m6i.large",
    "m6i.xlarge",
    "m6i.2xlarge",
    "m6i.4xlarge",
    "m6i.8xlarge",
    "m6i.12xlarge",
    "m6i.16xlarge",
    "m6i.24xlarge",
    "m6i.32xlarge",
    "m6i.metal",
    "m6id.large",
    "m6id.xlarge",
    "m6id.2xlarge",
    "m6id.4xlarge",
    "m6id.8xlarge",
    "m6id.12xlarge",
    "m6id.16xlarge",
    "m6id.24xlarge",
    "m6id.32xlarge",
    "m6id.metal",
    "m6idn.large",
    "m6idn.xlarge",
    "m6idn.2xlarge",
    "m6idn.4xlarge",
    "m6idn.8xlarge",
    "m6idn.12xlarge",
    "m6idn.16xlarge",
    "m6idn.24xlarge",
    "m6idn.32xlarge",
    "m6idn.metal",
    "m6in.large",
    "m6in.xlarge",
    "m6in.2xlarge",
    "m6in.4xlarge",
    "m6in.8xlarge",
    "m6in.12xlarge",
    "m6in.16xlarge",
    "m6in.24xlarge",
    "m6in.32xlarge",
    "m6in.metal",
    "m7a.medium",
    "m7a.large",
    "m7a.xlarge",
    "m7a.2xlarge",
    "m7a.4xlarge",
    "m7a.8xlarge",
    "m7a.12xlarge",
    "m7a.16xlarge",
    "m7a.24xlarge",
    "m7a.32xlarge",
    "m7a.48xlarge",
    "m7a.metal-48xl",
    "m7g.medium",
    "m7g.large",
    "m7g.xlarge",
    "m7g.2xlarge",
    "m7g.4xlarge",
    "m7g.8xlarge",
    "m7g.12xlarge",
    "m7g.16xlarge",
    "m7g.metal",
    "m7gd.medium",
    "m7gd.large",
    "m7gd.xlarge",
    "m7gd.2xlarge",
    "m7gd.4xlarge",
    "m7gd.8xlarge",
    "m7gd.12xlarge",
    "m7gd.16xlarge",
    "m7i.large",
    "m7i.xlarge",
    "m7i.2xlarge",
    "m7i.4xlarge",
    "m7i.8xlarge",
    "m7i.12xlarge",
    "m7i.16xlarge",
    "m7i.24xlarge",
    "m7i.48xlarge",
    "m7i-flex.large",
    "m7i-flex.xlarge",
    "m7i-flex.2xlarge",
    "m7i-flex.4xlarge",
    "m7i-flex.8xlarge",
    "mac1.metal",
    "mac2.metal",
    "p2.xlarge",
    "p2.8xlarge",
    "p2.16xlarge",
    "p3.2xlarge",
    "p3.8xlarge",
    "p3.16xlarge",
    "p3dn.24xlarge",
    "p4d.24xlarge",
    "p4de.24xlarge",
    "p5.48xlarge",
    "db.r3.large",
    "r3.large",
    "r3.large.elasticsearch",
    "db.r3.xlarge",
    "r3.xlarge",
    "r3.xlarge.elasticsearch",
    "cache.r3.2xlarge",
    "db.r3.2xlarge",
    "r3.2xlarge",
    "r3.2xlarge.elasticsearch",
    "db.r3.4xlarge",
    "r3.4xlarge",
    "r3.4xlarge.elasticsearch",
    "db.r3.8xlarge",
    "r3.8xlarge",
    "r3.8xlarge.elasticsearch",
    "cache.r4.large",
    "db.r4.large",
    "r4.large",
    "r4.large.elasticsearch",
    "cache.r4.xlarge",
    "db.r4.xlarge",
    "r4.xlarge",
    "r4.xlarge.elasticsearch",
    "cache.r4.2xlarge",
    "db.r4.2xlarge",
    "r4.2xlarge",
    "r4.2xlarge.elasticsearch",
    "cache.r4.4xlarge",
    "db.r4.4xlarge",
    "r4.4xlarge",
    "r4.4xlarge.elasticsearch",
    "cache.r4.8xlarge",
    "db.r4.8xlarge",
    "r4.8xlarge",
    "r4.8xlarge.elasticsearch",
    "cache.r4.16xlarge",
    "db.r4.16xlarge",
    "r4.16xlarge",
    "r4.16xlarge.elasticsearch",
    "cache.r5.large",
    "db.r5.large",
    "r5.large",
    "r5.large.elasticsearch",
    "cache.r5.xlarge",
    "db.r5.xlarge",
    "r5.xlarge",
    "r5.xlarge.elasticsearch",
    "cache.r5.2xlarge",
    "db.r5.2xlarge",
    "r5.2xlarge",
    "r5.2xlarge.elasticsearch",
    "cache.r5.4xlarge",
    "db.r5.4xlarge",
    "r5.4xlarge",
    "r5.4xlarge.elasticsearch",
    "db.r5.8xlarge",
    "r5.8xlarge",
    "cache.r5.12xlarge",
    "db.r5.12xlarge",
    "r5.12xlarge",
    "r5.12xlarge.elasticsearch",
    "db.r5.16xlarge",
    "r5.16xlarge",
    "cache.r5.24xlarge",
    "db.r5.24xlarge",
    "r5.24xlarge",
    "r5.metal",
    "r5a.large",
    "r5a.xlarge",
    "r5a.2xlarge",
    "r5a.4xlarge",
    "r5a.8xlarge",
    "r5a.12xlarge",
    "r5a.16xlarge",
    "r5a.24xlarge",
    "r5ad.large",
    "r5ad.xlarge",
    "r5ad.2xlarge",
    "r5ad.4xlarge",
    "r5ad.8xlarge",
    "r5ad.12xlarge",
    "r5ad.16xlarge",
    "r5ad.24xlarge",
    "r5b.large",
    "r5b.xlarge",
    "r5b.2xlarge",
    "r5b.4xlarge",
    "r5b.8xlarge",
    "r5b.12xlarge",
    "r5b.16xlarge",
    "r5b.24xlarge",
    "r5b.metal",
    "r5d.large",
    "r5d.xlarge",
    "r5d.2xlarge",
    "r5d.4xlarge",
    "r5d.8xlarge",
    "r5d.12xlarge",
    "r5d.16xlarge",
    "r5d.24xlarge",
    "r5d.metal",
    "r5dn.large",
    "r5dn.xlarge",
    "r5dn.2xlarge",
    "r5dn.4xlarge",
    "r5dn.8xlarge",
    "r5dn.12xlarge",
    "r5dn.16xlarge",
    "r5dn.24xlarge",
    "r5dn.metal",
    "r5n.large",
    "r5n.xlarge",
    "r5n.2xlarge",
    "r5n.4xlarge",
    "r5n.8xlarge",
    "r5n.12xlarge",
    "r5n.16xlarge",
    "r5n.24xlarge",
    "r5n.metal",
    "r6a.large",
    "r6a.xlarge",
    "r6a.2xlarge",
    "r6a.4xlarge",
    "r6a.8xlarge",
    "r6a.12xlarge",
    "r6a.16xlarge",
    "r6a.24xlarge",
    "r6a.32xlarge",
    "r6a.48xlarge",
    "r6a.metal",
    "r6g.medium",
    "cache.r6g.large",
    "db.r6g.large",
    "r6g.large",
    "r6g.large.elasticsearch",
    "cache.r6g.xlarge",
    "db.r6g.xlarge",
    "r6g.xlarge",
    "r6g.xlarge.elasticsearch",
    "cache.r6g.2xlarge",
    "db.r6g.2xlarge",
    "r6g.2xlarge",
    "r6g.2xlarge.elasticsearch",
    "cache.r6g.4xlarge",
    "db.r6g.4xlarge",
    "r6g.4xlarge",
    "r6g.4xlarge.elasticsearch",
    "cache.r6g.8xlarge",
    "r6g.8xlarge",
    "r6g.8xlarge.elasticsearch",
    "cache.r6g.12xlarge",
    "db.r6g.12xlarge",
    "r6g.12xlarge",
    "r6g.12xlarge.elasticsearch",
    "cache.r6g.16xlarge",
    "db.r6g.16xlarge",
    "r6g.16xlarge",
    "r6g.metal",
    "r6gd.medium",
    "r6gd.large",
    "r6gd.large.elasticsearch",
    "r6gd.xlarge",
    "r6gd.xlarge.elasticsearch",
    "r6gd.2xlarge",
    "r6gd.2xlarge.elasticsearch",
    "r6gd.4xlarge",
    "r6gd.4xlarge.elasticsearch",
    "r6gd.8xlarge",
    "r6gd.8xlarge.elasticsearch",
    "r6gd.12xlarge",
    "r6gd.12xlarge.elasticsearch",
    "r6gd.16xlarge",
    "r6gd.16xlarge.elasticsearch",
    "r6gd.metal",
    "r6i.large",
    "r6i.xlarge",
    "r6i.2xlarge",
    "r6i.4xlarge",
    "r6i.8xlarge",
    "r6i.12xlarge",
    "r6i.16xlarge",
    "r6i.24xlarge",
    "r6i.32xlarge",
    "r6i.metal",
    "r6id.large",
    "r6id.xlarge",
    "r6id.2xlarge",
    "r6id.4xlarge",
    "r6id.8xlarge",
    "r6id.12xlarge",
    "r6id.16xlarge",
    "r6id.24xlarge",
    "r6id.32xlarge",
    "r6id.metal",
    "r6idn.large",
    "r6idn.xlarge",
    "r6idn.2xlarge",
    "r6idn.4xlarge",
    "r6idn.8xlarge",
    "r6idn.12xlarge",
    "r6idn.16xlarge",
    "r6idn.24xlarge",
    "r6idn.32xlarge",
    "r6idn.metal",
    "r6in.large",
    "r6in.xlarge",
    "r6in.2xlarge",
    "r6in.4xlarge",
    "r6in.8xlarge",
    "r6in.12xlarge",
    "r6in.16xlarge",
    "r6in.24xlarge",
    "r6in.32xlarge",
    "r6in.metal",
    "r7a.medium",
    "r7a.large",
    "r7a.xlarge",
    "r7a.2xlarge",
    "r7a.4xlarge",
    "r7a.8xlarge",
    "r7a.12xlarge",
    "r7a.16xlarge",
    "r7a.24xlarge",
    "r7a.32xlarge",
    "r7a.48xlarge",
    "r7a.metal-48xl",
    "r7g.medium",
    "r7g.large",
    "r7g.xlarge",
    "r7g.2xlarge",
    "r7g.4xlarge",
    "r7g.8xlarge",
    "r7g.12xlarge",
    "r7g.16xlarge",
    "r7g.metal",
    "r7gd.medium",
    "r7gd.large",
    "r7gd.xlarge",
    "r7gd.2xlarge",
    "r7gd.4xlarge",
    "r7gd.8xlarge",
    "r7gd.12xlarge",
    "r7gd.16xlarge",
    "r7iz.large",
    "r7iz.xlarge",
    "r7iz.2xlarge",
    "r7iz.4xlarge",
    "r7iz.8xlarge",
    "r7iz.12xlarge",
    "r7iz.16xlarge",
    "r7iz.32xlarge",
    "ra3.4xlarge",
    "ra3.16xlarge",
    "t1.micro",
    "cache.t2.micro",
    "db.t2.micro",
    "cache.t2.small",
    "db.t2.small",
    "t2.micro",
    "t2.micro.elasticsearch",
    "t2.nano",
    "t2.small",
    "t2.small.elasticsearch",
    "db.t2.large",
    "cache.t2.medium",
    "db.t2.medium",
    "t2.large",
    "t2.medium",
    "t2.medium.elasticsearch",
    "db.t2.xlarge",
    "t2.xlarge",
    "db.t2.2xlarge",
    "t2.2xlarge",
    "db.t3.large",
    "t3.large",
    "cache.t3.medium",
    "db.t3.medium",
    "t3.medium",
    "t3.medium.elasticsearch",
    "cache.t3.micro",
    "db.t3.micro",
    "t3.micro",
    "t3.nano",
    "cache.t3.small",
    "db.t3.small",
    "t3.small",
    "t3.small.elasticsearch",
    "db.t3.xlarge",
    "t3.xlarge",
    "db.t3.2xlarge",
    "t3.2xlarge",
    "t3a.large",
    "t3a.medium",
    "t3a.micro",
    "t3a.nano",
    "t3a.small",
    "t3a.xlarge",
    "t3a.2xlarge",
    "t4g.large",
    "t4g.medium",
    "t4g.micro",
    "t4g.nano",
    "t4g.small",
    "t4g.xlarge",
    "t4g.2xlarge",
    "trn1.2xlarge",
    "trn1.32xlarge",
    "trn1n.32xlarge",
    "u-12tb1.112xlarge",
    "u-12tb1.metal",
    "u-18tb1.112xlarge",
    "u-18tb1.metal",
    "u-24tb1.112xlarge",
    "u-24tb1.metal",
    "u-3tb1.56xlarge",
    "u-6tb1.56xlarge",
    "u-6tb1.112xlarge",
    "u-6tb1.metal",
    "u-9tb1.112xlarge",
    "u-9tb1.metal",
    "vt1.3xlarge",
    "vt1.6xlarge",
    "vt1.24xlarge",
    "db.x1.16xlarge",
    "x1.16xlarge",
    "db.x1.32xlarge",
    "x1.32xlarge",
    "db.x1e.xlarge",
    "x1e.xlarge",
    "db.x1e.2xlarge",
    "x1e.2xlarge",
    "db.x1e.4xlarge",
    "x1e.4xlarge",
    "db.x1e.8xlarge",
    "x1e.8xlarge",
    "db.x1e.16xlarge",
    "x1e.16xlarge",
    "db.x1e.32xlarge",
    "x1e.32xlarge",
    "x2gd.medium",
    "x2gd.large",
    "x2gd.xlarge",
    "x2gd.2xlarge",
    "x2gd.4xlarge",
    "x2gd.8xlarge",
    "x2gd.12xlarge",
    "x2gd.16xlarge",
    "x2gd.metal",
    "x2idn.16xlarge",
    "x2idn.24xlarge",
    "x2idn.32xlarge",
    "x2idn.metal",
    "x2iedn.xlarge",
    "x2iedn.2xlarge",
    "x2iedn.4xlarge",
    "x2iedn.8xlarge",
    "x2iedn.16xlarge",
    "x2iedn.24xlarge",
    "x2iedn.32xlarge",
    "x2iedn.metal",
    "x2iezn.2xlarge",
    "x2iezn.4xlarge",
    "x2iezn.6xlarge",
    "x2iezn.8xlarge",
    "x2iezn.12xlarge",
    "x2iezn.metal",
    "db.z1d.large",
    "z1d.large",
    "db.z1d.xlarge",
    "z1d.xlarge",
    "db.z1d.2xlarge",
    "z1d.2xlarge",
    "db.z1d.3xlarge",
    "z1d.3xlarge",
    "db.z1d.6xlarge",
    "z1d.6xlarge",
    "db.z1d.12xlarge",
    "z1d.12xlarge",
    "z1d.metal"
]
```
</details>

## Get the impacts of a cloud instance with default usage data

Query:

```bash
# Query the data for `r6g.medium` with default usage value
curl -X 'GET' \
  '{{ endpoint }}/v1/cloud/instance?provider=aws&instance_type=r6g.medium&verbose=false&duration=8760&criteria=gwp' \
  -H 'accept: application/json'
```

<details>
	<summary>Results</summary>

```json
{
    "impacts": {
        "gwp": {
            "unit": "kgCO2eq",
            "description": "Total climate change",
            "embedded": {
                "value": 5.4,
                "min": 3.063,
                "max": 9.26,
                "warnings": [
                    "End of life is not included in the calculation"
                ]
            },
            "use": {
                "value": 18.0,
                "min": 0.9733,
                "max": 63.85
            }
        }
    }
}
```

This query returns :

* Only gwp impact since ```criteria=gwp```
* The usage impact for 1 year (since ```duration=8760```) of compute at 50% of load (default) for a r6g.medium instance type in europe (default)
* The embedded impacts of a ```r6g.medium``` allocated on one year (since ```duration=8760```).

</details>

## Get the values used to assess the impacts of each component

This is the same query as before. However, you add the `verbose=true` flag to get the impacts of each of its
components (including usage) and the value of the attributes used for the calculation. Both adp and gwp impacts are compute since ```criteria=adp&criteria=gwp```

!!!warning
  Before v1.2, the impacts in the verbose dictionary qualified the impacts of the component of the whole server hosting the instance. Since v1.2, the impacts in the verbose dictionary are the impacts of the part of the component used by the instance itself.

Query :

```bash
# Query the data for `r6g.medium` with default usage value
curl -X 'GET' \
  '{{ endpoint }}/v1/cloud/instance?cloud_provider=aws&instance_type=r6g.medium&verbose=true&duration=8760&criteria=gwp&criteria=adp' \
  -H 'accept: application/json'
```

<details>
	<summary>Results</summary>

```json
{
    "impacts": {
        "gwp": {
            "unit": "kgCO2eq",
            "description": "Total climate change",
            "embedded": {
                "value": 5.4,
                "min": 3.063,
                "max": 9.26,
                "warnings": [
                    "End of life is not included in the calculation"
                ]
            },
            "use": {
                "value": 18.0,
                "min": 0.9733,
                "max": 63.85
            }
        },
        "adp": {
            "unit": "kgSbeq",
            "description": "Use of minerals and fossil ressources",
            "embedded": {
                "value": 0.00057,
                "min": 0.0003965,
                "max": 0.0008337,
                "warnings": [
                    "End of life is not included in the calculation"
                ]
            },
            "use": {
                "value": 3e-06,
                "min": 5.603e-07,
                "max": 1.498e-05
            }
        }
    },
    "verbose": {
        "units": {
            "value": 1,
            "status": "ARCHETYPE",
            "min": 1,
            "max": 1
        },
        "vcpu": {
            "value": 1.0,
            "status": "ARCHETYPE"
        },
        "memory": {
            "value": 8.0,
            "status": "ARCHETYPE",
            "unit": "GB"
        },
        "avg_power": {
            "value": 5.354039687499999,
            "status": "COMPLETED",
            "unit": "W",
            "min": 4.8307125,
            "max": 6.44095
        },
        "duration": {
            "value": 8760.0,
            "unit": "hours"
        },
        "ASSEMBLY-1": {
            "impacts": {
                "gwp": {
                    "unit": "kgCO2eq",
                    "description": "Total climate change",
                    "embedded": {
                        "value": 0.02609,
                        "min": 0.02609,
                        "max": 0.02609,
                        "warnings": [
                            "End of life is not included in the calculation"
                        ]
                    },
                    "use": "not implemented"
                },
                "adp": {
                    "unit": "kgSbeq",
                    "description": "Use of minerals and fossil ressources",
                    "embedded": {
                        "value": 5.508e-09,
                        "min": 5.508e-09,
                        "max": 5.508e-09,
                        "warnings": [
                            "End of life is not included in the calculation"
                        ]
                    },
                    "use": "not implemented"
                }
            },
            "units": {
                "value": 1,
                "status": "ARCHETYPE",
                "min": 1,
                "max": 1
            },
            "duration": {
                "value": 8760.0,
                "unit": "hours"
            }
        },
        "CPU-1": {
            "impacts": {
                "gwp": {
                    "unit": "kgCO2eq",
                    "description": "Total climate change",
                    "embedded": {
                        "value": 0.07465,
                        "min": 0.07465,
                        "max": 0.07465,
                        "warnings": [
                            "End of life is not included in the calculation"
                        ]
                    },
                    "use": {
                        "value": 6.0,
                        "min": 0.3533,
                        "max": 17.38
                    }
                },
                "adp": {
                    "unit": "kgSbeq",
                    "description": "Use of minerals and fossil ressources",
                    "embedded": {
                        "value": 7.97e-05,
                        "min": 7.97e-05,
                        "max": 7.97e-05,
                        "warnings": [
                            "End of life is not included in the calculation"
                        ]
                    },
                    "use": {
                        "value": 1e-06,
                        "min": 2.034e-07,
                        "max": 4.08e-06
                    }
                }
            },
            "units": {
                "value": 1.0,
                "status": "ARCHETYPE",
                "min": 1.0,
                "max": 1.0
            },
            "core_units": {
                "value": 64,
                "status": "COMPLETED",
                "source": "Completed from name name based on https://docs.google.com/spreadsheets/d/1DqYgQnEDLQVQm5acMAhLgHLD8xXCG9BIrk-_Nv6jF3k/edit#gid=224728652.",
                "min": 64,
                "max": 64
            },
            "die_size": {
                "value": 457,
                "status": "COMPLETED",
                "unit": "mm2",
                "source": "Value of cpu_manufacture https://en.wikichip.org/wiki/annapurna_labs/alpine/alc12b00 : Completed from name name based on https://docs.google.com/spreadsheets/d/1DqYgQnEDLQVQm5acMAhLgHLD8xXCG9BIrk-_Nv6jF3k/edit#gid=224728652.",
                "min": 457,
                "max": 457
            },
            "model_range": {
                "value": "Graviton2",
                "status": "COMPLETED",
                "source": "Completed from name name based on https://docs.google.com/spreadsheets/d/1DqYgQnEDLQVQm5acMAhLgHLD8xXCG9BIrk-_Nv6jF3k/edit#gid=224728652.",
                "min": "Graviton2",
                "max": "Graviton2"
            },
            "manufacturer": {
                "value": "Annapurna Labs",
                "status": "COMPLETED",
                "source": "Completed from name name based on https://docs.google.com/spreadsheets/d/1DqYgQnEDLQVQm5acMAhLgHLD8xXCG9BIrk-_Nv6jF3k/edit#gid=224728652.",
                "min": "Annapurna Labs",
                "max": "Annapurna Labs"
            },
            "family": {
                "value": "Graviton2",
                "status": "COMPLETED",
                "source": "Completed from name name based on https://docs.google.com/spreadsheets/d/1DqYgQnEDLQVQm5acMAhLgHLD8xXCG9BIrk-_Nv6jF3k/edit#gid=224728652.",
                "min": "Graviton2",
                "max": "Graviton2"
            },
            "name": {
                "value": "Annapurna Labs Graviton2",
                "status": "COMPLETED",
                "source": "fuzzy match",
                "min": "Annapurna Labs Graviton2",
                "max": "Annapurna Labs Graviton2"
            },
            "tdp": {
                "value": 150,
                "status": "COMPLETED",
                "unit": "W",
                "source": "Completed from name name based on https://docs.google.com/spreadsheets/d/1DqYgQnEDLQVQm5acMAhLgHLD8xXCG9BIrk-_Nv6jF3k/edit#gid=224728652.",
                "min": 150,
                "max": 150
            },
            "threads": {
                "value": 64,
                "status": "COMPLETED",
                "source": "Completed from name name based on https://docs.google.com/spreadsheets/d/1DqYgQnEDLQVQm5acMAhLgHLD8xXCG9BIrk-_Nv6jF3k/edit#gid=224728652.",
                "min": 64,
                "max": 64
            },
            "duration": {
                "value": 8760.0,
                "unit": "hours"
            },
            "avg_power": {
                "value": 1.75359375,
                "status": "COMPLETED",
                "unit": "W",
                "min": 1.75359375,
                "max": 1.75359375
            },
            "time_workload": {
                "value": 50.0,
                "status": "ARCHETYPE",
                "unit": "%",
                "min": 0.0,
                "max": 100.0
            },
            "usage_location": {
                "value": "EEE",
                "status": "DEFAULT",
                "unit": "CodSP3 - NCS Country Codes - NATO"
            },
            "use_time_ratio": {
                "value": 1.0,
                "status": "ARCHETYPE",
                "unit": "/1",
                "min": 1.0,
                "max": 1.0
            },
            "hours_life_time": {
                "value": 35040.0,
                "status": "COMPLETED",
                "unit": "hours",
                "source": "from device",
                "min": 35040.0,
                "max": 35040.0
            },
            "workloads": {
                "value": [
                    {
                        "load_percentage": 0,
                        "power_watt": 18.0
                    },
                    {
                        "load_percentage": 10,
                        "power_watt": 48.0
                    },
                    {
                        "load_percentage": 50,
                        "power_watt": 112.5
                    },
                    {
                        "load_percentage": 100,
                        "power_watt": 153.0
                    }
                ],
                "status": "COMPLETED",
                "unit": "workload_rate:W"
            },
            "params": {
                "value": {
                    "a": 76.2719009422506,
                    "b": 0.06416377550196647,
                    "c": 20.45110311208281,
                    "d": -2.8366153241302814
                },
                "status": "COMPLETED",
                "source": "From TDP"
            },
            "gwp_factor": {
                "value": 0.38,
                "status": "DEFAULT",
                "unit": "kg CO2eq/kWh",
                "source": "https://www.sciencedirect.com/science/article/pii/S0306261921012149",
                "min": 0.023,
                "max": 1.13161
            },
            "adp_factor": {
                "value": 6.42317e-08,
                "status": "DEFAULT",
                "unit": "kg Sbeq/kWh",
                "source": "ADEME Base IMPACTS \u00ae",
                "min": 1.324e-08,
                "max": 2.65575e-07
            }
        },
        "RAM-1": {
            "impacts": {
                "gwp": {
                    "unit": "kgCO2eq",
                    "description": "Total climate change",
                    "embedded": {
                        "value": 3.9,
                        "min": 2.179,
                        "max": 7.366,
                        "warnings": [
                            "End of life is not included in the calculation"
                        ]
                    },
                    "use": {
                        "value": 120.0,
                        "min": 7.324,
                        "max": 360.4
                    }
                },
                "adp": {
                    "unit": "kgSbeq",
                    "description": "Use of minerals and fossil ressources",
                    "embedded": {
                        "value": 0.00021,
                        "min": 0.0001587,
                        "max": 0.0003072,
                        "warnings": [
                            "End of life is not included in the calculation"
                        ]
                    },
                    "use": {
                        "value": 2e-05,
                        "min": 4.216e-06,
                        "max": 8.457e-05
                    }
                }
            },
            "units": {
                "value": 16.0,
                "status": "ARCHETYPE",
                "min": 16.0,
                "max": 16.0
            },
            "capacity": {
                "value": 32.0,
                "status": "ARCHETYPE",
                "unit": "GB",
                "min": 32.0,
                "max": 32.0
            },
            "density": {
                "value": 1.2443636363636363,
                "status": "COMPLETED",
                "unit": "GB/cm2",
                "source": "Average of 11 rows",
                "min": 0.625,
                "max": 2.375
            },
            "duration": {
                "value": 8760.0,
                "unit": "hours"
            },
            "avg_power": {
                "value": 2.272,
                "status": "COMPLETED",
                "unit": "W",
                "min": 2.272,
                "max": 2.272
            },
            "time_workload": {
                "value": 50.0,
                "status": "ARCHETYPE",
                "unit": "%",
                "min": 0.0,
                "max": 100.0
            },
            "usage_location": {
                "value": "EEE",
                "status": "DEFAULT",
                "unit": "CodSP3 - NCS Country Codes - NATO"
            },
            "use_time_ratio": {
                "value": 1.0,
                "status": "ARCHETYPE",
                "unit": "/1",
                "min": 1.0,
                "max": 1.0
            },
            "hours_life_time": {
                "value": 35040.0,
                "status": "COMPLETED",
                "unit": "hours",
                "source": "from device",
                "min": 35040.0,
                "max": 35040.0
            },
            "params": {
                "value": {
                    "a": 9.088
                },
                "status": "COMPLETED",
                "source": "(ram_electrical_factor_per_go : 0.284) * (ram_capacity: 32.0) "
            },
            "gwp_factor": {
                "value": 0.38,
                "status": "DEFAULT",
                "unit": "kg CO2eq/kWh",
                "source": "https://www.sciencedirect.com/science/article/pii/S0306261921012149",
                "min": 0.023,
                "max": 1.13161
            },
            "adp_factor": {
                "value": 6.42317e-08,
                "status": "DEFAULT",
                "unit": "kg Sbeq/kWh",
                "source": "ADEME Base IMPACTS \u00ae",
                "min": 1.324e-08,
                "max": 2.65575e-07
            }
        },
        "POWER_SUPPLY-1": {
            "impacts": {
                "gwp": {
                    "unit": "kgCO2eq",
                    "description": "Total climate change",
                    "embedded": {
                        "value": 0.57,
                        "min": 0.1898,
                        "max": 0.9492,
                        "warnings": [
                            "End of life is not included in the calculation"
                        ]
                    },
                    "use": "not implemented"
                },
                "adp": {
                    "unit": "kgSbeq",
                    "description": "Use of minerals and fossil ressources",
                    "embedded": {
                        "value": 0.00019,
                        "min": 6.484e-05,
                        "max": 0.0003242,
                        "warnings": [
                            "End of life is not included in the calculation"
                        ]
                    },
                    "use": "not implemented"
                }
            },
            "units": {
                "value": 2.0,
                "status": "ARCHETYPE",
                "min": 2.0,
                "max": 2.0
            },
            "unit_weight": {
                "value": 2.99,
                "status": "ARCHETYPE",
                "unit": "kg",
                "min": 1.0,
                "max": 5.0
            },
            "duration": {
                "value": 8760.0,
                "unit": "hours"
            }
        },
        "CASE-1": {
            "impacts": {
                "gwp": {
                    "unit": "kgCO2eq",
                    "description": "Total climate change",
                    "embedded": {
                        "value": 0.59,
                        "min": 0.3355,
                        "max": 0.5859,
                        "warnings": [
                            "End of life is not included in the calculation"
                        ]
                    },
                    "use": "not implemented"
                },
                "adp": {
                    "unit": "kgSbeq",
                    "description": "Use of minerals and fossil ressources",
                    "embedded": {
                        "value": 7.9e-05,
                        "min": 7.891e-05,
                        "max": 0.0001081,
                        "warnings": [
                            "End of life is not included in the calculation"
                        ]
                    },
                    "use": "not implemented"
                }
            },
            "units": {
                "value": 1,
                "status": "ARCHETYPE",
                "min": 1,
                "max": 1
            },
            "case_type": {
                "value": "rack",
                "status": "ARCHETYPE"
            },
            "duration": {
                "value": 8760.0,
                "unit": "hours"
            }
        },
        "MOTHERBOARD-1": {
            "impacts": {
                "gwp": {
                    "unit": "kgCO2eq",
                    "description": "Total climate change",
                    "embedded": {
                        "value": 0.2582,
                        "min": 0.2582,
                        "max": 0.2582,
                        "warnings": [
                            "End of life is not included in the calculation"
                        ]
                    },
                    "use": "not implemented"
                },
                "adp": {
                    "unit": "kgSbeq",
                    "description": "Use of minerals and fossil ressources",
                    "embedded": {
                        "value": 1.441e-05,
                        "min": 1.441e-05,
                        "max": 1.441e-05,
                        "warnings": [
                            "End of life is not included in the calculation"
                        ]
                    },
                    "use": "not implemented"
                }
            },
            "units": {
                "value": 1,
                "status": "ARCHETYPE",
                "min": 1,
                "max": 1
            },
            "duration": {
                "value": 8760.0,
                "unit": "hours"
            }
        },
        "usage_location": {
            "value": "EEE",
            "status": "DEFAULT",
            "unit": "CodSP3 - NCS Country Codes - NATO"
        },
        "use_time_ratio": {
            "value": 1.0,
            "status": "ARCHETYPE",
            "unit": "/1",
            "min": 1.0,
            "max": 1.0
        },
        "hours_life_time": {
            "value": 35040.0,
            "status": "COMPLETED",
            "unit": "hours",
            "source": "from device",
            "min": 35040.0,
            "max": 35040.0
        },
        "other_consumption_ratio": {
            "value": 0.33,
            "status": "ARCHETYPE",
            "unit": "ratio /1",
            "min": 0.2,
            "max": 0.6
        },
        "gwp_factor": {
            "value": 0.38,
            "status": "DEFAULT",
            "unit": "kg CO2eq/kWh",
            "source": "https://www.sciencedirect.com/science/article/pii/S0306261921012149",
            "min": 0.023,
            "max": 1.13161
        },
        "adp_factor": {
            "value": 6.42317e-08,
            "status": "DEFAULT",
            "unit": "kg Sbeq/kWh",
            "source": "ADEME Base IMPACTS \u00ae",
            "min": 1.324e-08,
            "max": 2.65575e-07
        }
    }
}
```
</details>

## Get the impacts of a cloud instance with custom usage data

In this query we override default usage data with your custom data for ```r6g.medium``` instance type

*Note: you can override zero to many attributes.*

Query:

```bash
# Query the data for `r6g.medium` with custom usage value
curl -X 'POST' \
  '{{ endpoint }}/v1/cloud/instance?verbose=false&duration=2' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
    "provider": "aws",
    "instance_type": "r6g.medium",
    "usage": {
       "usage_location": "FRA",
       "time_workload": [
          {
            "time_percentage": 50,
            "load_percentage": 0
          },
          {
            "time_percentage": 50,
            "load_percentage": 50
          }
       ]}
    }'
```
<details>
	<summary>Results</summary>

```json
{
    "impacts": {
        "gwp": {
            "unit": "kgCO2eq",
            "description": "Total climate change",
            "embedded": {
                "value": 0.0012,
                "min": 0.0006994,
                "max": 0.002114,
                "warnings": [
                    "End of life is not included in the calculation"
                ]
            },
            "use": {
                "value": 0.00086,
                "min": 0.0007735,
                "max": 0.001031
            }
        },
        "adp": {
            "unit": "kgSbeq",
            "description": "Use of minerals and fossil ressources",
            "embedded": {
                "value": 1.31e-07,
                "min": 9.054e-08,
                "max": 1.903e-07,
                "warnings": [
                    "End of life is not included in the calculation"
                ]
            },
            "use": {
                "value": 4.2e-10,
                "min": 3.834e-10,
                "max": 5.112e-10
            }
        },
        "pe": {
            "unit": "MJ",
            "description": "Consumption of primary energy",
            "embedded": {
                "value": 0.016,
                "min": 0.009094,
                "max": 0.02717,
                "warnings": [
                    "End of life is not included in the calculation"
                ]
            },
            "use": {
                "value": 0.099,
                "min": 0.0891,
                "max": 0.1188
            }
        }
    }
}
```
</details>


* Since no criteria flags are specified, the API returns the impacts of the instance for the default criteria (adp, pe,
  gwp).
* Since duration is set at 2 and time_workload is provided, the query usage can be translated as such :

```I used a r6g.medium in a french data center for 2 hours half of the time in IDLE mode and half of the time at 50% of workload```

For further information see : [The explanation page on cloud](../Explanations/services/cloud.md)