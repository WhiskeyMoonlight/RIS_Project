select orderDate, hall_name, avans, realPrice, surname
from banquet_order.orders ord join banquet_order.restauranthall r_hall on (ord.hallId = r_hall.hall_id)
join banquet_order.manager man on (man.idmanager = ord.managerId)
where month(ord.orderDate) = '$month' AND year(ord.orderDate) = '$year';