select man.*
from banquet_order.manager man
         left join
     (select managerId, idorder
      from banquet_order.orders ord
      where month(ord.orderDate) = '$month'
        AND year(ord.orderDate) = '$year') order_to_check on (man.idmanager = order_to_check.managerId)
where order_to_check.idorder is NULL;