update nations
set age = :age,
    money = :money,
    morale = :morale,
    tax_rate = :tax_rate,
    elite = :elite,
    army_spending = :army_spending,
    ruler = :ruler
where id = :id
