// Add to cart
$('.btn-add-cart').on('click', function(e) {
    pname = $(this).attr('data-pname');
    pdesc = $(this).attr('data-desc');
    price = $(this).attr('data-price');
    pimg = $(this).attr('data-pimg');
    pcat = $(this).attr('data-pcat');

    var data = {
        "p_name": pname,
        "p_desc": pdesc,
        "p_price": price,
        "p_img": pimg,
        "p_cat": pcat
    };

    if ($(this).children().hasClass('bi-cart-plus')) {
        $this = $(this);
        $this.html('');
        $this.html('<i class="bi bi-check2 me-2"></i>Added to cart');
        if ($this.hasClass('btn-outline-secondary')) {
            $this.removeClass('btn-outline-secondary');
            $this.addClass('btn-secondary')
        }
        $.ajax({
            url: "/api/cart/add",
            type: "POST",
            contentType: "application/json",
            data: JSON.stringify(data),
            success: function() {
                $this.html('');
                $this.html('<i class="bi bi-check2 me-2"></i>Added to cart');
                if ($this.hasClass('btn-outline-secondary')) {
                    $this.removeClass('btn-outline-secondary');
                    $this.addClass('btn-secondary')
                }
            },
            error: function(error) {
                $this.html('');
                $this.html('<i class="bi bi-cart-plus me-2"></i>Add to cart');
                if ($this.hasClass('btn-secondary')) {
                    $this.removeClass('btn-secondary');
                    $this.addClass('btn-outline-secondary')
                }
            }
        });
    } else {
        $this = $(this);
        $this.html('');
        $this.html('<i class="bi bi-cart-plus me-2"></i>Add to cart');
        if ($this.hasClass('btn-secondary')) {
            $this.removeClass('btn-secondary');
            $this.addClass('btn-outline-secondary')
        }
        $.ajax({
            url: "/api/cart/remove",
            type: "POST",
            contentType: "application/json",
            data: JSON.stringify(data),
            success: function() {
                $this.html('');
                $this.html('<i class="bi bi-cart-plus me-2"></i>Add to cart');
                if ($this.hasClass('btn-secondary')) {
                    $this.removeClass('btn-secondary');
                    $this.addClass('btn-outline-secondary')
                }
            },
            error: function() {
                $this.html('');
                $this.html('<i class="bi bi-check2 me-2"></i>Added to cart');
                if ($this.hasClass('btn-outline-secondary')) {
                    $this.removeClass('btn-outline-secondary');
                    $this.addClass('btn-secondary')
                }
            }
        });
    }
});

// Remove from cart
$('.remove-from-cart').on('click', function(e) {
    itemName = $(this).parents('.product-price-section').prev().find('.product-name').html();
    pname = $(this).attr('data-pname');
    pdesc = $(this).attr('data-desc');
    price = $(this).attr('data-price');
    pimg = $(this).attr('data-pimg');
    pcat = $(this).attr('data-pcat');

    var data = {
        "p_name": pname,
        "p_price": price,
        "p_desc": pdesc,
        "p_img": pimg,
        "p_cat": pcat
    };
    $this = $(this).parents('.cart-item')
    d = new Dialog('Remove from cart', 'Are you sure want to remove the <b>' + itemName + '</b> from the cart?');
    d.setButtons([{
            'name': "Cancel",
            "class": "btn-secondary",
            "onClick": function(event) {
                $(event.data.modal).modal('hide');
            }
        },
        {
            'name': "Remove",
            "class": "btn-danger",
            "onClick": function(event) {
                $.ajax({
                    url: "/api/cart/remove",
                    type: "POST",
                    contentType: "application/json", // Set the Content-Type header
                    data: JSON.stringify(data),
                    success: function() {
                        $this.remove();
                        updateOrderSummary()
                    },
                    error: function(error) {
                        console.error(error);
                    }
                });

                $(event.data.modal).modal('hide')
            }
        }
    ]);
    d.show();
})

// Update order summary details
function updateOrderSummary() {
    var prices = $('.total-item-price').map(function() {
        return parseFloat($(this).text());
    }).get();

    let sum = 0;

    for (let i = 0; i < prices.length; i++) {
        sum += prices[i];
    }

    shipping_cost = parseInt($('.cart-shipping-cost').text());
    $('.cart-subtotal').text(sum);
    $('.cart-total').text(sum + shipping_cost);
}

// Update cart quantity
$('.btn-update-cart').on('click', function(e) {
    e.preventDefault();
    var $this = $(this);
    var data = [];


    $('.cart-item').each(function() {
        pname = $(this).data('pname');
        pdesc = $(this).data('desc');
        price = $(this).data('price');
        pimg = $(this).data('pimg');
        pcat = $(this).data('pcat');
        quantity = $(this).find('.product-quantity').text();
        data.push({
            "p_name": pname,
            "p_price": parseInt(price),
            "p_desc": pdesc,
            "p_img": pimg,
            "p_cat": pcat,
            "qty": parseInt(quantity)
        });
    });

    var oldHtml = $this.html();
    var spinner = `<div class="spinner-border spinner-border-sm text-body me-2" role="status"></div>`
    $this.html(spinner + 'Updating...');
    $this.attr('disabled', true);
    $.ajax({
        url: "/api/cart/update",
        type: "POST",
        contentType: "application/json",
        data: JSON.stringify(data),
        success: function() {
            location.reload();
        },
        error: function() {
            $this.html(oldHtml);
            $this.removeAttr('disabled')
        }
    });
})

// Increase count of items
$('.items-increase').click(function(e) {
    c_qty = parseInt($(this).prev().html());
    max = parseInt($(this).prev().attr('data-max'))
    total_price_el = $(this).parents('.quantity-section').next().find('.total-item-price');
    original_price = parseInt($(this).parents('.quantity-section').prev().find('.price-per-item').html())
    if (max > c_qty) {
        c_qty += 1;
        new_price = original_price + parseInt(total_price_el.html())
        total_price_el.html(new_price)
    }
    $(this).prev().html(c_qty);
    updateOrderSummary()
});

// Decrease count of items
$('.items-decrease').click(function(e) {
    c_qty = parseInt($(this).next().html());
    total_price_el = $(this).parents('.quantity-section').next().find('.total-item-price');
    original_price = parseInt($(this).parents('.quantity-section').prev().find('.price-per-item').html())
    if (c_qty > 1) {
        c_qty -= 1;
        new_price = parseInt(total_price_el.html()) - original_price
        total_price_el.html(new_price)
    }
    $(this).next().html(c_qty);
    updateOrderSummary()
});

// Empty cart
$('.btn-empty-cart').on('click', function(e) {
    e.preventDefault();
    var $this = $(this);
    var token = $this.data('token');

    data = {
        "token": parseInt(token)
    }

    $.ajax({
        url: "/api/cart/empty",
        type: "POST",
        contentType: "application/json",
        data: JSON.stringify(data),
        success: function() {
            window.location.href = "/"
        },
        error: function() {
            $this.text("Can't empty the cart")
            console.error("Can't empty the cart");
        }
    });
});

if (window.location.pathname == '/checkout') {
    $(document).ready(function() {
        // Function to check if all form fields are filled
        function checkForm() {
            var formFilled = true;

            // Check each input field in the form
            $('#checkout-form input').each(function() {
                if ($(this).val() === '') {
                    formFilled = false;
                    return false; // Exit the loop if any field is empty
                }
            });

            // Enable or disable the submit button based on the formFilled variable
            if (formFilled) {
                $('.btn-review-order').removeClass('disabled');
            } else {
                $('.btn-review-order').addClass('disabled');
            }
        }

        // Call the checkForm function whenever a form field changes
        $('#checkout-form input').on('input', checkForm);
    });
}

// Remove item from menu
$('.btn-remove-menu-item').on('click', function() {
    itemName = $(this).parents('.item-action').prev().prev().html();
    item_name = $(this).data('name');
    item_category = $(this).data('category');
    item_image = $(this).data('image');

    var data = {
        "name": item_name,
        "category": item_category,
        "image": item_image
    };
    $this = $(this).parents('.menu-item')
    console.log($this);
    d = new Dialog('Remove Item from Menu', 'Are you sure want to remove the <b>' + itemName + '</b> from the menu?');
    d.setButtons([{
            'name': "Cancel",
            "class": "btn-secondary",
            "onClick": function(event) {
                $(event.data.modal).modal('hide');
            }
        },
        {
            'name': "Remove",
            "class": "btn-danger",
            "onClick": function(event) {
                $.ajax({
                    url: "/api/menu/remove",
                    type: "POST",
                    contentType: "application/json", // Set the Content-Type header
                    data: JSON.stringify(data),
                    success: function() {
                        $this.remove();
                    },
                    error: function(error) {
                        console.error(error);
                    }
                });

                $(event.data.modal).modal('hide')
            }
        }
    ]);
    d.show();
});

$('.btn-remove-order').on('click', function(e) {
    e.preventDefault();
    var $this = $(this);
    var p1 = $this.parents('.user-order');
    var order_id = $this.data('id');
    var token_id = $this.data('token');
    var is_show = $this.data('show');

    data = {
        "order_id": parseInt(order_id),
        "token_id": parseInt(token_id)
    }

    d = new Dialog('Confirm deliver', 'Are you sure want to deliver <b>#' + token_id + '</b>?');
    d.setButtons([{
            'name': "Cancel",
            "class": "btn-secondary",
            "onClick": function(event) {
                $(event.data.modal).modal('hide');
            }
        },
        {
            'name': "Deliver",
            "class": "btn-success",
            "onClick": function(event) {
                $.ajax({
                    url: "/api/order/remove",
                    type: "POST",
                    contentType: "application/json",
                    data: JSON.stringify(data),
                    success: function() {
                        console.log("removed order!");
                        if (is_show == true) {
                            window.location.pathname = "/admin/orders"
                        } else {
                            p1.remove();
                            location.reload();
                        }
                    },
                    error: function(error) {
                        console.error(error);
                    }
                });

                $(event.data.modal).modal('hide')
            }
        }
    ]);
    d.show();
});