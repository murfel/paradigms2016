select country.name, max(literacyrate.rate) from literacyrate
join country on country.code = literacyrate.countrycode;
