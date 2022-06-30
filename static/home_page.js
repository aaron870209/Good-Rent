//Get the button:
mybutton = document.getElementById("myBtn");

// When the user scrolls down 20px from the top of the document, show the button
window.onscroll = function() {scrollFunction()};

function scrollFunction() {
  if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
    mybutton.style.display = "block";
  } else {
    mybutton.style.display = "none";
  }
}

// When the user clicks on the button, scroll to the top of the document
function topFunction() {
  document.body.scrollTop = 0; // For Safari
  document.documentElement.scrollTop = 0; // For Chrome, Firefox, IE and Opera
}

function show_bar(){
    x = document.getElementById("menu")
    if (x.style.display === "none"){
        x.style.display = "block";
    }else{
        x.style.display = "none";
    }
}


function show_Taipei() {
  var x = document.getElementById("Taipei_region");
  var y = document.getElementById("New_Taipei_region")
  if (x.style.display === "none") {
    y.style.display = "none";
    x.style.display = "block";
  } else {
    x.style.display = "none";
  }
}


function show_New_Taipei() {
  var x = document.getElementById("New_Taipei_region");
  var y = document.getElementById("Taipei_region");
  if (x.style.display === "none") {
    y.style.display = "none";
    x.style.display = "block";
  } else {
    x.style.display = "none";
  }
}


function search(){
    var data_dict = {}
    var formEl_taipei = document.querySelectorAll('input[name="台北市地區"]');
    var checkboxEls_taipei = [];
    console.log(formEl_taipei)
    for (var i=0;i<formEl_taipei.length;i++){
        console.log(formEl_taipei[i].checked)
        console.log(formEl_taipei[i].value)
        if(formEl_taipei[i].checked === true){
        checkboxEls_taipei.push(formEl_taipei[i].getAttribute('value'))
    }
    }
    var formEl_new_taipei = document.querySelectorAll('input[name="新北市地區"]');
    var checkboxEls_new_taipei = [];
    console.log(formEl_new_taipei)
    for (var i=0;i<formEl_new_taipei.length;i++){
        console.log(formEl_new_taipei[i].checked)
        console.log(formEl_new_taipei[i].value)
        if(formEl_new_taipei[i].checked === true){
        checkboxEls_new_taipei.push(formEl_new_taipei[i].getAttribute('value'))
    }
    }
    var formEl_type = document.querySelectorAll('input[name="house_type"]');
    var checkboxEls_type = [];
    console.log(formEl_type)
    for (var i=0;i<formEl_type.length;i++){
        console.log(formEl_type[i].checked)
        console.log(formEl_type[i].value)
        if(formEl_type[i].checked === true){
        checkboxEls_type.push(formEl_type[i].getAttribute('value'))
    }
    }

    var formEl_rent = document.querySelectorAll('input[name="house_rent"]');
    var checkboxEls_rent = [];
    console.log(formEl_rent)
    for (var i=0;i<formEl_rent.length;i++){
        console.log(formEl_rent[i].checked)
        console.log(formEl_rent[i].value)
        if(formEl_rent[i].checked === true){
        checkboxEls_rent.push(formEl_rent[i].getAttribute('value'))
    }
    }

    data_dict["taipei"]=checkboxEls_taipei
    data_dict["new_taipei"]=checkboxEls_new_taipei
    data_dict["type"]=checkboxEls_type
    data_dict["rent"]=checkboxEls_rent
    console.log(data_dict)
    return data_dict
}


function item(data){
    console.log(data)
    for(var i = 0; i < data.length; i++){
        console.log(data[i].title)
        const div = document.createElement("div")
        div.className = "create_div"
        const link = document.createElement("a")
        link.href = "./detail?id="+data[i].house_id
        div.appendChild(link)
        const img = document.createElement("img");
        img.className = "img";
        img.style.width="20%";
        img.src = data[i].img;
        link.appendChild(img);
        const title = document.createElement("div");
        title.className = "title";
        title.innerHTML = '<h2>'+data[i].title+'</h2>';
        link.appendChild(title);
        const address = document.createElement("div");
        address.className = "address";
        address.innerHTML = '<h3>'+data[i].address+'</h3>'
        link.appendChild(address)
        const type = document.createElement("div");
        type.className = "house_type"
        type.innerHTML = '<h3>'+data[i].house_type+'</h3>'
        link.appendChild(type)
        const detail = document.createElement("div");
        detail.className = "detail";
        detail.innerHTML = '<h3>'+data[i].size+' | '+data[i].floor+'F</h3>'
        link.appendChild(detail)
        const price = document.createElement("div");
        price.className = "price";
        price.innerHTML = '<p>'+data[i].price+'元/月</p>';
        link.appendChild(price);
        const clear = document.createElement("div")
        clear.className = "clear"
        clear.innerHTML = '<hr class="downer_line2">'
        link.appendChild(clear)
        var recommendedProduct = document.getElementById("data");
        recommendedProduct.appendChild(div);
                    }
}


function search_ajax(){
    let data= search()
    console.log(data)
    var xmlhttp = new XMLHttpRequest();
    var url = "/search";
    xmlhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            let data = this.response
            console.log(data)
            document.getElementById('data').innerHTML = ''
            item(data["data"])
        };
    };
    xmlhttp.open("POST", url, true);
    xmlhttp.setRequestHeader('Content-Type','application/x-www-form-urlencode');
    xmlhttp.responseType = 'json';
    xmlhttp.send(JSON.stringify({
        "data": data
    }));
}

