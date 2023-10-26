function loadRecommendation() {
    const xhttp = new XMLHttpRequest();
    xhttp.onload = function () {
        const recommend = document.getElementById("recommend");
        if (recommend == undefined) {
            return;
        }
        if (xhttp.status === 200) {
            const data = JSON.parse(xhttp.responseText); // Parse the JSON response
            if (data.length == 0) {
                recommend.innerHTML += `<p style='font-size:20px;text-align:center;margin:50px;font-weight:bold;'>No Pets Found</p>`;
                return;
            }
            recommend.innerHTML = "";
            data.forEach(function (item) {
                if (recommend) {
                    recommend.innerHTML += `
                    <div class="row">
                        <div class="container">
                            <div class="wrapper">
                                <div class="product-img">
                                    <img src="`+ item.image + `" height="420" width="410">
                                </div>
                                <div class="product-info">
                                    <div class="product-text">
                                        <h1>`+ item.breed + `</h1><br>
                                        <h3>Seller mail : `+ item.seller_email + `</h3>
                                        <h3>Compatibility Score : `+ item.score + `</h3>
                                    </div>
                                    <div class="product-price-btn">
                                        <p><span>₹`+ item.price + `</span></p>
                                        <button type="button" class="bg-info" onclick="window.location.href ='/confirmation?id=`+ item.id + `'">Buy Now</button>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>`;
                } else {
                }
            });
        }
    };
    xhttp.open("POST", "/getRecommended", true);
    xhttp.send();
}


function loadAdoption() {
    const xhttp = new XMLHttpRequest();
    xhttp.onload = function () {
        const recommend = document.getElementById("adopt");
        if (recommend == undefined) {
            return;
        }
        if (xhttp.status === 200) {
            const data = JSON.parse(xhttp.responseText); // Parse the JSON response
            if (data.length == 0) {
                recommend.innerHTML += `<p style='font-size:20px;text-align:center;margin:50px;font-weight:bold;'>No Pets Found</p>`;
                return;
            }
            console.log(data);
            recommend.innerHTML = "";
            data.forEach(function (item) {
                recommend.innerHTML += `
                <div class="row">
                    <div class="container">
                        <div class="wrapper">
                            <div class="product-img">
                                <img src="`+ item.image + `" height="420" width="410">
                            </div>
                            <div class="product-info">
                                <div class="product-text">
                                    <h1>`+ item.breed + `</h1><br>
                                    <h3>Seller mail : `+ item.seller_email + `</h3>
                                    <h3>Compatibility Score : `+ item.score + `</h3>
                                </div>
                                <div class="product-price-btn">
                                    <button type="button" class="bg-info" onclick="window.location.href ='/confirmation?id=`+ item.id + `'">Buy Now</button>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>`;
            });
        }
    };
    xhttp.open("POST", "/getAdoption", true);
    xhttp.send();
}

function loadOrder() {
    const xhttp = new XMLHttpRequest();
    xhttp.onload = function () {
        const sell = document.getElementById("sell");
        if (sell == undefined) {
            return;
        }
        sell.innerHTML = "";
        const buy = document.getElementById("buy");
        if (buy == undefined) {
            return;
        }
        buy.innerHTML = "";
        if (xhttp.status === 200) {
            const data = JSON.parse(xhttp.responseText); // Parse the JSON response
            if (data.length == 0) {
                sell.innerHTML += `<p style='font-size:20px;text-align:center;margin:50px;font-weight:bold;'>No Pets Found</p>`;
                return;
            }
            data[0].forEach(function (item) {
                if (sell) {
                    if (item.price == "0") {
                        //adoption
                        if (item.seller_confirm == "no") {
                            sell.innerHTML += `<div class="row">
                            <div class="container">
                                <div class="wrapper">
                                    <div class="product-img">
                                        <img src="`+ item.image + `" height="420" width="410">
                                    </div>
                                    <div class="product-info">
                                        <div class="product-text">
                                            <h1>`+ item.breed + `</h1><br>
                                            <h3>Seller mail : `+ item.seller + `</h3>
                                            <h3>Buyer mail : `+ item.buyer + `</h3>
                                        </div>
                                        <div class="product-price-btn">
                                            <button type="button" onclick="window.location.href ='/confirm1?id=` + item.id + `'">Confirm</button>
                                            <button type="button" onclick="window.location.href ='/cancel1?id=`+ item.id + `'">Cancel</button>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>`;
                        } else if (item.buyer_confirm == "no") {
                            sell.innerHTML += `<div class="row">
                            <div class="container">
                                <div class="wrapper">
                                    <div class="product-img">
                                        <img src="`+ item.image + `" height="420" width="410">
                                    </div>
                                    <div class="product-info">
                                        <div class="product-text">
                                            <h1>`+ item.breed + `</h1><br>
                                            <h3>Seller mail : `+ item.seller + `</h3>
                                            <h3>Buyer mail : `+ item.buyer + `</h3>
                                        </div>
                                        <div class="product-price-btn">
                                            <button type="button" class="bg-info">Waiting for Buyer Confirmation</button>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>`;
                        } else {
                            sell.innerHTML += `<div class="row">
                            <div class="container">
                                <div class="wrapper">
                                    <div class="product-img">
                                        <img src="`+ item.image + `" height="420" width="410">
                                    </div>
                                    <div class="product-info">
                                        <div class="product-text">
                                            <h1>`+ item.breed + `</h1><br>
                                            <h3>Seller mail : `+ item.seller + `</h3>
                                            <h3>Buyer mail : `+ item.buyer + `</h3>
                                        </div>
                                        <div class="product-price-btn">
                                            <button type="button" class="bg-success">Order Confirmed</button>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>`;
                        }
                    } else {
                        //sell-buy
                        if (item.seller_confirm == "no") {
                            sell.innerHTML += `<div class="row">
                            <div class="container">
                                <div class="wrapper">
                                    <div class="product-img">
                                        <img src="`+ item.image + `" height="420" width="410">
                                    </div>
                                    <div class="product-info">
                                        <div class="product-text">
                                            <h1>`+ item.breed + `</h1><br>
                                            <h3>Seller mail : `+ item.seller + `</h3>
                                            <h3>Buyer mail : `+ item.buyer + `</h3>
                                        </div>
                                        <div class="product-price-btn">
                                            <p><span>₹`+ item.price + `</span></p>
                                            <button type="button" onclick="window.location.href ='/confirm1?id=` + item.id + `'">Confirm</button>
                                            <button type="button" onclick="window.location.href ='/cancel1?id=`+ item.id + `'">Cancel</button>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>`;
                        } else if (item.buyer_confirm == "no") {
                            sell.innerHTML += `<div class="row">
                            <div class="container">
                                <div class="wrapper">
                                    <div class="product-img">
                                        <img src="`+ item.image + `" height="420" width="410">
                                    </div>
                                    <div class="product-info">
                                        <div class="product-text">
                                            <h1>`+ item.breed + `</h1><br>
                                            <h3>Seller mail : `+ item.seller + `</h3>
                                            <h3>Buyer mail : `+ item.buyer + `</h3>
                                        </div>
                                        <div class="product-price-btn">
                                            <p><span>₹`+ item.price + `</span></p>
                                            <button type="button" class="bg-info">Waiting for Buyer Confirmation</button>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>`;
                        } else {
                            sell.innerHTML += `<div class="row">
                            <div class="container">
                                <div class="wrapper">
                                    <div class="product-img">
                                        <img src="`+ item.image + `" height="420" width="410">
                                    </div>
                                    <div class="product-info">
                                        <div class="product-text">
                                            <h1>`+ item.breed + `</h1><br>
                                            <h3>Seller mail : `+ item.seller + `</h3>
                                            <h3>Buyer mail : `+ item.buyer + `</h3>
                                        </div>
                                        <div class="product-price-btn">
                                            <p><span>₹`+ item.price + `</span></p>
                                            <button type="button" class="bg-success">Order Confirmed</button>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>`;
                        }
                    }
                } else {
                }
            });

            data[1].forEach(function (item) {
                if (buy) {
                    if (item.price == "0") {
                        //adoption
                        if (item.buyer_confirm == "no") {
                            buy.innerHTML += `<div class="row">
                            <div class="container">
                                <div class="wrapper">
                                    <div class="product-img">
                                        <img src="`+ item.image + `" height="420" width="410">
                                    </div>
                                    <div class="product-info">
                                        <div class="product-text">
                                            <h1>`+ item.breed + `</h1><br>
                                            <h3>Seller mail : `+ item.seller + `</h3>
                                            <h3>Buyer mail : `+ item.buyer + `</h3>
                                        </div>
                                        <div class="product-price-btn">
                                            <button type="button" onclick="window.location.href ='/confirm2?id=` + item.id + `'">Confirm</button>
                                            <button type="button" onclick="window.location.href ='/cancel2?id=`+ item.id + `'">Cancel</button>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>`;
                        } else if (item.seller_confirm == "no") {
                            buy.innerHTML += `<div class="row">
                            <div class="container">
                                <div class="wrapper">
                                    <div class="product-img">
                                        <img src="`+ item.image + `" height="420" width="410">
                                    </div>
                                    <div class="product-info">
                                        <div class="product-text">
                                            <h1>`+ item.breed + `</h1><br>
                                            <h3>Seller mail : `+ item.seller + `</h3>
                                            <h3>Buyer mail : `+ item.buyer + `</h3>
                                        </div>
                                        <div class="product-price-btn">
                                            <button type="button" class="bg-info">Waiting for Seller Confirmation</button>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>`;
                        } else {
                            buy.innerHTML += `<div class="row">
                            <div class="container">
                                <div class="wrapper">
                                    <div class="product-img">
                                        <img src="`+ item.image + `" height="420" width="410">
                                    </div>
                                    <div class="product-info">
                                        <div class="product-text">
                                            <h1>`+ item.breed + `</h1><br>
                                            <h3>Seller mail : `+ item.seller + `</h3>
                                            <h3>Buyer mail : `+ item.buyer + `</h3>
                                        </div>
                                        <div class="product-price-btn">
                                            <button type="button" class="bg-success">Order Confirmed</button>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>`;
                        }
                    } else {
                        //sell-buy
                        if (item.buyer_confirm == "no") {
                            buy.innerHTML += `<div class="row">
                            <div class="container">
                                <div class="wrapper">
                                    <div class="product-img">
                                        <img src="`+ item.image + `" height="420" width="410">
                                    </div>
                                    <div class="product-info">
                                        <div class="product-text">
                                            <h1>`+ item.breed + `</h1><br>
                                            <h3>Seller mail : `+ item.seller + `</h3>
                                            <h3>Buyer mail : `+ item.buyer + `</h3>
                                        </div>
                                        <div class="product-price-btn">
                                            <p><span>₹`+ item.price + `</span></p>
                                            <button type="button" onclick="window.location.href ='/confirm2?id=` + item.id + `'">Confirm</button>
                                            <button type="button" onclick="window.location.href ='/cancel2?id=`+ item.id + `'">Cancel</button>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>`;
                        } else if (item.seller_confirm == "no") {
                            buy.innerHTML += `<div class="row">
                            <div class="container">
                                <div class="wrapper">
                                    <div class="product-img">
                                        <img src="`+ item.image + `" height="420" width="410">
                                    </div>
                                    <div class="product-info">
                                        <div class="product-text">
                                            <h1>`+ item.breed + `</h1><br>
                                            <h3>Seller mail : `+ item.seller + `</h3>
                                            <h3>Buyer mail : `+ item.buyer + `</h3>
                                        </div>
                                        <div class="product-price-btn">
                                            <p><span>₹`+ item.price + `</span></p>
                                            <button type="button" class="bg-info">Waiting for Seller Confirmation</button>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>`;
                        } else {
                            buy.innerHTML += `<div class="row">
                            <div class="container">
                                <div class="wrapper">
                                    <div class="product-img">
                                        <img src="`+ item.image + `" height="420" width="410">
                                    </div>
                                    <div class="product-info">
                                        <div class="product-text">
                                            <h1>`+ item.breed + `</h1><br>
                                            <h3>Seller mail : `+ item.seller + `</h3>
                                            <h3>Buyer mail : `+ item.buyer + `</h3>
                                        </div>
                                        <div class="product-price-btn">
                                            <p><span>₹`+ item.price + `</span></p>
                                            <button type="button" class="bg-success">Order Confirmed</button>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>`;
                        }
                    }

                } else {
                }
            });
        }
    };
    xhttp.open("POST", "/getOrders", true);
    xhttp.send();
}

function loadsell() {
    const xhttp = new XMLHttpRequest();
    xhttp.onload = function () {
        const recommend = document.getElementById("seller");
        if (recommend == undefined) {
            return;
        }
        if (xhttp.status === 200) {
            const data = JSON.parse(xhttp.responseText); // Parse the JSON response
            if (data.length == 0) {
                recommend.innerHTML += `<p style='font-size:20px;text-align:center;margin:50px;font-weight:bold;'>No Pets Found</p>`;
                return;
            }
            recommend.innerHTML = "";
            data.forEach(function (item) {
                if (recommend) {
                    recommend.innerHTML += `
                    <div class="row">
                        <div class="container">
                            <div class="wrapper">
                                <div class="product-img">
                                    <img src="`+ item.image + `" height="420" width="410">
                                </div>
                                <div class="product-info">
                                    <div class="product-text">
                                        <h1>`+ item.breed + `</h1><br>
                                    </div>
                                    <div class="product-price-btn">
                                        <p><span>₹`+ item.price + `</span></p>
                                        <button type="button" class="bg-info" onclick="window.location.href ='/remove?id=`+ item.id + `'">remove</button>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>`;
                } else {
                }
            });
        }
    };
    xhttp.open("POST", "/getsell", true);
    xhttp.send();
}

loadAdoption();
loadRecommendation();
loadOrder();
loadsell();