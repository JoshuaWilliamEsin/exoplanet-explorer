# The Most Useful Free API Nobody Knows About: NASA's Exoplanet Archive TAP Service

## The API

**NASA Exoplanet Archive TAP service**
https://exoplanetarchive.ipac.caltech.edu/TAP/sync

Most people who touch NASA's public APIs know the APOD picture endpoint or the near-Earth asteroid feed. Almost nobody realizes that the actual scientific database behind all exoplanet discoveries, the same table researchers use, is exposed as a plain HTTP endpoint you can query with SQL-style filters and get back JSON or CSV.

It is run by IPAC at Caltech on behalf of NASA. There is no account, no key, no email signup, no rate-limit page hidden behind a login wall. You send a query, you get data. It has been up and quietly serving the astronomy community for years, which is probably why it never makes those "cool free APIs" listicles: the people who need it already know about it, and nobody else stumbles into it.

## A working example

This was run for real while writing this submission, and reproduced on a second machine:

```
curl -s -G "https://exoplanetarchive.ipac.caltech.edu/TAP/sync" \
  --data-urlencode "query=select pl_name,hostname,disc_year,pl_orbper,sy_dist from ps where default_flag=1 and disc_year=2024 and sy_dist<50 order by sy_dist" \
  --data-urlencode "format=csv"
```

The response (abridged - 48 rows came back):

```
pl_name,hostname,disc_year,pl_orbper,sy_dist
"Barnard b","Barnard's star",2024,3.15420000000,1.82655000
"Teegarden's Star d","Teegarden's Star",2024,26.13000000000,3.83078000
"GJ 1289 b","GJ 1289",2024,111.74000000000,8.35147000
```

Translation: every planet confirmed in 2024 that orbits within 50 light-years of us, sorted by distance. Barnard's Star b, the closest of them, laps its star every 3.15 days. One count query against the same table confirms 6,451 confirmed planets in the `ps` table right now.

Change `format=csv` to `format=json` if you prefer JSON. The full list of queryable columns is in the archive's documented table schema.

## A practical use case

The obvious one: a "new neighbors" tracker. A small script that runs once a week, asks for planets discovered in the last 7 days within 50 light-years, and posts whatever it finds, newly confirmed worlds orbiting stars you can point at in the night sky, delivered before any news aggregator picks them up.

Beyond that: a classroom tool with zero setup. Students can filter by orbital period or distance and immediately see real astrophysics, like how planets with orbits under 5 days (roasting close to their stars) vastly outnumber slow ones in the discovery record, because short orbits are easier to detect. That's a genuine selection-effect lesson hiding in a plain CSV.

## The demo

`exoplanet-explorer.html` is a single-file web app, included in this submission. It queries the API live; nothing cached, nothing faked and lets you filter by maximum distance in light-years, discovery year, and orbital period, with a sortable results table and summary stats.

To run it: put it in a folder with the included `server.py` and run `py server.py` (Python 3, nothing else). The server exists for one reason: browsers block cross-origin requests to APIs that don't send CORS headers, and NASA's service doesn't, so a 16-line local proxy fetches on the page's behalf. The API itself never required a key at any point.

## Why it's special

1. **Zero friction.** No key, no account, no payment info, no expiry. The curl above is the entire onboarding process.
2. **It's a queryable database, not a feed.** Most free APIs hand you fixed endpoints. This one takes SQL-style WHERE clauses over dozens of columns (distance, orbital period, discovery method, stellar temperature, and more), so the same endpoint answers a hundred different questions.
3. **It's the primary source.** This isn't a re-sold aggregate; it's the working table planetary scientists use, kept current as discoveries are confirmed.
4. **Obscurity for the right reason.** It's well documented, it just never appears in API roundups because it looks like a research tool rather than a product. The best kind of hidden gem: public, stable, and overlooked.