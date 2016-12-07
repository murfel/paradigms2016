select city.name from capital
join city on city.id = capital.cityid
join country on country.code = capital.countrycode
where country.name like "Malaysia";
