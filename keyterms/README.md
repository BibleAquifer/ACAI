# ACAI KeyTerm Data

**Initial Edition**, v1.00, 2025-07-23

Rick Brannan, rickb@missionmutual.org, and Jessica Parks, jessicap@missionmutual.org

## Context

Mission Mutual and Biblica are working together to create data representing explicit and implicit instances of 
people and places (and other things) in the Bible. This information is being compiled as part of the ACAI project, 
the _Aquifer Concept Architecture for Information_, which itself is a part of the [Bible Aquifer](https://www.notion.so/etenlab/Aquifer-Home-c88f20c13eb440539a9ec532ca30b78a) project.

## Sources

* Biblica/Clear-Bible's [Macula Hebrew](https://github.com/Clear-Bible/macula-hebrew)
* Biblica/Clear-Bible's [Macula Greek](https://github.com/Clear-Bible/macula-greek)
* United Bible Societies' _UBS Dictionary of Biblical Hebrew_ (UBSDBH) and _UBS Dictionary of the Greek New Testament_
  (UBSDGNT). See [SemanticDictionary.org](https://semanticdictionary.org/) for an implementation and the git repo
  [ubs-open-license](https://github.com/ubsicap/ubs-open-license) for data (English, French, Spanish, and Chinese). 
  Macula Hebrew and Greek encode domains and references from these resources at the word level for most OT and NT words.
* United Bible Societies' Key Terms data from Paratext, which has been instrumental in providing the initial
  structure for the KeyTerm data. This data is used by permission.
* Copenhagen Alliance [versification-specification](https://github.com/Copenhagen-Alliance/versification-specification).
  Bible references within this data reflect the 'ORG' scheme specified by the Copenhagen Alliance. This means that
  Old Testament references assume the versification structure of the Hebrew Bible, and New Testament references assume
  the structure of the Greek New Testament. For use with translations, the references may need to be be converted to the
  Copenhagen Alliance 'ENG' scheme. The repo cited above has information and sample code for how to achieve that; if 
  assistance is needed please contact us.

Each of these sources are available as CC-BY-4.0 or CC-BY-SA-4.0 licensed data.

Mission Mutual have done a significant amount of curation and supplementation 
in order to account for and model the data according to the needs of the ACAI project. 

### About Paratext Key Term Data

The Paratext application (from UBS) has functionality built around _key terms_ that translators rely on. Paratext 
supplies data for this functionality. UBS (or other parties) do not claim copyright on the underlying data, and 
when we (Mission Mutual) inquired about using this data as basis for Key Term data in ACAI, they enthusiastically 
endorsed the usage.

Please note that the set of key term data that we have used as basis is not necessarily exhaustive (though in many if 
not most cases it is exhaustive), but it does mark instances of key terms that translators have identified as necessary 
to review.

Mission Mutual has done significant work to curate and supplement the Paratext Key Term data. This includes, 
but is not limited to:
* grouping entries into primary and secondary relationships
* revising descriptions
* adding key passages to each entry
* determining preferred labels for each entry
* using Biblica's MACULA data to identify referents

There are likely areas where others may consider some key terms missed, and other areas where items marked as key terms 
may not be considered key terms by others. This is a consequence of the problem of key terms: everything can't be _key_; 
decisions have to be made. As a result, the current implementation is best viewed as a starting point.

## Status / Completeness of Project

We have aggregated as much KeyTerm data as possible from available sources. 

### Areas Still Under Development

Word-level references, particularly within the Hebrew Bible, may also have omissions. The 
_UBS Dictionary of the Hebrew Bible_, which portions of the word-level analysis are based on,
remains a work in progress, and not all word tokens of the Hebrew Bible have been analyzed. 
Also, the Macula analysis of the Hebrew Bible is not as developed as its Greek New Testament counterpart,
and the referent data information can only be considered to be an initial draft.

## JSON Schema Documentation

This documentation represents the current (as of 2025-07-18) schema and is based on the Python dataclasses used 
while processing the place-specific data. We will do our best to keep this up to date, but there may be discrepancies.

### AcaiKeyTermEntry

<table>
<tr><td><b>property</b></td><td><b>type</b></td><td><b>description</b></td></tr>
<tr><td>id</td><td>string</td><td>a string representing the unique identifier of this group (e.g. `group:Pharisees`)</td></tr>
<tr><td>primary_id</td><td>string</td><td>a group that has multiple representations has a primary entry identified by this string. The primary entry is identified where `primary_id` == `id`.</td></tr>
<tr><td>alternate_sources</td><td>AlternateSources dataclass</td><td>a dataclass that allows each possible alternate source to provide some information</td></tr>
<tr><td>type</td><td>string</td><td>for key terms, `keyterm` is the only valid type</td></tr>
<tr><td>keyterm_type</td><td>string</td><td>valid types: `attributes`, `rituals`, `miscellaneous`.</td></tr>
<tr><td>ubsdbg</td><td>list</td><td>a list of domain.article (##.##) strings representing the UBSDBG annotation</td></tr>
<tr><td>ubsdbh</td><td>list</td><td>a list of strings representing the article identifier(s) from UBSDBH</td></tr>
<tr><td>localizations</td><td>dict[str, dict[str, list]]</td><td>an object for collecting strings and other structures by language for localization purposes. This is where `preferred_label`, `alternate_labels`, and `description` are collected.</td></tr>
<tr><td>referred_to_as</td><td>list</td><td>a list of `id` for other entities that are considered functionally equivalent</td></tr>
<tr><td>only_mentioned_in_apocrypha</td><td>bool</td><td>If `TRUE` this group is only mentioned in the apocryphal portions of the Bible (note: here "apocrypha" are the apocryphal books of the protestant edition of the NRSV with apocyrpha).</td></tr>
<tr><td>non_biblical</td><td>bool</td><td>If `TRUE` there is no mention whatever of this group in the Bible.</td></tr>
<tr><td>lemmas</td><td>dict[str, list]</td><td>The key is the language (`el`, `he`, or `arc`) with lemmas as values in the list.</td></tr>
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
<tr><td>ubsfauna</td><td>list</td><td>Pointer to relevant article in the <i>UBS Thematic Lexicon: Fauna</i></td></tr>
<tr><td>ubsflora</td><td>list</td><td>Pointer to relevant article in the <i>UBS Thematic Lexicon: Flora</i></td></tr>
<tr><td>ubsrealia</td><td>list</td><td>Pointer to relevant article in the <i>UBS Thematic Lexicon: Realia</i></td></tr>
<tr><td>digital_atlas_roman_empire</td><td>list</td><td>Relevant URL and ID from the <i>Digital Atlas of the Roman Empire</i>, extracted from OpenBible.info data</td></tr>
<tr><td>pleiades</td><td>list</td><td>Relevant URL and ID from the <a href="https://pleiades.stoa.org/places/">Pleiades Project</a>, extracted from OpenBible.info data</td></tr>
<tr><td>tipnr</td><td>list</td><td>Relevant ID from Tyndale House's StepBible project, <i>Translators Individualized Proper Names with all References</i> (TIPNR), extracted from OpenBible.info data</td></tr>
<tr><td>wikidata</td><td>list</td><td>Relevant ID from wikidata, extracted from OpenBible.info data</td></tr>
<tr><td>wikipedia</td><td>list</td><td>Relevant ID from wikidata, extracted from OpenBible.info data</td></tr>
</table>
