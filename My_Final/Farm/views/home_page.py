from My_Final.funcs import make_list_of_lists
from My_Final.settings import (PRODUCT_PIC_NAMES,
                          PRODUCTS_ON_THE_LINE, )
from django.shortcuts import (render,
                              redirect, )
from Farm.models import (ProductType,
                               User, )


def home_page(request):
    product_types = ProductType.objects.filter()
    signed_user = User.objects.filter(login=1).first()
    loaded_pics_number = len(PRODUCT_PIC_NAMES)
    product_types_number = len(product_types)
    if product_types_number > loaded_pics_number:
        for i in range(loaded_pics_number, product_types_number):
            PRODUCT_PIC_NAMES.append('none.png')
    product_types = make_list_of_lists(product_types, PRODUCTS_ON_THE_LINE, product_types_number)
    product_pic_names = make_list_of_lists(PRODUCT_PIC_NAMES, PRODUCTS_ON_THE_LINE, product_types_number)
    product_object = []
    for type, pic in zip(product_types, product_pic_names):
        row = list(zip(type, pic))
        product_object.append(row)
    if request.method == 'GET':
        return render(request, 'home_page.html', {
            'product_object': product_object, 'signed_user': signed_user, 'row_len': PRODUCTS_ON_THE_LINE})
    # выход пользователя с перенаправлением на страницу откуда выход был совершен.
    elif request.method == 'POST':
        User.objects.filter(login=1).update(login=0)
        referer = request.META['HTTP_REFERER']
        return redirect(referer)
