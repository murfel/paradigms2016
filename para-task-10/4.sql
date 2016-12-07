select country.name, count(city.id) as citycount
from country left join city on country.code = city.countrycode
and city.population >= 1000000
group by country.name
order by citycount desc, country.name;
