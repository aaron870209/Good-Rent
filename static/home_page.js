//Get the button:
mybutton = document.getElementById("myBtn");

// When the user scrolls down 20px from the top of the document, show the button
window.onscroll = function() {
	scrollFunction()
};

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

function show_detail(tag) {
	if (tag === 1) {
		x = document.getElementById("tag1_detail")
		x.style.display = "block"
	} else if (tag === 2) {
		x = document.getElementById("tag2_detail")
		x.style.display = "block"
	} else {
		x = document.getElementById("tag3_detail")
		x.style.display = "block"
	}
}

function hide_detail(tag) {
	if (tag === 1) {
		x = document.getElementById("tag1_detail")
		x.style.display = "none"
	} else if (tag === 2) {
		x = document.getElementById("tag2_detail")
		x.style.display = "none"
	} else {
		x = document.getElementById("tag3_detail")
		x.style.display = "none"
	}

}

function show_bar() {
	x = document.getElementById("menu")
	y = document.getElementById("dropdownMenuButton1")
	if (x.style.display === "none") {
		x.style.display = "block";
		y.style.marginRight = "28%";
	} else {
		x.style.display = "none";
		y.style.marginRight = "11px";
	}
}


function show_Taipei() {
	var x = document.getElementById("Taipei_region");
	var y = document.getElementById("New_Taipei_region")
	if (x.style.display === "none") {
		y.style.display = "none";
		x.style.display = "block";
	}
}


function show_New_Taipei() {
	var x = document.getElementById("New_Taipei_region");
	var y = document.getElementById("Taipei_region");
	if (x.style.display === "none") {
		y.style.display = "none";
		x.style.display = "block";
	}
}


function search() {
	var data_dict = {}
	var formEl_taipei = document.querySelectorAll('input[name="台北市地區"]');
	var checkboxEls_taipei = [];
	for (var i = 0; i < formEl_taipei.length; i++) {
		if (formEl_taipei[i].checked === true) {
			checkboxEls_taipei.push(formEl_taipei[i].getAttribute('value'))
		}
	}
	var formEl_new_taipei = document.querySelectorAll('input[name="新北市地區"]');
	var checkboxEls_new_taipei = [];
	for (var i = 0; i < formEl_new_taipei.length; i++) {
		if (formEl_new_taipei[i].checked === true) {
			checkboxEls_new_taipei.push(formEl_new_taipei[i].getAttribute('value'))
		}
	}
	var formEl_type = document.querySelectorAll('input[name="house_type"]');
	var checkboxEls_type = [];
	for (var i = 0; i < formEl_type.length; i++) {
		if (formEl_type[i].checked === true) {
			checkboxEls_type.push(formEl_type[i].getAttribute('value'))
		}
	}

	var formEl_rent = document.querySelectorAll('input[name="house_rent"]');
	var checkboxEls_rent = [];
	for (var i = 0; i < formEl_rent.length; i++) {
		if (formEl_rent[i].checked === true) {
			checkboxEls_rent.push(formEl_rent[i].getAttribute('value'))
		}
	}

	data_dict["taipei"] = checkboxEls_taipei
	data_dict["new_taipei"] = checkboxEls_new_taipei
	data_dict["type"] = checkboxEls_type
	data_dict["rent"] = checkboxEls_rent
	return data_dict
}


function item(data) {
	var data1 = data["data"]
	for (var i = 0; i < data1.length; i++) {
		const div = document.createElement("div")
		div.className = "create_div"
		const link = document.createElement("a")
		link.href = "./detail?id=" + data1[i].house_id
		div.appendChild(link)
		const img = document.createElement("img");
		img.className = "img";
		img.style.width = "20%";
		img.src = data1[i].img;
		link.appendChild(img);
		const title = document.createElement("div");
		title.className = "title";
		title.innerHTML = '<h2>' + data1[i].title + '</h2>';
		link.appendChild(title);
		const address = document.createElement("div");
		address.className = "address";
		address.innerHTML = '<h3>' + data1[i].address + '</h3>'
		link.appendChild(address)
		const type = document.createElement("div");
		type.className = "house_type"
		type.innerHTML = '<h3>' + data1[i].house_type + '</h3>'
		link.appendChild(type)
		const detail = document.createElement("div");
		detail.className = "detail";
		detail.innerHTML = '<h3>' + data1[i].size + ' | ' + data1[i].floor + 'F</h3>'
		link.appendChild(detail)
		const price = document.createElement("div");
		price.className = "price";
		price.innerHTML = '<p>' + data1[i].price + '元/月</p>';
		link.appendChild(price);
		const clear = document.createElement("div")
		clear.className = "clear"
		clear.innerHTML = '<hr class="downer_line2">'
		link.appendChild(clear)
		var recommendedProduct = document.getElementById("data");
		recommendedProduct.appendChild(div);
	}
	var page = data.page
	var previous_page = document.getElementById("previous_page")
	previous_page.innerHTML = ''
	if (page == 0) {
		previous_page.innerHTML = '<a id="上一頁1" class="page-link" onclick="page_control(2)">Previous</a>'
	} else {
		previous_page.innerHTML = '<a id="上一頁1" class="page-link" onclick="search_ajax(' + (page - 1) + ')">Previous</a>'
	}
	var next_page = document.getElementById("next_page")
	let total = data.total
	var limit_page = parseInt(total / 15)
	if (page == limit_page) {
		next_page.innerHTML = ''
		next_page.innerHTML = '<a id="下一頁1" class="page-link" onclick="page_control(1)">next</a>'
	} else {
		var next_page = document.getElementById("next_page")
		next_page.innerHTML = ''
		next_page.innerHTML = '<a id="下一頁1" class="page-link" onclick="search_ajax(' + (page + 1) + ')">next</a>'
	}
}


function page_control(tag) {
	if (tag == 1) {
		alert("這是最後一頁囉！！")
	} else {
		alert("這是第一頁囉！！")
	}
}




function search_ajax(page) {
	var x = document.getElementById("home_page_paging");
	var y = document.getElementById("tag_page_paging")
	x.style.display = "none";
	y.style.display = "block";
	let data = search()
	var xmlhttp = new XMLHttpRequest();
	var url = "/search";
	xmlhttp.onreadystatechange = function() {
		if (this.readyState == 4 && this.status == 200) {
			let data = this.response
			document.documentElement.scrollTop = 0;
			document.getElementById('data').innerHTML = ''
			item(data)
			document.getElementById('total').innerHTML = ''
			document.getElementById('total').innerHTML = '<h1>為您找到 ' + data["total"] + ' 間適合的房子</h1>'
		};
	};


	xmlhttp.open("POST", url, true);
	xmlhttp.setRequestHeader('Content-Type', 'application/x-www-form-urlencode');
	xmlhttp.responseType = 'json';
	xmlhttp.send(JSON.stringify({
		"data": data,
		"page": page
	}));
}