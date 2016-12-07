select name, max(rate) from
(select country.name, literacyrate.rate
from country join literacyrate on country.code = literacyrate.countrycode
group by country.code
having literacyrate.year = max(literacyrate.year));
