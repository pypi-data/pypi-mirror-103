
# Table of Contents

1.  [CSV Reconcile Geo distance scoring plugin](#org29f43c1)
    1.  [Reconciliation](#org5045203)
    2.  [Scoring](#orgab2a0ca)
    3.  [Configuration](#orgb7b0f96)
    4.  [Future enhancements](#org67b2374)


<a id="org29f43c1"></a>

# CSV Reconcile Geo distance scoring plugin

A scoring plugin for [csv-reconcile](https://github.com/gitonthescene/csv-reconcile) using geodesic distance.  See csv-reconcile for details.


<a id="org5045203"></a>

## Reconciliation

This plugin is used to reconcile values representing points on the globe.  It expects those
values to be in [well-known text](https://en.wikipedia.org/wiki/Well-known_text_representation_of_geometry) format for a point.  That is, like so: `POINT( longitude latitude )`.

The pre-processor automatically strips off [literal datatypes](https://www.w3.org/TR/sparql11-query/#matchingRDFLiterals) when present as well as double quotes.

The CSV column to be reconciled needs to be in the same format.  In addition, there must be at
most one instance of any id column.  For instance, if reconciling against [coordinate location](https://www.wikidata.org/wiki/Property:P625) for
a [wikidata item](https://www.wikidata.org/wiki/Help:Items), there must be at most one location per item.


<a id="orgab2a0ca"></a>

## Scoring

The scoring used is more or less arbitrary but has the following properties:

-   The highest score is 100 and occurs when the distance to the reconciliation candidate is zero
-   The lower the score the greater the distance to the reconciliation candidate
-   The score is scaled so that a distance of 10km yields a score of 50


<a id="orgb7b0f96"></a>

## Configuration

The plugin can be controlled via `SCOREOPTIONS` in the csv-reconcile `--config` file.
`SCOREOPTIONS` is a [Python dictionary](https://www.w3schools.com/python/python_dictionaries.asp) and thus has the following form `SCOREOPTIONS={
   "key1":"value1,"key2":"value2"}`.

-   `SCALE` set distance in kilometers at which a score of 50 occurs.  ( Default 10km )  e.g. `"SCALE":2`
-   `COORDRANGE` If supplied do a precheck that both the latitude and the longitude of the compared
    values are within range.  This is for performance to avoid the more expensive distance
    calculation for points farther apart. e.g. `"COORDRANGE":"1"`


<a id="org67b2374"></a>

## Future enhancements

Some of the current implementation was driven by the current design of csv-reconcile.  Both may
be updated to accommodate the following:

-   Allow for separate latitude and longitude column in the CSV file
-   Add some scoring options such as the following:
    -   Allow for overriding the scaling function
    -   etc.

