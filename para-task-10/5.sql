select governmentform, sum(surfacearea) as totalarea from country
group by governmentform
order by totalarea desc limit 1;
