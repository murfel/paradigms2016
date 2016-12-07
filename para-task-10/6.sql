select city.name, city.population, country.population
from city join country on city.countrycode = country.code
order by 100.0 * city.population / country.population desc, city.name desc limit 20;
