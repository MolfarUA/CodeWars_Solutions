SELECT id, last::inet - first::inet as ips_between
FROM ip_addresses;
________________
SELECT
DISTINCT id,
(d4+d3*256+d2*256*256+d1*256*256*256) as ips_between
FROM
(SELECT *,
cast(split_part(last,'.',1) as bigint) - cast(split_part(first,'.',1) as bigint) as d1,
cast(split_part(last,'.',2) as bigint) - cast(split_part(first,'.',2) as bigint) as d2,
cast(split_part(last,'.',3) as bigint) - cast(split_part(first,'.',3) as bigint) as d3,
cast(split_part(last,'.',4) as bigint) - cast(split_part(first,'.',4) as bigint) as d4
FROM ip_addresses) as ip;
________________
SELECT id, last::inet - first::inet AS ips_between FROM ip_addresses ORDER BY id;
