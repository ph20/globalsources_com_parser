#!/bin/bash
sqlite3 company_db.sqlite <<!
.headers on
.mode csv
.output globalsources_parsed.csv
SELECT id, name, about, url_card, site, country, address_index, city, province, address, tel, fax, person, stars, exporter, importer, email FROM company;
!
