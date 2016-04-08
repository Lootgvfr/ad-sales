from django.shortcuts import render
from django.template import RequestContext, loader, Context
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User, Group
from django.core.urlresolvers import reverse
import re
from django.contrib.auth.models import User, Group
from ad_sales.models import User_info, Prototype, Order, Spot, Prototype_pic
from datetime import date, datetime
from django.db import connection
from ad_sales.forms import FileForm

def home(request):
    """Home page."""
    template = loader.get_template('ad_sales/home.html')
    context = RequestContext(request, {
    })
    return HttpResponse(template.render(context))
    
def thx(request):
    """Page after posting feedback."""
    template = loader.get_template('ad_sales/thx.html')
    context = RequestContext(request, {
    })
    return HttpResponse(template.render(context))
    
def login(request):
    """Page with a login form."""
    if request.user.is_authenticated():
        auth_logout(request)
    error = ''
    username = ''
    if request.method == "POST":
        try:
            username = request.POST['Username']
            password = request.POST['Password']
            user = authenticate(username=username, password=password)
            if user is None:
                raise Exception('Invalid login data')
            else:
                if not user.is_active:
                    raise Exception('This user is disabled')
        except Exception as ex:
            error = ex
            password_error = True
        else:
            auth_login(request, user)   
            return HttpResponseRedirect(reverse('home'))
    return render(request, 'ad_sales/login.html', {
        'error_message':error,
        'username':username
    })

def register(request):
    """Page with a registration form."""
    if request.user.is_authenticated():
        auth_logout(request)
    error = ''
    username = ''
    email = ''
    phone = ''
    name = ''
    if request.method == "POST":
        try:
            username = request.POST['Username']
            email = request.POST['Email']
            password = request.POST['Password']
            pr = request.POST['Password_repeat']
            phone = request.POST['Phone']
            name = request.POST['Name']
            em = re.compile(r'^[a-zA-Z0-9._%-]+@[a-zA-Z0-9._%-]+\.[a-zA-Z]{2,6}$')
            n = re.compile(r'^[a-zA-Z0-9_@+.-]+$')
            ph = re.compile(r'\+?[0-9]+$')
            if username == '' or email == '' or name == '' or phone == '' or password == '' or pr == '':
                raise Exception('Деякі поля пусті.')
            elif len(username) > 29:
                raise Exception('Логін занадто довгий.')
            elif not n.match(username):
                raise Exception('Логін містить заборонені символи.')
            elif not em.match(email):
                raise Exception('Введено не валідний e-mail.')
            elif not ph.match(phone):
                raise Exception('Формат номеру телефона невірний.')
            elif password != pr:
                raise Exception('Паролі не співпадають.')       
        except Exception as ex:
            error = ex
        else:
            user = User.objects.create_user(username=username, password=password)
            usergroup = Group.objects.get(name='User')
            user.groups.add(usergroup)
            info = User_info(user=user, phone=phone, name=name, email=email)
            info.save()
            return HttpResponseRedirect(reverse('login'))
    return render(request, 'ad_sales/register.html', {
        'error_message':error,
        'username':username,
        'email':email,
        'phone':phone,
        'name':name
    })
    
def logout(request):
    """Log out and redirect to home page."""
    auth_logout(request)
    return HttpResponseRedirect(reverse('home'))
    
def add_order(request):
    """Page with a form for adding an order."""
    width = ''
    height = ''
    text = ''
    layout = ''
    error = ''
    graph = ''
    if request.method == "POST":
        if 'input_submit' in request.POST:
            try:
                width = request.POST['Width']
                height = request.POST['Height']
                text = request.POST['Text']
                layout = request.POST['Layout']
                graph = request.POST['Graph']
                num = re.compile(r'^[0-9]{1,2}$')
                if width == '' or height == '' or text == '' or layout == '' or graph == '':
                    raise Exception('Деякі поля пусті.')
                elif not num.match(width) or not num.match(height):
                    raise Exception('Введіть числа від 0 до 99 в перші два рядки.')     
            except Exception as ex:
                error = ex
            else:
                submit_date = datetime.now()
                cursor = connection.cursor()
                cursor.execute(
                    "INSERT INTO `order`(status, date_recieved, user_id) VALUES (%s, %s, %s)",
                    [u'Вибір макета', submit_date.strftime('%Y-%m-%d'), request.user.id])
                order_id = cursor.lastrowid
                cursor.execute(
                    "INSERT INTO prototype(width, height, layout, text, desc_graphical, order_id)" +
                    " VALUES (%s, %s, %s, %s, %s, %s)",
                    [width, height, layout, text, graph, order_id])
                return HttpResponseRedirect(reverse('thx'))
        elif 'upload_submit' in request.POST:
            try:
                form = FileForm(request.POST, request.FILES)
                width = request.POST['Width']
                height = request.POST['Height']
                num = re.compile(r'^[0-9]{1,2}$')
                if width == '' or height == '':
                    raise Exception('Деякі поля пусті.')
                elif not num.match(width) or not num.match(height):
                    raise Exception('Введіть числа від 0 до 99 в перші два рядки.')
                elif not form.is_valid():
                    raise Exception('Помилка завантаження файлу.')
            except Exception as ex:
                error = ex
            else:
                submit_date = datetime.now()
                cursor = connection.cursor()
                cursor.execute(
                    "INSERT INTO `order`(status, date_recieved, user_id) VALUES (%s, %s, %s)",
                    [u'Очікування позицій', submit_date.strftime('%Y-%m-%d'), request.user.id])
                order_id = cursor.lastrowid
                prot = Prototype_pic(status=u'Затверджено', width=width, height=height, order_id=order_id, img=request.FILES['img'])
                prot.author = request.user
                prot.save()
                return HttpResponseRedirect(reverse('thx'))
    else:
        form = FileForm()
    return render(request, 'ad_sales/add_order.html', {
        'error_message':error,
        'width':width,
        'height':height,
        'text':text,
        'layout':layout,
        'graph':graph,
        'form':form
    })
    
def view_orders(request):
    """Page with a list of orders."""
    template = loader.get_template('ad_sales/view_orders.html')
    cursor = connection.cursor()
    if request.user.groups.filter(name='User').exists():
        cursor.execute(
            "SELECT auth_user.username, order.id, order.date_recieved, order.status "+ 
            "FROM `order` "+
            "INNER JOIN auth_user ON order.user_id=auth_user.id AND auth_user.id=%s "+
            "GROUP BY order.id " +
            "ORDER BY order.date_recieved, order.id",
            [request.user.id])
    else:
        cursor.execute("SELECT auth_user.username, order.id, order.date_recieved, order.status "+
            "FROM `order` INNER JOIN auth_user ON order.user_id=auth_user.id GROUP BY order.id " + 
            "ORDER BY auth_user.username, order.date_recieved, order.id")
    rows = cursor.fetchall()
    orders = []
    for row in rows:
        orders.append({'id':row[1], 'user':row[0], 'date':row[2].strftime('%Y-%m-%d'), 'status':row[3]})
    context = RequestContext(request, {
        'orders':orders
    })
    return HttpResponse(template.render(context))
    
def view_orders_filter(request, status):
    """Page with a list of orders filtered."""
    template = loader.get_template('ad_sales/view_orders.html')
    st = u''
    if status == 'prototype':
        st = u'Вибір макета'
    elif status == 'spots':
        st = u'Очікування позицій'
    elif status == 'completed':
        st = u'Завершено'
    else:
        return HttpResponseRedirect(reverse('view_orders'))
    cursor = connection.cursor()
    if request.user.groups.filter(name='User').exists():
        cursor.execute(
            "SELECT auth_user.username, order.id, order.date_recieved, order.status "+
            "FROM `order` "+
            "INNER JOIN auth_user ON order.user_id=auth_user.id AND auth_user.id=%s AND order.status=%s "+
            "GROUP BY order.id "+
            "ORDER BY order.date_recieved, order.id", 
            [request.user.id, st])
    else:
        cursor.execute("SELECT auth_user.username, order.id, order.date_recieved, order.status "+
            "FROM `order` INNER JOIN auth_user ON order.user_id=auth_user.id AND order.status=%s "+
            "GROUP BY order.id ORDER BY order.date_recieved, order.id", [st])
    rows = cursor.fetchall()
    orders = []
    for row in rows:
        orders.append({'id':row[1], 'user':row[0], 'date':row[2].strftime('%Y-%m-%d'), 'status':row[3]})
    context = RequestContext(request, {
        'orders':orders,
        'status':status
    })
    return HttpResponse(template.render(context))

def delete_order(request, order_id):
    """Delete an order."""
    cursor = connection.cursor()
    if request.user.groups.filter(name='User').exists():
        if len(Order.objects.filter(id=order_id)) == 1:
            if Order.objects.get(id=order_id).user_id == request.user.id:
                cursor.execute("DELETE FROM `order` WHERE id=%s", [order_id])
                spots = Spot.objects.filter(order_id=order_id)
                for spot in spots:
                    spot.status = 'Вільна'
                    spot.save()
    else:
        if len(Order.objects.filter(id=order_id)) == 1:
            cursor.execute("DELETE FROM `order` WHERE id=%s", [order_id])
            spots = Spot.objects.filter(order_id=order_id)
            for spot in spots:
                spot.status = 'Вільна'
                spot.save()
    return HttpResponseRedirect(reverse('view_orders'))
    
def view_order(request, order_id):
    """Page with a basic info about an order."""
    template = loader.get_template('ad_sales/view_order.html')
    order = Order.objects.get(id=order_id)
    username = User.objects.get(id=order.user_id).username
    context = RequestContext(request, {
        'order_id':order_id,
        'username':username,
        'date_recieved':order.date_recieved,
        'date_completed':order.date_completed,
        'status':order.status
    })
    return HttpResponse(template.render(context))
    
def view_order_prototypes(request, order_id):
    """Page with the prototypes of an order."""
    if request.method == 'POST':
        if 'upload_submit' in request.POST:
            try:
                form = FileForm(request.POST, request.FILES)
                width = request.POST['Width']
                height = request.POST['Height']
                num = re.compile(r'^[0-9]{1,2}$')
                if width == '' or height == '':
                    raise Exception('Деякі поля пусті.')
                elif not num.match(width) or not num.match(height):
                    raise Exception('Введіть числа від 0 до 99 в перші два рядки.')
                elif not form.is_valid():
                    raise Exception('Помилка завантаження файлу.')
            except Exception as ex:
                error = ex
            else:
                prot = Prototype_pic(status=u'Запропоновано', width=width, height=height, order_id=order_id, img=request.FILES['img'])
                prot.author = request.user
                prot.save()
                return HttpResponseRedirect(reverse('view_order_prototypes', args=(order_id,)))
        else:
            prots = Prototype_pic.objects.filter(order_id=order_id)
            i = -1
            for prot in prots:
                prid = prot.id
                if 'select'+str(prid) in request.POST:
                    i = prid
                    break
            pr = Prototype_pic.objects.get(id=i)
            pr.status = u'Затверджено'
            pr.save()
            prots = Prototype_pic.objects.filter(order_id=order_id, status='Запропоновано')
            for prot in prots:
                prot.delete()
            ord = Order.objects.get(id=order_id)
            ord.status='Очікування позицій'
            ord.save()
            return HttpResponseRedirect(reverse('view_order_prototypes', args=(order_id,)))
    else:
        template = loader.get_template('ad_sales/view_order_prototypes.html')
        order = Order.objects.get(id=order_id)
        form = FileForm()
        if order.status == u'Вибір макета':
            prototypes = Prototype_pic.objects.filter(order_id=order_id)
        else:
            prototypes = Prototype_pic.objects.filter(order_id=order_id)
        prototype = None
        if len(Prototype.objects.filter(order_id=order_id)) == 1:
            prototype = Prototype.objects.get(order_id=order_id)
        context = RequestContext(request, {
            'order_id':order_id,
            'status':order.status,
            'form':form,
            'prototypes':prototypes,
            'prototype':prototype
        })
        return HttpResponse(template.render(context))
    
def view_order_spots(request, order_id):
    """Page with the spots of an order."""
    if request.method == 'POST':
        if 'propose' in request.POST:
            spot_id = request.POST['spot_id']
            spot = Spot.objects.get(id=spot_id)
            spot.status = u'Запропонована'
            spot.order_id = order_id
            spot.save()
            return HttpResponseRedirect(reverse('view_order_spots', args=(order_id,)))
        elif 'chkb' in request.POST:
            checked = []
            spots = Spot.objects.filter(order_id=order_id)
            for spot in spots:
                if 'checkbox' + str(spot.id) in request.POST:
                    checked.append(spot.id)
            for i in checked:
                sp = Spot.objects.get(id=i)
                sp.status = u'Зайнята'
                sp.save()
            free = Spot.objects.filter(order_id=order_id, status=u'Запропонована')
            for spot in free:
                spot.order = None
                spot.status = u'Вільна'
                spot.save()
            ord = Order.objects.get(id=order_id)
            ord.status = u'Завершено'
            ord.date_completed = datetime.now()
            ord.save()
            return HttpResponseRedirect(reverse('view_order_spots', args=(order_id,)))
    else:
        template = loader.get_template('ad_sales/view_order_spots.html')
        spots = Spot.objects.filter(order_id=order_id).order_by('page')
        free_spots = Spot.objects.filter(status=u'Вільна').order_by('page')
        order = Order.objects.get(id=order_id)
        context = RequestContext(request, {
            'order_id':order_id,
            'status':order.status,
            'spots':spots,
            'free_spots':free_spots
        })
        return HttpResponse(template.render(context))
    
def download(request, pr_id):
    """Download a prototype picture."""
    if len(Prototype_pic.objects.filter(id=pr_id)) == 1:
        pr = Prototype_pic.objects.get(id=pr_id)
        filename = pr.img.name.split('/')[-1]
        response = HttpResponse(pr.img.file, content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename=%s' % filename
        return response
    else:
        return HttpResponseRedirect(reverse('home'))
        
def profile(request, username):
    """Page with a profile of a user."""
    template = loader.get_template('ad_sales/profile.html')
    if len(User.objects.filter(username=username)) == 0:
        return HttpResponseRedirect(reverse('home'))
    else:
        cursor = connection.cursor()
        cursor.execute(
            "SELECT user_info.name, user_info.email, user_info.phone, user_info.groupname "+
            "FROM auth_user "+
            "INNER JOIN user_info ON auth_user.username = %s AND auth_user.id = user_info.user_id "+
            "GROUP BY auth_user.username",
            [username])
        row = cursor.fetchone()
        context = RequestContext(request, {
            'username':username,
            'name':row[0],
            'email':row[1],
            'phone':row[2],
            'groupname':row[3]
        })
        return HttpResponse(template.render(context))
        
def view_spots_index(request):
    """Redirect to the first page of spots list."""
    return HttpResponseRedirect(reverse('view_spots', args=(1,)))
    
def view_spots(request, page):
    """Page with a list of spots for given page number."""
    template = loader.get_template('ad_sales/view_spots.html')
    spots = Spot.objects.filter(page=page)
    pages = [i for i in range(1,6)]
    context = RequestContext(request, {
        'spots':spots,
        'page':page,
        'pages':pages
    })
    return HttpResponse(template.render(context))
    
def add_spot(request):
    """Page with a form for adding a spot."""
    template = loader.get_template('ad_sales/add_spot.html')
    pages = [i for i in range(1,6)]
    width = ''
    height = ''
    cost = ''
    position = ''
    page = ''
    error = ''
    if request.method == 'POST':
        try:
            width = request.POST['Width']
            height = request.POST['Height']
            cost = request.POST['Cost']
            position = request.POST['Position']         
            page = request.POST['Page']
            num = re.compile(r'^[0-9]{1,2}$')
            fl = re.compile(r'^[0-9]+')
            if width == '' or height == '' or cost == '':
                raise Exception('Деякі поля пусті.')
            elif not num.match(width) or not num.match(height):
                raise Exception('Введіть числа від 0 до 99 в перші два рядки.')
            elif not fl.match(cost):
                raise Exception('Вартість має бути числом.')
            elif len(Spot.objects.filter(page=page, position=position)) > 0:
                raise Exception('Вибране положення на цій сторінці вже зайняте.')
        except Exception as ex:
            error = ex
        else:
            sp = Spot(width=width, height=height, position=position, cost=cost, page=page, status='Вільна')
            sp.save()
            return HttpResponseRedirect(reverse('view_spots_index'))
    context = RequestContext(request, {
        'pages':pages,
        'width':width,
        'height':height,
        'cost':cost,
        'error_message':error,
        'page':page,
        'position':position
    })
    return HttpResponse(template.render(context))
  
def delete_spot(request, spot_id):
    """Delete a spot."""
    cursor = connection.cursor()
    if len(Spot.objects.filter(id=spot_id)) == 1:
        cursor.execute("DELETE FROM `spot` WHERE id=%s", [spot_id])
    return HttpResponseRedirect(reverse('view_spots_index'))
    
def edit_spot(request, spot_id):
    """Page with a form for editing a spot."""
    template = loader.get_template('ad_sales/edit_spot.html')
    if len(Spot.objects.filter(id=spot_id))>0:
        spot = Spot.objects.get(id=spot_id)
        width = str(spot.width)
        height = str(spot.height)
        cost = str(spot.cost)
        position = spot.position
        page = str(spot.page)
        error = ''
        if request.method == 'POST':
            try:
                width = request.POST['Width']
                height = request.POST['Height']
                cost = request.POST['Cost']
                position = request.POST['Position']         
                page = request.POST['Page']
                num = re.compile(r'^[0-9]{1,2}$')
                fl = re.compile(r'^[0-9]+')
                if width == '' or height == '' or cost == '':
                    raise Exception('Деякі поля пусті.')
                elif not num.match(width) or not num.match(height):
                    raise Exception('Введіть числа від 0 до 99 в перші два рядки.')
                elif not fl.match(cost):
                    raise Exception('Вартість має бути числом.')
                elif len(Spot.objects.filter(page=page, position=position)) > 0:
                    raise Exception('Вибране положення на цій сторінці вже зайняте.')
            except Exception as ex:
                error = ex
            else:
                cursor = connection.cursor()
                cursor.execute(
                    "UPDATE spot SET width=%s, height=%s, cost=%s, position=%s, page=%s "+
                    "WHERE id = %s", [width, height, cost, position, page, spot_id])
                return HttpResponseRedirect(reverse('view_spots_index'))
        context = RequestContext(request, {
            'width':width,
            'height':height,
            'cost':cost,
            'error_message':error,
            'spot_id':spot_id,
            'page':page,
            'position':position
        })
        return HttpResponse(template.render(context))
    else:
        return HttpResponseRedirect(reverse('view_spots_index'))

def free_spot(request, order_id, spot_id):
    """Set status of a given spot to be free."""
    if len(Spot.objects.filter(id=spot_id)) > 0:
        spot = Spot.objects.get(id=spot_id)
        spot.order = None
        spot.status = u'Вільна'
        spot.save()
        return HttpResponseRedirect(reverse('view_order_spots', args=(order_id,)))
    else:
        return HttpResponseRedirect(reverse('view_order_spots', args=(order_id,)))
        
def statistics(request):
    """Page with statistics info."""
    template = loader.get_template('ad_sales/statistics.html')
    error = ''
    value = ''
    result = None
    success = 0
    if request.method == 'POST':
        try:
            value = int(request.POST['Value'])
            cursor = connection.cursor()
            if request.POST['var'] == 'var1':
                cursor.execute(
                    "SELECT auth_user.username FROM auth_user "+
                    "INNER JOIN `order` ON `order`.user_id = auth_user.id "+
                    "INNER JOIN spot ON `order`.id = spot.order_id AND spot.status = 'Зайнята' "+
                    "GROUP BY auth_user.username "+
                    "HAVING SUM(spot.cost) > %s",
                    [value])
            else:
                cursor.execute(
                    "SELECT auth_user.username FROM auth_user "+
                    "INNER JOIN `order` ON `order`.user_id = auth_user.id "+
                    "INNER JOIN spot ON `order`.id = spot.order_id "+
                    "GROUP BY auth_user.username "+
                    "HAVING COUNT(spot.id) > %s", 
                    [value])
            rows = cursor.fetchall()
            result = []
            for i in rows:
                result.append(i[0])
            success = 1
        except Exception as ex:
            error = ex          
    context = RequestContext(request, {
        'error_message':error,
        'value':value,
        'result':result,
        'success':success
    })
    return HttpResponse(template.render(context))