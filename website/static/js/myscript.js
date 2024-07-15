$(document).ready(function() {
    // Initialize Owl Carousel
    $('#slider1, #slider2, #slider3').owlCarousel({
        loop: true,
        margin: 20,
        responsiveClass: true,
        responsive: {
            0: {
                items: 2,
                nav: false,
                autoplay: true,
            },
            600: {
                items: 4,
                nav: true,
                autoplay: true,
            },
            1000: {
                items: 6,
                nav: true,
                loop: true,
                autoplay: true,
            }
        }
    });

    // Plus-cart action
    $('.plus-cart').click(function() {
        var id = $(this).attr("pid").toString();
        var eml = this.parentNode.children[2];

        $.ajax({
            type: "GET",
            url: "/pluscart",
            data: { prod_id: id },
            success: function(data) {
                window.location.href = data.redirect_url;
                if (data.quantity !== undefined && data.amount !== undefined && data.totalamount !== undefined) {
                    eml.innerText = data.quantity;
                    var amountElement = document.getElementById("amount");
                    var totalAmountElement = document.getElementById("totalamount");

                    if (amountElement && totalAmountElement) {
                        amountElement.innerText = "Rs. " + data.amount.toFixed(2);
                        totalAmountElement.innerText = "Rs. " + data.totalamount.toFixed(2);
                    } else {
                        console.error('Element with id="amount" or id="totalamount" not found');
                    }
                } else {
                    console.error('Incomplete data returned from server:', data);
                }
            },
            error: function(xhr, status, error) {
                console.error('Failed to update cart:', error);
            }
        });
    });

    // Minus-cart action
    $('.minus-cart').click(function() {
        var id = $(this).attr("pid").toString();
        var eml = this.parentNode.children[2];

        $.ajax({
            type: "GET",
            url: "/minuscart",
            data: { prod_id: id },
            success: function(data) {
                window.location.href = data.redirect_url;
                if (data.quantity !== undefined && data.amount !== undefined && data.totalamount !== undefined) {
                    eml.innerText = data.quantity;
                    var amountElement = document.getElementById("amount");
                    var totalAmountElement = document.getElementById("totalamount");

                    if (amountElement && totalAmountElement) {
                        amountElement.innerText = "Rs. " + data.amount.toFixed(2);
                        totalAmountElement.innerText = "Rs. " + data.totalamount.toFixed(2);
                    } else {
                        console.error('Element with id="amount" or id="totalamount" not found');
                    }
                } else {
                    console.error('Incomplete data returned from server:', data);
                }
            },
            error: function(xhr, status, error) {
                console.error('Failed to update cart:', error);
            }
        });
    });

    // Remove-cart action
    $('.remove-cart').click(function() {
        var id = $(this).attr("pid").toString();
        var cartItem = $(this).closest('.cart-item');

        $.ajax({
            type: "GET",
            url: "/removecart",
            data: { prod_id: id },
            success: function(data) {
                window.location.href = data.redirect_url;
                if (data.amount !== undefined && data.totalamount !== undefined) {
                    var amountElement = document.getElementById("amount");
                    var totalAmountElement = document.getElementById("totalamount");

                    if (amountElement && totalAmountElement) {
                        amountElement.innerText = "Rs. " + data.amount.toFixed(2);
                        totalAmountElement.innerText = "Rs. " + data.totalamount.toFixed(2);
                    } else {
                        console.error('Element with id="amount" or id="totalamount" not found');
                    }

                    // Remove the cart item from the DOM
                    cartItem.remove();
                    
                } else {
                    console.error('Amount or totalamount missing in data:', data);
                    alert('Failed to remove item');
                }
            },
            error: function(xhr, status, error) {
                console.error('Failed to remove item:', error);
                alert('Failed to remove item: ' + error);
            }
        });
    });

    // Plus-wishlist action
    $('.plus-wishlist').click(function() {
        var id = $(this).attr("pid").toString();
        $.ajax({
            type: "GET",
            url: "/pluswishlist",
            data: { prod_id: id },
            success: function(data) {
                window.location.href = `http://localhost:8000/product-detail/${id}`
            },
            error: function(xhr, status, error) {
                console.error('Failed to add to wishlist:', error);
            }
        });
    });

    // Minus-wishlist action
    $('.minus-wishlist').click(function() {
        var id = $(this).attr("pid").toString();
        $.ajax({
            type: "GET",
            url: "/minuswishlist",
            data: { prod_id: id },
            success: function(data) {
                window.location.href = `http://localhost:8000/product-detail/${id}`
            },
            error: function(xhr, status, error) {
                console.error('Failed to remove from wishlist:', error);
            }
        });
    });
});
