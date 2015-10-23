function add_cart_json(button, part_id) {
    var btn = $(button);
    trigger_preloader(btn);
    badge_json();
    $.ajax(
        {
            type: 'get',
            url: '/account/ajax_add_cart/',
            data: {cart_part_id: part_id},
            success: function(data){
                if(data.code_add == 1){
                    alert('Вы не можете добавить в корзину, т.к. товара нет на складе')
                }
                if(data.code_add == 0){
                   trigger_preloader(btn);
                   alert('Товар успешно добавлен в корзину!');
                    badge_json();
                }
                if(data.code_add == 2){
                    alert('Вы не можете купить у себя!')
                }
                if(data.code_add == 3){
                    alert('Вы не можете добавить товара больше, чем есть в базе')
                }
            },
            error: function(data) {
                trigger_preloader(btn);
                alert('Произошла непридведенная ошибка. Обратитесь в службу поддержки.');
                badge_json();
            }
    });
    event.preventDefault();
}

function add_to_cart_json(button, part_pk) {
    var btn = $(button);
    badge_json();
    $.ajax(
        {
            type: 'get',
            url: '/account/ajax_add_to_cart/',
            data: {cart_part_id: part_pk},
            success: function(data){
                if(data.code_add == 1){
                    alert('Вы не можете добавить в корзину, т.к. товара нет на складе')
                }
                if(data.code_add == 0){
                    alert('Товар успешно добавлен в корзину!');
                    $('span#obj_count_'+part_pk).text(data.part_count);
                    badge_json();
                }
                if(data.code_add == 2){
                    alert('Вы не можете купить у себя!')
                }
                if(data.code_add == 3){
                    alert('Вы не можете добавить товара больше, чем есть в базе')
                }
            },
            error: function(data) {
                alert('Произошла непридведенная ошибка. Обратитесь в службу поддержки.');
                badge_json();
            }
    });
    event.preventDefault();
}

function badge_json(){
    $.ajax({
            type: 'get',
            url: '/account/ajax_badge_cart/',
            success: function(data){
                $('span#badge_cart').text(data.badge_cart);
                if (data.chat_count != 0){
                    $('span#badge_message').text('+'+data.chat_count);
                }
                else { $('span#badge_message').text(''); }
                $.each(data.unread_chats, function(index, chat){
                    if (chat.count != 0){
                        $('span#'+chat.chat_pk).text('+'+chat.count);
                    }
                    else{$('span#'+chat.chat_pk).text('');}
                })
            },
            error: function(data) {
//                alert('Произошла непридведенная ошибка. Обратитесь в службу поддержки.')
            }
    });
    event.preventDefault();
}

function delete_cart_json(button, object_id){
    var btn = $(button);
    badge_json();
    $.ajax(
        {
            type: 'get',
            url: '/account/ajax_delete_to_cart/',
            data: {cart_part_id: object_id},
            success: function(data){
                $('tr#cart_part_'+object_id).fadeOut(500);
                badge_json();
                if(data.code_del == 1){
                    badge_json();
                    location.reload();
                }
            },
            error: function(data) {
                alert('Произошла непридведенная ошибка. Обратитесь в службу поддержки.')
            }
    });
    event.preventDefault();
}

function plus_cart_json(button, object_id){
    var btn = $(button);
    $.ajax(
        {
            type: 'get',
            url: '/account/ajax_plus_to_cart/',
            data: {cart_part_id: object_id},
            success: function(data){
                if(data.code_plus == 1){
                    $('span#cart_count_'+object_id).text(data.part_count);
                    $('span#cart_price_'+object_id).text(data.part_price);
                    $('span#cart_amount').text(data.amount_price);
                    }
                if(data.code_plus == 0){
                    alert('Вы не можете добавить товара больше, чем есть в базе')
                }
            },
            error: function(data) {
                alert('Произошла непридведенная ошибка. Обратитесь в службу поддержки.')
            }
    });
    event.preventDefault();
}


function minus_cart_json(button, object_id){
    var btn = $(button);
    $.ajax(
        {
            type: 'get',
            url: '/account/ajax_minus_to_cart/',
            data: {cart_part_id: object_id},
            success: function(data){
                if(data.code_min == 1){
                    alert('Вы не можете купить нулевое или отрицательное колличество товара!')
                }
                else{
                    $('span#cart_count_'+object_id).text(data.part_count);
                    $('span#cart_price_'+object_id).text(data.part_price);
                    $('span#cart_amount').text(data.amount_price);
                    }
            },
            error: function(data) {
                alert('Произошла непридведенная ошибка. Обратитесь в службу поддержки.')
            }
    });
    event.preventDefault();
}

function trigger_preloader(button){

    if (button.hasClass('preload')) {
         var preloader = $('<img/>', {
                                src: '/static/img/loadinfo.net (1).gif',
                                height: 15,
                                width: 128,
                                class: 'preloader'
                            });
    }
    if (button.is(':visible')){
        button.hide();
        button.parent().append(preloader);
        preloader.fadeIn(200);
    }
    else {
        button.fadeIn(600);
        button.parent().find('.preloader').remove();

    }
}

function get_user(input, pk){
    var input = $(input);
    var q = input.val();
    $.ajax({
        type: "get",
        url:"/account/ajax_search_user/",
        data: {user_search: q},
        success: function(data){
            var div = document.getElementById('search_list_user');
            div.innerHTML = ("<div>" + "" + "</div>");
            if (!$.isEmptyObject(data.users)){
                $.each(data.users, function(index, value){
                        div.innerHTML += ("<div " + "id=search" + value.pk  + ">" + "</div>");
                        var r2;
                        if (pk != 0){
                            r2 = $('<input/>').attr({
                                type: "button",
                                class: "btn btn-primary btn-xs",
                                id: value.pk,
                                value: "+",
                                style: "margin: 5px",
                                onclick: "window.location.href='/account/chat_add_user/" +  pk + "/" + value.pk + "'"
                                });
                        }
                        else{
                            r2 = $('<input/>').attr({
                                type: "button",
                                class: "btn btn-primary btn-xs",
                                id: value.pk,
                                value: "→",
                                style: "margin: 5px",
                                onclick: "window.location.href='/account/chat_control/" + value.pk + "'"
                                });
                        }
                        $("#search"+value.pk).append( r2, value.full_name);
                });
            }
            else {
                div.innerHTML +=("<div>" + 'По вашему запросу ничего не найдено' + "</div>")
            }
        },
        error: function(){
            alert('error');
        }
    });
    event.preventDefault();
}

function div_bottom(id){
                var objDiv = document.getElementById(id);
                objDiv.scrollTop = objDiv.scrollHeight;
}

function linkify(inputText) {
    var pattern = /([-a-zA-Z0-9@:%_\+.~#?&\/\/=]{2,256}\.[a-z]{2,4}\b(\/?[-a-zA-Z0-9@:%_\+.~#?&\/\/=]*)?)/gi;
    var replacedText = inputText.replace(pattern, function(s){
      var str = (/:\/\//.exec(s) === null ? "http://" + s : s );
      return "<a href=\""+ str + "\">" + s /*s*/ + "</a>";
    });zxc88DSA
    return replacedText;
}

$(function() {
    $('.btn-comment-reply').each(function(e){
        var baton = $(this);
        baton.on('click', function(){
            $('#comment_reply_to').val($(this).attr('data-comment-id'));
            $('#comment_reply_to_fullname').html($(this).attr('data-comment-fullname'));
            $('#comment_reply_to_p').show();
        })
    })

$(".message-alert").each(function(){
        $(this).alert().fadeIn(200);
    })
});

$(function() {
    $("#id_ShippingForm-shipping_1").on("change",function(){
//        alert(this.value);
        document.getElementById('adr').style.display='block';
        document.getElementById('bbb').style.display='none';
    });
    $("#id_ShippingForm-shipping_0").on("change",function(){
//        alert(this.value);
        document.getElementById('adr').style.display='none';
        document.getElementById('bbb').style.display='block';
    });
});

function validation_cart(button, stat, object_id) {
    var btn = $(button);
    $.ajax(
        {
            type: 'get',
            url: '/account/validation_cart/',
            data: {stat: stat, pk: object_id},
            success: function(data){
                if(stat == 'ok'){
                    $('span#cost_'+object_id).text(data.cost)
                    $('span#cart_price_'+object_id).text(data.part_price);
                    $('span#cart_amount').text(data.amount_price);
                    document.getElementById('base_cost_'+object_id).style.display='none';
                    document.getElementById('btn_'+object_id).style.display='none';
                }
                if(stat == 'fail'){
                    if (data.part_list){
                        $.each(data.part_list, function(){
        //                        $('tr#cart_part_'+this).css('backgroundColor', 'Salmon')
        //                        $('span#base_count_'+this).css('backgroundColor', 'Salmon')
                            $('span#base_count_'+this).text('Доступно - '+data.count[this]+'ед.').css( "color","salmon" )
                        });
                    }
                    if (data.cost_list){
                        $.each(data.cost_list, function(){
                            document.getElementById('base_cost_'+this).style.display='block';
                            document.getElementById('btn_'+this).style.display='block';
    //                        $('span#base_cost_'+this).style.display='block';
//                            $('span#btn_'+this).text('Новая стоимость - '+data.price[this])
                            $('span#base_cost_'+this).text('Новая цена - '+data.price[this]+' тг.').css( "color","salmon")
                        });
                    }
                    if (data.code_a == 1){
                        location.href = '/account/checkout_cart/'
                    }
                }
            },
            error: function(data){
                alert('Произошла непридведенная ошибка. Обратитесь в службу поддержки.')
            }
    });
    event.preventDefault();
}

$(document).ready(function () {
    $("p img").click(function(){
        if (this.src != "") {
            $('body').append('<table id="FixedBlack" class="FixedBlack"><tr><td style="text-align: center;"><div align="center"><img src="" id="im" class="im" /></div></td></tr></table>');
            $("img#im").attr("src", this.src);
            $("#FixedBlack").show().fadeTo(200, 1);
            $("#im").show().fadeTo(0.5, 1);
        }
    });
    $(document).on("click", "#FixedBlack", function () {
        $("img#im").fadeOut(500);
        $("table#FixedBlack").remove();
    })
});