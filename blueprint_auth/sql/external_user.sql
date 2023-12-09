select user_id, NULL as user_group
from banquet_order.external_users
where login = '$login'
  and password = '$password';