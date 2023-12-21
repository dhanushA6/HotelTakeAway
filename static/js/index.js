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
    console.log(data);
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