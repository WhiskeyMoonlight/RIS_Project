select user_id, user_group
from banquet_order.internal_users
where login = '$login'
  and password = '$password';
