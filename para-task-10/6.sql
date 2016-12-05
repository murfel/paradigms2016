select city.name, city.population, country.population from city
join country on country.code = city.countrycode
order by city.population / country.population desc, city.name desc limit 20;
