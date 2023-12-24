import wrapper as wp


orders_list = wp.get_orders_list()

# for order in orders_list:
#     wp.add_subscriber(order.customer.email)

print(wp.get_subscriber())