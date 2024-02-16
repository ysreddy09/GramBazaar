from django.shortcuts import render, redirect
import io
from django.http import FileResponse
from reportlab.pdfgen import canvas


def index(request):
    return render(request, 'index.html')


# views.py


def signup(request):
    return render(request, 'signup.html')


def login(request):
    return render(request, 'login.html')


def home(request):
    return render(request, 'home.html')


def navbar(request):
    return render(request, 'navbar.html')


def home_page_slider(request):
    return render(request, 'home_page_slider.html')


def products(request):
    return render(request, 'products.html')


def generate_pdf(request):
    # Create a file-like buffer to receive PDF data.
    buffer = io.BytesIO()

    # Create the PDF object, using the buffer as its "file."
    p = canvas.Canvas(buffer)

    # Draw content on the PDF.
    p.drawString(100, 750, "Shopping Cart")
    p.drawString(100, 700, "Image")
    p.drawString(200, 700, "Product")
    p.drawString(350, 700, "Price")
    p.drawString(450, 700, "Quantity")
    p.drawString(550, 700, "Total")

    # Example product details (replace with actual data)
    prods = [
        {"title": "Dingo Dog Bones", "price": "$12.99", "quantity": "2", "total": "$25.98"},
        {"title": "Nutro™ Adult Lamb and Rice Dog Food", "price": "$45.99", "quantity": "1", "total": "$45.99"},
        {"title": "Nutro™ Adult Lamb and Rice Dog Food", "price": "$45.99", "quantity": "1", "total": "$45.99"}
    ]
    y = 680
    for product in prods:
        y -= 20
        p.drawString(100, y, product["title"])
        p.drawString(350, y, product["price"])
        p.drawString(450, y, product["quantity"])
        p.drawString(550, y, product["total"])

    # Add subtotal, tax, shipping, and grand total
    p.drawString(100, y - 30, "Subtotal: $71.97")
    p.drawString(100, y - 50, "Tax (5%): $3.60")
    p.drawString(100, y - 70, "Shipping: $15.00")
    p.drawString(100, y - 90, "Grand Total: $90.57")

    # Close the PDF object cleanly.
    p.showPage()
    p.save()

    # Set the file pointer back to the beginning of the buffer.
    buffer.seek(0)

    # Return the PDF as a FileResponse.
    return FileResponse(buffer, as_attachment=True, filename="shopping_cart.pdf")


def add_to_cart(request):
    return render(request, 'add_to_cart.html')


def profile(request):
    return render(request, 'profile.html')


def footer(request):
    return render(request, 'footer.html')


def update(request):
    return render(request, 'update.html')


def about(request):
    return render(request, 'about.html')


def purchased_history(request):
    return render(request, 'purchased_history.html')


def side_nav(request):
    return render(request, 'side_nav.html')


def seller_home(request):
    return render(request, 'seller_home.html')


def add_product(request):
    return render(request, 'add_product.html')


def details(request):
    return render(request, 'details.html')


def products_hist(request):
    return render(request, 'products_hist.html')


def update_seller(request):
    return render(request, 'update_seller.html')


def profile_seller(request):
    return render(request, 'profile_seller.html')


def admin_home(request):
    return render(request, 'admin_home.html')


def admin_details(request):
    return render(request, 'admin_details.html')


def admin_side_nav(request):
    return render(request, 'admin_side_nav.html')
