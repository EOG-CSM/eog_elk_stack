# Ranking Users

1. Click menu on the left (3 lines), then under Analytics, click dashboard.
2. Click create new visualization.
3. From the left, drag userinfo.email into the graph
4. Click the top 5 values, and change the number of values to whatever you want
5. Then follow the steps below depending on how you want to rank.

## Rank by number of accesses
1. Leave rank by as count of records.

## Rank by Volume Downloaded
1. Click on what is under the vertical axis section
2. Select the field `http.response.body.bytes`
3. Under functions, select sum
4. Now there should be a vertical axis section that says `Sum of http.response.body.bytes`.

## Export
1. Click download as CSV at the top
