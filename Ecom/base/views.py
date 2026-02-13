from django.shortcuts import render,redirect
from django.http import JsonResponse
from base.form import UserForm
from.models import Electronic,Product,ard
from django.contrib import messages
from django.contrib.auth import authenticate,login as log,logout as out
import json

# Create your views here.
def home(request):
    return render(request,'home.html')

def login(request):
    if request.method == 'POST':
        name=request.POST.get('username')
        psw=request.POST.get('password')
        user=authenticate(request,username=name,password=psw)
        if user is not None:
            log(request,user)
            messages.success(request,'Login Successfully')
            return redirect('home')
        else:
            messages.error(request,'Username or Password is Worng')
            return redirect('/login') 
    return render(request,'log.html')
            
    
        

def Register(request):
    form=UserForm()
    if request.method=='POST':
        form=UserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Registration Success full Goto Login')
            return redirect('/login')
    return render(request,'register.html',{'form':form})

def elec(request):
    electronics=Electronic.objects.filter(status=0)
    return render(request,'elec.html',{'electronic':electronics})

def elecs(request,name):
    if(Electronic.objects.filter(name=name,status=0)):
        products=Product.objects.filter(catogry__name=name)
        return render(request,'Products.html',{"products":products,"category":name})
    else:
        messages.warning(request,"No Such Electronics")
        return redirect(elec)
    
def p_details(request,cname,pname):
     if(Electronic.objects.filter(name=cname,status=0)):
         if(Product.objects.filter(name=pname,status=0)):
             products=Product.objects.filter(name=pname,status=0).first()
             return render(request,'Pdetails.html',{"products":products})
         else:
            messages.error(request,"Product Not Found")
            return redirect('elec')    
     else:
         messages.warning(request,"No Such Electronics")
         return redirect(elec)    

def cart(request):
     if request.user.is_authenticated:
         cart=ard.objects.filter(user=request.user)
         return render(request,'cart.html',{'cart':cart})
     else:
         return redirect('home')

    
def addcard(request):
    if request.headers.get('X-requested-with')=='XMLHttpRequest':
        if request.user.is_authenticated:
            data=json.load(request)
            product_qty=data['product_qty']
            product_id=data['pid']
            #print(request.user.id)
            product_status=Product.objects.get(id=product_id)
            if product_status:
                if ard.objects.filter(user=request.user.id,product_id=product_id):
                    return JsonResponse({'status':'Product Already in Cart'}, status=200)
                else:
                    if product_status.quentity>=product_qty:
                        ard.objects.create(user=request.user,product_id=product_id,product_qty=product_qty)
                        return JsonResponse({'status':'Product Added to Cart'}, status=200)
                    else:
                        return JsonResponse({'status':'Product Stock Not Available'}, status=200)
            
        else:
            return JsonResponse({'status':'Login to Add Cart'},status=200)
    else:
        return JsonResponse({'status':'Invalid Access'}, status=200)
            
        
def delete(request,cid):
    cartitem=ard.objects.get(id=cid)
    cartitem.delete()
    return redirect('cart')
    
    
    
def logout(request):
    if request.user.is_authenticated:
        out(request)
        messages.success(request,"Logout Successfully")
    return redirect('home')
        
