/* JavaScript code goes here */
        // Set rates + misc
        var taxRate = 0.05;
        var shippingRate = 15.00;
        var fadeTime = 300;

        // Assign actions
        $('.product-quantity input').change(function () {
            updateQuantity(this);
        });

        $('.product-removal button').click(function () {
            removeItem(this);
        });

        // Recalculate cart
        function recalculateCart() {
            var subtotal = 0;

            // Sum up row totals
            $('.product').each(function () {
                subtotal += parseFloat($(this).children('.product-line-price').text());
            });

            // Calculate totals
            var tax = subtotal * taxRate;
            var shipping = (subtotal > 0 ? shippingRate : 0);
            var total = subtotal + tax + shipping;

            // Update totals display
            $('.totals-value').fadeOut(fadeTime, function () {
                $('#cart-subtotal').html(subtotal.toFixed(2));
                $('#cart-tax').html(tax.toFixed(2));
                $('#cart-shipping').html(shipping.toFixed(2));
                $('#cart-total').html(total.toFixed(2));
                if (total == 0) {
                    $('.checkout').fadeOut(fadeTime);
                } else {
                    $('.checkout').fadeIn(fadeTime);
                }
                $('.totals-value').fadeIn(fadeTime);
            });
        }

        // Update quantity
        function updateQuantity(quantityInput) {
            // Calculate line price
            var productRow = $(quantityInput).parent().parent();
            var price = parseFloat(productRow.children('.product-price').text());
            var quantity = $(quantityInput).val();
            var linePrice = price * quantity;

            // Update line price display and recalc cart totals
            productRow.children('.product-line-price').each(function () {
                $(this).fadeOut(fadeTime, function () {
                    $(this).text(linePrice.toFixed(2));
                    recalculateCart();
                    $(this).fadeIn(fadeTime);
                });
            });
        }

        // Remove item from cart
        function removeItem(removeButton) {
            // Remove row from DOM and recalc cart total
            var productRow = $(removeButton).parent().parent();
            productRow.slideUp(fadeTime, function () {
                productRow.remove();
                recalculateCart();
                $.ajax({
            url: '/add_to_cart/',  // Replace this with your Django view URL
            method: 'POST',
            data: {'product_id': productId},  // Send product ID to identify the item to delete
            success: function (response) {
                // Handle success response if needed
            },
            error: function (xhr, status, error) {
                // Handle error response if needed
            }
            });
            });
        }

$(document).ready(function() {
    // Add click event listener to the checkout button
    $('#checkoutButton').click(function() {
        // Send a GET request to the Django view that generates the PDF
        $.get('/generate-pdf/', function(response) {
            // Create a blob from the response
            var blob = new Blob([response]);
            var link = document.createElement('a');
            link.href = window.URL.createObjectURL(blob);
            link.download = 'GramBazaar_bill' + Math.random().toString(36).substring(2, 8) + '.pdf';
            link.click();
        });
    });
});
