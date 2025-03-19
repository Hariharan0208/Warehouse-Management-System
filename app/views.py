from django.shortcuts import render,redirect
from app.models import userdetails,Category,ProductTable,Cart,ShipType,Buy,Order
from django.contrib.auth import authenticate,login
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import authenticate,login
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.db import transaction
from django.shortcuts import render, get_object_or_404
import random
from datetime import datetime, timedelta
import re
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.

def Home_Page(request):
    return render(request,"Home.html")

def Login_Page(request):
    return render(request,"LoginPage.html")

def LoginPage_Backend(request):
    if request.method=="POST":
        username=request.POST["username"]
        password=request.POST["password"]

        user= authenticate(username=username,password=password)

        if user is not None:
            if(user.is_superuser):
                login(request, user)
                return redirect("Admin_Home")
            elif user is not None and user.is_user:
                login(request, user)
                return redirect('UserHome_Page')
            elif user is not None and user.is_agent:
                login(request, user)
                return redirect('AgentHome_Page')
        else:
            messages.info(request,"Invalid username and password")
            return redirect("Login_Page")
    else:
        return redirect("Sign_Page")


def Sign_Page(request):
    return render(request,"SignUp.html")

def SignPage_Backend(request):
    if request.method=="POST":
        # Auth user Table
        first_name=request.POST["first_name"]
        last_name=request.POST["last_name"]
        username=request.POST["username"]
        email=request.POST["Email"]
        
        # our Table(Connecter table)
        address=request.POST["Address"]
        pan=request.POST["Pan"]
        phone=request.POST["PhoneNumber"]
        usertype=request.POST["select"]

        image=request.FILES.get("file")
        if image==None:
            image="Image/imgg.jpg"
        
        if usertype=='User':
            customer=True
            agent=False
        else:
            customer=False
            agent=True

        if userdetails.objects.filter(email=email).exists():
            messages.info(request, "This email is already exist, try new")
            return redirect("Sign_Page")
        
        if userdetails.objects.filter(username=username).exists():
            messages.info(request, "This username is already exist, try new")
            return redirect("Sign_Page")
        
        if userdetails.objects.filter(Phone= phone).exists():
            messages.info(request,"This Phone Number is already exist, try new")
            return redirect("Sign_Page")
        else:
            # Auth user Table
            user = userdetails.objects.create_user(
                                                    first_name=first_name,
                                                    last_name=last_name,
                                                    username=username,
                                                    email=email,
                                                    Address=address,
                                                    Phone=phone,
                                                    PanCard=pan,
                                                    UserType=usertype,
                                                    Permission='denied',
                                                    is_user=customer,
                                                    is_agent=agent,
                                                    Image=image
                                                  )
            user.save()
    
            messages.success(request, "Your registration was successful. Please wait for admin approval.")
            return redirect("Login_Page")          
    else:
        return redirect("Sign_Page")

def Admin_Home(request):
    context = {
        "total_categories": Category.objects.count(),
        "total_products": ProductTable.objects.count(),
        "total_customers": userdetails.objects.filter(UserType="user").count(),
        "total_delivery_agents": userdetails.objects.filter(UserType="agent").count(),
        "total_order_returns": Buy.objects.filter(DeliveryCondition="Returned").count(),
        # "Users":userdetails.objects.filter(Permission='denied').count(),
    }
    Users=userdetails.objects.filter(Permission='denied').count()
    if(Users > 0):
        messages.info(request, f"{Users} Users are waiting in the lobby for your approval!")
        return render(request,"AdminHome.html",context)
    return render(request,"AdminHome.html",context)

def AdminPermission_Allow(request,pk):
    Data=userdetails.objects.get(id=pk)
    Email=Data.email
    Name=Data.first_name
    Username=Data.username
    Password=str(random.randint(100000,999999))
    subject = "Registration Completed"
    message = f"Dear {Name},\nYour account has been successfully created. \nUsername: {Username}\nPassword: {Password}"
    recipient = Email
    send_mail(subject, message, settings.EMAIL_HOST_USER, [recipient], fail_silently=False)
    Data.set_password(Password)
    Data.Permission="allow"
    Data.save()
    update_session_auth_hash(request, Data) 
    messages.success(request,"Process Successful Done!")
    return redirect(' UserPermission_Page')

def AdminPermission_Denied(request,pk):
    Data=userdetails.objects.get(id=pk)
    Email=Data.email
    Name=Data.first_name
    subject = "Registration Update"
    message = f"Dear {Name},\nYour Permission is Denied from Admin, Sorry for inconvenient."
    recipient = Email
    send_mail(subject, message, settings.EMAIL_HOST_USER, [recipient], fail_silently=False)
    Data.delete()
    messages.success(request,"Process Successful Done!")
    return redirect(' UserPermission_Page')

def RemoveUser_Backend(request,pk):
    Data=userdetails.objects.get(id=pk)
    Data.delete()
    messages.success(request,"Account Successful Removed!")
    return redirect(' UserPermission_Page')

def UserList_Page(request):
    Data=userdetails.objects.all()
    return render(request,"UserList.html",{'Data':Data})

def UserPermission_Page(request):
    Data=userdetails.objects.filter(Permission='denied')
    return render(request,"UserPermission.html",{'Data':Data})



def AddCategory_Page(request):
    return render (request,"AddCategory.html")

def AddCategoryPage_Backend(request):
    if request.method=="POST":
        Cat_name=request.POST["category_name"]
        Cat_table=Category(categorys=Cat_name)
        Cat_table.save()
        messages.success(request,"Successful Add a Category!")
        return redirect('AddCategory_Page')

def CategoryList_Page(request):
    Data=Category.objects.all()
    # messages.info(request,"successfully removed Category")
    return render(request,"CategoryList.html",{"Data":Data})

def Delete_CategoryItem(request,pk):
    pro=Category.objects.get(id=pk)
    pro.delete()
    messages.info(request,"successfully removed Category")
    return redirect("CategoryList_Page")

def AddProduct_Page(request):
    category=Category.objects.all()
    return render (request,"AddProduct.html",{'category':category})

def AddProductPage_Backend(request):
    if request.method=="POST":
        Cat_name=request.POST["name"]
        Cat_description=request.POST["description"]
        Cat_specifications=request.POST['specifications']
        Cat_price=request.POST["price"]
        Cat_quantity=request.POST["quantity"]

        select=request.POST["select"]
        category=Category.objects.get(id=select)
        

        image=request.FILES.get("file")
        if image==None:
            image="Image/imgg.jpg"

        data=ProductTable(CategoryType=category,
                          ProductName=Cat_name,
                          Description=Cat_description,
                          Specifications=Cat_specifications,
                          Price=Cat_price,
                          Quantity=Cat_quantity,
                          Image=image)
    
        data.save()
        messages.success(request,"Successful Add a Product")
        return redirect("AddProduct_Page")

def ProductList_Page(request):
    Data=ProductTable.objects.all()
    return render(request,"ProductList.html",{"Data":Data})

def EditProduct_Page(request,pk):
    Data=ProductTable.objects.get(id=pk)
    Cat=Category.objects.all()
    return render (request,"EditProduct.html",{"Data":Data,"Cat":Cat})

def EditProductPage_Backend(request, pk):
    Data=ProductTable.objects.get(id=pk)
    # Cat=Category.objects.get(id=userId)

    if request.method == "POST":
        # For Auth user
        Data.ProductName = request.POST["name"]
        Data.Description = request.POST["description"]
        Data.Specifications = request.POST['specifications']
        Data.Price = request.POST["price"]
        Data.Quantity = request.POST["quantity"]

        select = request.POST["select"]
        Cat= Category.objects.get(id=select)
        Data.CategoryType = Cat

        old = Data.Image
        new = request.FILES.get("file")

        if old != None and new == None:
            Data.Image = old
        else:
            Data.Image = new

        Data.save()
        messages.info(request,"successfully Edit product")
        return redirect("ProductList_Page")

def Delete_ProductItem(request,pk):
    pro=ProductTable.objects.get(id=pk)
    pro.delete()
    messages.info(request,"successfully removed product")
    return redirect("ProductList_Page")

def AdminOrder_Page(request):
    Data = Buy.objects.filter(Agent='No')
    Agent =userdetails.objects.all()
    context = {'Data':Data,'Agent':Agent }
    return render(request,"AdminOrder.html",context)


def AdminOrderPage_Backend(request,pk):
    order=Buy.objects.get(id=pk)
    select=request.POST["select"]
    agent=userdetails.objects.get(id=select)
    Data=Order(DeliveryAgent=agent,OrderList=order)
    order.Agent='Yes'
    order.save()
    Data.save()
    messages.info(request,"successfully Order Allocated !!!")
    return redirect('AdminOrder_Page')

def OrderList(request):
    Data = Buy.objects.all()
    Agent =userdetails.objects.all()
    order=Order.objects.all()
    context = {'Data':Data,'Agent':Agent,'Order':order}
    return render(request,"UserOrderList.html",context)
    


def UserHome_Page(request):
    Data=ProductTable.objects.all()
    return render(request,"UserHome.html",{'Data':Data})

def AddToCart_Page(request):
    cat=Category.objects.all()
    cart_list=Cart.objects.filter(user=request.user).select_related('product')
    total_price= sum(item.total_price() for item in cart_list)
    return render(request,'AddToCart.html',{"cart_list":cart_list,"total_price":total_price, 'cat':cat})

def add_to_cart(request, pk):
    product = ProductTable.objects.get(id=pk)
    cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)

    if cart_item.Quantity >= product.Quantity:
        if cart_item.Quantity>1:
            messages.info(request, "Product Out Of Stock!!!")
            return redirect('AddToCart_Page')
        else:
            return redirect('AddToCart_Page')
    if not created:
        cart_item.Quantity += 1
        cart_item.save()
        
    return redirect("AddToCart_Page")

def remove_cart(request,pk):
    product=ProductTable.objects.get(id=pk)
    cart_item=Cart.objects.filter(user=request.user,product=product).first()
    
    if cart_item:
        cart_item.delete()
        return redirect("AddToCart_Page")
    
def Increase_quantity(request, id):
    try:
        cart_item = Cart.objects.get(product_id=id, user=request.user)
        data = ProductTable.objects.get(id=id)
    except ObjectDoesNotExist:
        messages.error(request, "Product or Cart Item does not exist.")
        return redirect('AddToCart_Page')

    # Check if the requested quantity can be increased
    if cart_item.Quantity >= data.Quantity:
        messages.info(request, "Product Out Of Stock!!!")
        return redirect('AddToCart_Page')

    # Atomic transaction to update cart and product quantities
    with transaction.atomic():
        cart_item.Quantity += 1
        cart_item.save()

    return redirect('AddToCart_Page')


def Decrease_quantity(request,id):
    cart_item=Cart.objects.get(product_id=id,user=request.user)

    with transaction.atomic():
        cart_item.Quantity -=1
        cart_item.save()
        # cart_item.product.Quantity +=1
        # cart_item.product.save()
    return redirect("AddToCart_Page")


def Buy_now_page(request, pk):
    product = get_object_or_404(ProductTable, id=pk)
    category = product.CategoryType
    customer = userdetails.objects.filter(id=request.user.id).first()
    Type = ShipType.objects.all()

    context = {
        'product': product,
        'category': category,
        'customer': customer,
        'Type'    : Type,
    }
    return render(request, "BuyPage.html", context)


def BuyNowPage_Backend(request, pk):
    product = get_object_or_404(ProductTable, id=pk)
    # category = product.CategoryType
    customer = userdetails.objects.filter(id=request.user.id).first()
    Type = ShipType.objects.all()
    cart_item=Cart.objects.filter(user=request.user,product=product).first()

    quantity_str = request.POST.get('quantity')
    
    if quantity_str:
        try:
            quantity = int(quantity_str)
        except ValueError:
            # If quantity is not a valid number, set it to None and show error
            quantity = None
    else:
        quantity = None
    if quantity is not None:
        if quantity > 0 and quantity <= product.Quantity:
             
            paymenttype=request.POST["payment_option"]
            select=request.POST["select"]
            value=ShipType.objects.get(id=select)

            current_date = datetime.now().date()
            order_Day=current_date.strftime("%d")
            order_month=current_date.strftime("%B")

            future_date = current_date + timedelta(days=5)
            Delivery_day = future_date.strftime("%d")
            Delivery_month = future_date.strftime("%B")

            Id = random.randint(1000000000,9999999999)
            total=quantity*product.Price

            data=Buy(Customer=customer,
                    ProductName=product.ProductName,
                    Description=product.Description,
                    Specifications=product.Specifications,
                    Quentity= quantity,
                    Price=product.Price,
                    TotalPrice=total,
                    shiptype=value,
                    OrderDate=order_Day+order_month,
                    DeliverData=Delivery_day+Delivery_month,
                    OrderID=Id,
                    PaymentMethod=paymenttype,
                    Image1=product.Image
                    )
            if cart_item:
                cart_item.delete()
            data.save()
            Email=customer.email
            Name=customer.first_name
            subject = "Order Delivery Confirmation!!!"
            message = f"Dear {Name},\nYour Order has been successfully Placed.\nOrder ID: {Id} \nProduct Name: {product.ProductName}\nDescription: {product.Description}\nPrice: {product.Price}\nQuentity: {quantity}\nTotalPrice: {total}\nOrder Date: {order_Day+order_month}\nDeliver Data: {Delivery_day+Delivery_month}"
            recipient = Email
            send_mail(subject, message, settings.EMAIL_HOST_USER, [recipient], fail_silently=False)
            product.Quantity=product.Quantity-quantity
            product.save()
            error_message = "Order Successfully Placed !!!"
            return redirect('OrderTracking_Page')
        else:
            error_message = f"Out of stock! Only {product.Quantity} items are available."
            return render(request, "BuyPage.html", {"product": product, "category": product.CategoryType, "Content": error_message,"Type":Type,"customer":customer})
    
    else:
        error_message = "Please enter a valid quantity."
        return render(request, "BuyPage.html", {"product": product, "category": product.CategoryType, "Content": error_message,"Type":Type,"customer":customer})


def OrderTracking_Page(request):
    Data = Buy.objects.all()
    Customer = userdetails.objects.filter(id=request.user.id).first()
    context = {'Data':Data,'Customer':Customer }
    return render(request,"OrderTracking.html",context)

def UserProfile(request):
    Data = userdetails.objects.filter(id=request.user.id).first()

    return render(request,'UserProfile.html',{"Data":Data})

def OrderSearch(request,pk):
    order = get_object_or_404(Buy, id=pk)
    return render(request,'TrackIdSearch.html',{"order": order})

def Admin_OrderStatus(request,pk):
    Data=Buy.objects.get(id=pk)
    return render(request,'OrderLocation.html',{"i":Data})


def AgentProfile(request):
    Data = userdetails.objects.filter(id=request.user.id).first()
    return render(request,'AgentProfile.html',{"Data":Data})

def edit_profile(request,pk):
    User=userdetails.objects.get(id=pk)
    return render(request,'EditProfile.html',{'User':User}) 

def Agentedit_profile(request,pk):
    User=userdetails.objects.get(id=pk)
    return render(request,'AgentProfileEdit.html',{'User':User}) 

def update_userprofile(request, pk):
    Data=userdetails.objects.get(id=pk)
    if request.method == "POST":
        # For Auth user
        Data.first_name = request.POST["first_name"]
        Data.last_name = request.POST["last_name"]
        UserName=request.POST["username"]
        phone=request.POST["phone"]
        Email=request.POST["email"] 
        # Our user table
        Data.Address = request.POST["address"]
        Data.Phone = request.POST["phone"]

        old = Data.Image
        new = request.FILES.get("file")

        if old != None and new == None:
            Data.Image = old
        else:
            Data.Image = new
        if userdetails.objects.filter(email= Data.email).exists():
            if(Data.email != Email): 
                messages.info(request, "This email is already exist, try new")
                User= userdetails.objects.filter(id=request.user.id).first()
                return render(request,'EditProfile.html',{'User':User}) 

        if userdetails.objects.filter(username=Data.username).exists():
            if(Data.username != UserName):
                messages.info(request, "This username is already exist, try new")
                User= userdetails.objects.filter(id=request.user.id).first()
                return render(request,'EditProfile.html',{'User':User}) 
        if userdetails.objects.filter(Phone=Data.Phone).exists():
            if(Data.Phone != phone):
                messages.info(request,"This Phone Number is already exist, try new")
                User= userdetails.objects.filter(id=request.user.id).first()
                return render(request,'EditProfile.html',{'User':User})
        Data.email = request.POST["email"] 
        Data.username = request.POST["username"]
        Data.Phone = request.POST["phone"]
        Data.save()
        if Data.UserType=='User':
            messages.error(request, "Profile Successfully Updated !!!")
            return redirect("UserProfile")
        else:
            messages.error(request, "Profile Successfully Updated !!!")
            return redirect("AgentProfile")

@login_required

def ChangePassword(request):
    Agent = userdetails.objects.filter(id=request.user.id).first()
    if request.method == "POST":
        old_password = request.POST["old_password"]
        new_password = request.POST["new_password"]
        confirm_new_password = request.POST["confirm_new_password"]
        user = request.user

        if not user.check_password(old_password):
            messages.error(request, "Incorrect old password. Please try again.")
            return redirect('ChangePassword')

        if new_password != confirm_new_password:
            messages.error(request, "New passwords do not match. Please try again.")
            return redirect('ChangePassword')
        
        if not re.search(r'[A-Z]', new_password):
            messages.error(request, "Password contains at least one uppercase letter")
            return redirect('ChangePassword')
        if not re.search(r'[0-9]', new_password):
            messages.error(request, "Password contains at least one digit")
            return redirect('ChangePassword')
        if not re.search(r'[@$!%*?&]', new_password):
            messages.error(request, "Password contains at least one special character")
            return redirect('ChangePassword')
        user.set_password(new_password)
        user.save()
        update_session_auth_hash(request, user) 
        if Agent.UserType=='User':
            messages.success(request, "Password changed successfully.")
            return redirect('UserProfile')
        else:
            messages.success(request, "Password changed successfully.")
            return redirect('AgentProfile')
    else:
        return render(request,"ChangePassword.html")


def AgentHome_Page(request):
    Data = Order.objects.all()
    Agent = userdetails.objects.filter(id=request.user.id).first()
    context={"Data":Data,'Agent':Agent}
    return render(request,"AgentHome.html",context)

def Delivery_Update(request,pk):
    product=Buy.objects.get(id=pk)
    return render(request,"DeliveryUpdate.html",{"product":product})

def DeliverUpdate_Backend(request,pk):
    product=Buy.objects.get(id=pk)
    if request.method == 'POST':
        status = request.POST.get('status')
        product.status = status
        location = request.POST.get('location')
        if location:
           product.Loaction = location
        if status == 'delivered':
            product.DeliveryCondition='No'
        product.save()
        messages.info(request,"Delivery Status successfully Updated !!!")
    return redirect('AgentHome_Page')

def LocationUpdate_Page(request,pk):
    product=Buy.objects.get(id=pk)
    return render(request,"AgentDeliveryLocation.html",{"product":product})

def LocationUpdate_Back(request,pk):
    product=Buy.objects.get(id=pk)
    update=request.POST["category_name"]
    product.Loaction=update
    product.save()
    messages.info(request,"Delivery Location successfully Updated !!!")
    return redirect('AgentHome_Page')

def DeliveryCondition(request,pk):
    product=Buy.objects.get(id=pk)
    if product.DeliveryCondition == "No":
        product.DeliveryCondition="Yes"
        product.DeliveryStatus="Product Delivery Successfully Done!!!"
        product.save()
        messages.info(request,"Product Successfully Received!!!")
        return redirect('OrderTracking_Page')

def ShipType_Page(request):
    return render(request,"ShipType.html")

def ShipType_Backend(request):
    if request.method=="POST":
        name=request.POST["category_name"]
        Cat_table=ShipType(type=name)
        Cat_table.save()
        messages.success(request,"Shiping Type Add Successful!")
        return redirect('ShipType_Page')

def ShipTypeList_Page(request):
    Data=ShipType.objects.all()
    # messages.info(request,"successfully removed Category")
    return render(request,"ShipTypeList.html",{"Data":Data})

def Delete_ShipType(request,pk):
    pro=ShipType.objects.get(id=pk)
    pro.delete()
    messages.info(request,"successfully removed Category")
    return redirect("CategoryList_Page")


def search_product(request):
    query = request.GET.get('search')  # Get the search term from the GET request
    
    if query:
        # Filter products where either ProductName or Description contains the search term (case-insensitive)
        products = ProductTable.objects.filter(
            ProductName__icontains=query
        ) | ProductTable.objects.filter(
            Description__icontains=query
        )
    else:
        # If no query is entered, return all products
        products = ProductTable.objects.all()
    
    return render(request, 'SearchProduct.html', {'products': products, 'query': query})
