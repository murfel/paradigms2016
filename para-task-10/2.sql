select country.name, max(literacyrate.rate)
from (literacyrate join country on country.code = literacyrate.countrycode)
group by country.name having literacyrate.year = max(literacyrate.year)
order by literacyrate.rate desc limit 1;
