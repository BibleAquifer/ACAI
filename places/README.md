# ACAI Place Data

**Initial Draft Edition**, v1.00, 2024-10-08

Rick Brannan, rick.brannan@biblionexus.org, and Jessica Parks, jessica.parks@biblionexus.org, 2024-05-10

## Context

BiblioNexus and Biblica are working together to create data representing explicit and implicit instances of 
people and places (and other things) in the Bible. This information also includes entity-level (for places, place-level)
information about the place, such as a title/default form (and localizations), description (and localizations), 
and other data.

This information is being compiled as part of the ACAI project, the _Aquifer Concept Architecture for Information_, 
which itself is a part of the [Bible Aquifer](https://www.notion.so/etenlab/Aquifer-Home-c88f20c13eb440539a9ec532ca30b78a) project.

## Sources

* Biblica/Clear-Bible's [Macula Hebrew](https://github.com/Clear-Bible/macula-hebrew)
* Biblica/Clear-Bible's [Macula Greek](https://github.com/Clear-Bible/macula-greek)
* Biblica/Clear-Bible's [speaker-quotations](https://github.com/Clear-Bible/speaker-quotations), an attempt to identify the 
  original language words, in both the Old and New Testaments, translated as quotations (material using "double" and 'single' 
  quotation marks) in various English Bibles. It also attempts to associate speakers with the quotations, where possible, 
  using data from Faith Comes By Hearing.
* United Bible Societies' _UBS Dictionary of Biblical Hebrew_ (UBSDBH) and _UBS Dictionary of the Greek New Testament_
  (UBSDGNT). See [SemanticDictionary.org](https://semanticdictionary.org/) for an implementation and the git repo
  [ubs-open-license](https://github.com/ubsicap/ubs-open-license) for data (English, French, Spanish, and Chinese). 
  Macula Hebrew and Greek encode domains and references from these resources at the word level for most OT and NT words.
* openbible.info [Bible Geocoding Data](https://github.com/openbibleinfo/Bible-Geocoding-Data)
* Robert Rouse's [theographic-bible-metadata](https://github.com/robertrouse/theographic-bible-metadata) (aka [viz.bible](https://viz.bible))
* [STEPBible](https://www.stepbible.org) [TIPNR](https://github.com/STEPBible/STEPBible-Data/blob/master/TIPNR%20-%20Translators%20Individualised%20Proper%20Names%20with%20all%20References%20-%20STEPBible.org%20CC%20BY.txt) 
  * Patristic Text Archive [JSON/XML versions of TIPNR](https://github.com/PatristicTextArchive/tipnr_data) (with persons and places separated)
* Copenhagen Alliance [versification-specification](https://github.com/Copenhagen-Alliance/versification-specification).
  Bible references within this data reflect the 'ORG' scheme specified by the Copenhagen Alliance. This means that
  Old Testament references assume the versification structure of the Hebrew Bible, and New Testament references assume
  the structure of the Greek New Testament. For use with translations, the references may need to be be converted to the
  Copenhagen Alliance 'ENG' scheme. The repo cited above has information and sample code for how to achieve that; if 
  assistance is needed please contact us.

Each of these sources are available as CC-BY-4.0 or CC-BY-SA-4.0 licensed data.

In particular, the definitions provided by the UBS Dictionaries supply a decent starting point and several of our English 
place descriptions are directly inspired by these definitions. We owe much to the UBS team (and Reinier DuBlois 
in particular) for their work and for their licensing of the material under a CC-BY-SA-4.0 license.

In addition to these sources, BiblioNexus have done a significant amount of curation and supplementation 
in order to account for and model the data according to the needs of the ACAI project. 

## Aggregation

This process started with Biblica's **Macula Hebrew** and **Macula Greek** data, which has word-level
semantic domain annotations from the _UBS Dictionary of Biblical Hebrew_ (UBSDBH) and _UBS 
Dictionary of Biblical Greek_ (UBSDBG). This was used in an initial pass to identify explicitly named people and places. 

We next processed data from [openbible.info](https://openbible.info), [viz.bible](https://viz.bible), and 
[STEPBible's](https://www.stepbible.org) TIPNR data to prepare place data to be integrated into one cohesive set.

Upon processing these datasets, we realized that STEPBible's TIPNR data did the best job of the lot of grouping together 
different methods of referring to the same location. So it made sense to begin with the TIPNR data as a basic representation, 
incorporate the semantic, instance, and referent information aggregated from the UBS Dictionaries and from the Macula 
datasets, and then fold in data from openbible.info and viz.bible. 

We identified similar entities from the different datasets for merging through a comparison of labeling and known 
references. We then merged this data together with data that modeled relationships between places (and, importantly, 
curated descriptions of the locations) that had been on a separate development/curation track. In that merge, 
we considered this data primary and at times had to re-arrange our snapshot of the TIPNR data to support the merge.

## Status / Completeness of Project

While we believe we've identified places explicitly named in the Bible and associated references with them, there are 
some aspects of this data that are not complete. 

### Areas Still Under Development

* **Subregions:** A significant amount of work has been done with subregions, but there is still more to do.
* **Nearby Places:** What exists is fairly subjective, we plan on using coordinate data to help identify nearby places
  and then curate that information to relevant nearby places.

The work on _Subregions_ and _Nearby Places_ is incomplete and left as-is for the v1.0 release. We may decide to 
pursue completing this work in the future, and we may not.

Word-level references, particularly within the Hebrew Bible, may also have omissions. The 
_UBS Dictionary of the Hebrew Bible_ remains a work in progress, and not all word tokens of the Hebrew Bible have been 
analyzed. Also, the Macula analysis of the Hebrew Bible is not as developed as its Greek New Testament counterpart,
and the referent data information can only be considered to be an initial draft.

## JSON Schema Documentation

This documentation represents the current (as of 2024-01-22) schema and is based on the Python dataclasses used 
while processing the place-specific data. We will do our best to keep this up to date, but there may be discrepancies.

### AcaiPlaceEntry

<table>
<tr><td><b>property</b></td><td><b>type</b></td><td><b>description</b></td></tr>
<tr><td>id</td><td>string</td><td>a string representing the unique identifier of this place (e.g. `place:Rome`)</td></tr>
<tr><td>primary_id</td><td>string</td><td>a place that has multiple representations has a primary entry identified by this string. The primary entry is identified where `primary_id` == `id`.</td></tr>
<tr><td>alternate_sources</td><td>AlternateSources dataclass</td><td>a dataclass that allows each possible alternate source to provide some information</td></tr>
<tr><td>type</td><td>string</td><td>for places, `place` is the only valid type</td></tr>
<tr><td>ubsdbg</td><td>list</td><td>a list of domain.article (##.##) strings representing the UBSDBG annotation</td></tr>
<tr><td>ubsdbh</td><td>list</td><td>a list of strings representing the article identifier(s) from UBSDBH</td></tr>
<tr><td>localizations</td><td>dict[str, dict[str, list]]</td><td>an object for collecting strings and other structures by language for localization purposes. This is where `preferred_label`, `alternate_labels`, and `description` are collected.</td></tr>
<tr><td>referred_to_as</td><td>list</td><td>a list of `id` for places/locations that are considered functionally equivalent</td></tr>
<tr><td>possibly_same_as</td><td>list</td><td>a list of `id` for places/locations that may be the same location. This is less sure that `referred_to_as`.</td></tr>
<tr><td>tribal_area</td><td>string</td><td>the `id` of ACAI group representing the tribe/nationality associated with the location</td></tr>
<tr><td>associated_places</td><td>list</td><td>a list of `id` for places/locations that are associated for some reason. An example is Sodom and Gomorrah.</td></tr>
<tr><td>nearby_places</td><td>list</td><td>a list of `id` for places/locations that are nearby (as determined by human curation, not by geographic comparison).</td></tr>
<tr><td>subregion_of</td><td>list</td><td>a list of `id` for places/locations that the current location is to be considered a subregion of.</td></tr>
<tr><td>mentioned_in_bible</td><td>bool</td><td>If `TRUE` this place is mentioned in the Bible (note: "Bible" includes the canon of the protestant edition of the NRSV with apocrypha).</td></tr>
<tr><td>only_mentioned_in_apocrypha</td><td>bool</td><td>If `TRUE` this place is only mentioned in the apocryphal portions of the Bible (note: here "apocrypha" are the apocryphal books of the protestant edition of the NRSV with apocyrpha).</td></tr>
<tr><td>non_biblical</td><td>bool</td><td>If `TRUE` there is no mention whatever of this location in the Bible. These are included to provide context and typically also include `geocoordinates` data.</td></tr>
<tr><td>is_artifact</td><td>bool</td><td>The identification is restricted to a human-created structure, such as a gate or pillar.</td></tr>
<tr><td>is_person</td><td>bool</td><td>Some locations are innately associated with people.</td></tr>
<tr><td>added_entry</td><td>bool</td><td>Used only during creation of data, not relevant for any future use.</td></tr>
<tr><td>lemmas</td><td>dict[str, list]</td><td>The key is the language (`el`, `he`, or `arc`) with lemmas as values in the list.</td></tr>
<tr><td>place_types</td><td>dict[str, list]</td><td>The key is the place-type scheme (`obi`, `vizbible`, `acai`, etc.) with values. Note that <b>acai</b> is to be considered the default. These values, along with descriptions and hierarchy, <a href="https://github.com/Clear-Bible/ACAI/blob/main/data/places/Biblical%20Places%20Guidelines.md#type">are available here</a>.</td></tr>
<tr><td>geocoordinates</td><td>dict[str, dict[str, str]]</td><td>A dictionary with various sources of latitude and longitude (point-based) for the location. The default (preferred) source is <b>biblica-maps</b>.</td></tr>
<tr><td>key_references</td><td>list</td><td>A list of BCV8 style references, where eight digits encode the zero-padded book (two digits), chapter (three digits), and verse (three digits) of the reference: `BBCCCVVV`. Note these references reflect the versification of the Hebrew Bible and Greek New Testament via the Copenhagen Alliance 'ORG' scheme.</td></tr>
<tr><td>references</td><td>list</td><td>A list of BCV8 style references, where eight digits encode the zero-padded book (two digits), chapter (three digits), and verse (three digits) of the reference: `BBCCCVVV`. Note these references reflect the versification of the Hebrew Bible and Greek New Testament via the Copenhagen Alliance 'ORG' scheme.</td></tr>
<tr><td>explicit_instances</td><td>dict[str, list]</td><td>initial key is edition (SBLGNT, WLC), list is corpus-specific word references where a 13 digit string encodes the reference to the word part position: `[on]BBCCCVVVWWWP`. Note these references reflect the versification of the Hebrew Bible and Greek New Testament via the Copenhagen Alliance 'ORG' scheme.</td></tr>
<tr><td>pronominal_referents</td><td>dict[str, list]</td><td>initial key is edition (SBLGNT, WLC), list is corpus-specific word references where a 13 digit string encodes the reference to the word part position: `[on]BBCCCVVVWWWP`. Note these references reflect the versification of the Hebrew Bible and Greek New Testament via the Copenhagen Alliance 'ORG' scheme.</td></tr>
<tr><td>subject_referents</td><td>dict[str, list]</td><td>initial key is edition (SBLGNT, WLC), list is corpus-specific word references where a 13 digit string encodes the reference to the word part position: `[on]BBCCCVVVWWWP`. Note these references reflect the versification of the Hebrew Bible and Greek New Testament via the Copenhagen Alliance 'ORG' scheme.</td></tr>
<tr><td>speeches</td><td>dict[str, list[dict[str, obj]]]</td><td>initial key is edition (SBLGNT, WLC), list is word-level information regarding reported speech the entity is responsible for. Each speech has a `quote_type` property (usually `Normal` but sometimes `Questioning` or other contextually important data) as well as `words`;a list of corpus-specific word references where a 13 digit string encodes the reference to the word part position: `[on]BBCCCVVVWWWP`. Note these references reflect the versification of the Hebrew Bible and Greek New Testament via the Copenhagen Alliance 'ORG' scheme.</td></tr>
</table>

### AlternateSources

<table>
<tr><td><b>property</b></td><td><b>type</b></td><td><b>description</b></td></tr>
<tr><td>aquifer</td><td>list</td><td>A pipe-delimited string (id|name|resource) derived from aquifer.bible</td></tr>
<tr><td>obi</td><td>list</td><td>Information derived from openbible.info</td></tr>
<tr><td>ubsdbh</td><td>list</td><td>Information derived from the <i>UBS Dictionary of Biblical Hebrew</i></td></tr>
<tr><td>ubsdbg</td><td>list</td><td>Information derived from the <i>UBS Dictionary of New Testament Greek</i></td></tr>
<tr><td>digital_atlas_roman_empire</td><td>list</td><td>Relevant URL and ID from the <i>Digital Atlas of the Roman Empire</i>, extracted from OpenBible.info data</td></tr>
<tr><td>pleiades</td><td>list</td><td>Relevant URL and ID from the <a href="https://pleiades.stoa.org/places/">Pleiades Project</a>, extracted from OpenBible.info data</td></tr>
<tr><td>tipnr</td><td>list</td><td>Relevant ID from Tyndale House's StepBible project, <i>Translators Individualized Proper Names with all References</i> (TIPNR), extracted from OpenBible.info data</td></tr>
<tr><td>wikidata</td><td>list</td><td>Relevant ID from wikidata, extracted from OpenBible.info data</td></tr>
<tr><td>wikipedia</td><td>list</td><td>Relevant ID from wikidata, extracted from OpenBible.info data</td></tr>
</table>
