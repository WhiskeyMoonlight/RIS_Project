select idmanager, surname, count(*) as order_num, sum(realPrice) as full_price
from banquet_order.orders ord
         join banquet_order.manager man on (ord.managerId = man.idmanager)
where month(ord.orderDate) = '03'
  AND year(ord.orderDate) = 2020
group by idmanager;
