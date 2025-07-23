# ACAI Release: 2025-07-23

The ACAI project annotates information about people and places in the Bible. Specifically, it annotates the original languages at the word and phrase level for specific instances of people, places, and other entities. When used with a word-level alignment to a translation of the Bible (see Biblica's [Alignments](https://github.com/Clear-Bible/Alignments)) this information can be useful in all sorts of translation contexts.

ACAI also contains information about those entities including a preferred label, description, and information about relationships with other entities.

As you encounter issues or have questions, please contact Rick Brannan at rick.brannan@biblionexus.org.

# License

This release of the ACAI data (the JSON and Markdown forms included here) is under a Creative Commons CC-BY-SA 4.0 license. See [LICENSE.md](LICENSE.md) for more details.

# Identifiers

Identifiers in the ACAI ecosystem consist of two parts. The first part represents the type of identifier (e.g. people, places, deities, groups, fauna, flora, realia, keyterms). The second part is a unique identifier representing the specific record. For example, the identifier for **Aaron** as a person is `person:Aaron`.

## Primary Identifiers

The structure of the JSON is flat; we simply have all the records of a single type (e.g. people) in individual JSON files in the ACAI type folder/directory. The JSON files are named with the identifier, sans type, as the filename. For example, the JSON file for Aaron as a person is `Aaron.json`.

However, there are many people like **Abraham** who are known by more than one name within the biblical canon. Each of these forms of **Abraham** has a separate record encoded as JSON, so we have both  `Abraham.json` and `Abram.json`. When multiple forms of a thing exist, it is useful to know which is the primary form. Each record contains an `id` and a `primary_id`. When `id` and `primary_id` for a record match, the record can be considered the primary form of the record; the other forms are encoded in the `referred_to_as` list contained elsewhere in the record. The primary record contains data for all forms of the entity, in word level references, pronominal referents, and subject referents. The non-primary records only contain references to the specific form of the record (e.g. **Abram**).

The specification of primary and non-primary records is consistent through all ACAI types.

In most applications (“where are all the places ‘Abraham’ occurs in the Bible?”), it is anticipated that the information in the primary record is what will be required.

# Descriptions

Each record contains a `localizations` object that contains a `preferred_label` and a `description`. The `description` is a curated, free-text description of the entity. The JSON records support localization and in the future may have material in languages beside English.

# Included Data

The data included in this release is a snapshot of the data as of 2025-07-23. It includes JSON files and Markdown files for each record. The Markdown files are generated from the JSON files (along with some Berean Standard Bible [text alignment data](https://github.com/Clear-Bible/Alignments)). They are only included as a visualization of the data within the JSON and not intended to direct or dictate how the JSON data should be used or rendered.

* [people ReadMe](people/README.md)
  * [Markdown Index](people/md/00-Index.md)
* [places ReadMe](places/README.md)
  * [Markdown Index](places/md/00-Index.md)
* [deities ReadMe](deities/README.md)
  * [Markdown Index](deities/md/00-Index.md)
* [groups ReadMe](groups/README.md)
  * [Markdown Index](groups/md/00-Index.md)
* [fauna ReadMe](fauna/README.md)
  * [Markdown Index](fauna/md/00-Index.md)
* [flora ReadMe](flora/README.md)
  * [Markdown Index](flora/md/00-Index.md)
* [realia ReadMe](realia/README.md)
  * [Markdown Index](realia/md/00-Index.md)
* [keyterms ReadMe](keyterms/README.md)
  * [Markdown Index](keyterms/md/00-Index.md)
# Sources

* Biblica/Clear-Bible's [Macula Hebrew](https://github.com/Clear-Bible/macula-hebrew)
* Biblica/Clear-Bible's [Macula Greek](https://github.com/Clear-Bible/macula-greek)
* Biblica/Clear-Bible's [speaker-quotations](https://github.com/Clear-Bible/speaker-quotations), an attempt to identify the original language words, in both the Old and New Testaments, translated as quotations (material using “double” and ‘single’ quotation marks) in various English Bibles. It also attempts to associate speakers with the quotations, where possible, using data from Faith Comes By Hearing.
* United Bible Societies' _UBS Dictionary of Biblical Hebrew_ (UBSDBH) and _UBS Dictionary of the Greek New Testament_ (UBSDGNT). See [SemanticDictionary.org](https://semanticdictionary.org/) for an implementation and the git repo [ubs-open-license](https://github.com/ubsicap/ubs-open-license) for data (English, French, Spanish, and Chinese). Macula Hebrew and Greek encode domains and references from these resources at the word level for most OT and NT words.
* United Bible Societies' _Thematic Lexicons_. The UBS recently (March 2025) issued their highly useful _Thematic Lexicons_ under an open license. There are three Thematic Lexicons, one for _Flora_ (plants), one for _Fauna_ (animals), and one for _Realia_ (man-made things). These are available in the [ubs-open-license](https://github.com/ubsicap/ubs-open-license/tree/main/flora-fauna-realia) github repo.
* United Bible Societies' _Key Term_ data from Paratext. This is used by permission.
* openbible.info [Bible Geocoding Data](https://github.com/openbibleinfo/Bible-Geocoding-Data)
* Robert Rouse's [theographic-bible-metadata](https://github.com/robertrouse/theographic-bible-metadata) (aka [viz.bible](https://viz.bible))
* [STEPBible](https://www.stepbible.org) [TIPNR](https://github.com/STEPBible/STEPBible-Data/blob/master/TIPNR%20-%20Translators%20Individualised%20Proper%20Names%20with%20all%20References%20-%20STEPBible.org%20CC%20BY.txt) 
  * Patristic Text Archive [JSON/XML versions of TIPNR](https://github.com/PatristicTextArchive/tipnr_data) (with persons and places separated)
* Copenhagen Alliance [versification-specification](https://github.com/Copenhagen-Alliance/versification-specification). Bible references within this data reflect the 'ORG' scheme specified by the Copenhagen Alliance. This means that Old Testament references assume the versification structure of the Hebrew Bible, and New Testament references assume the structure of the Greek New Testament. For use with translations, the references may need to be be converted to the Copenhagen Alliance 'ENG' scheme. The repo cited above has information and sample code for how to achieve that; if assistance is needed please contact us.

Unless mentioned otherwise, each of these sources are available as CC-BY-4.0 or CC-BY-SA-4.0 licensed data.

