let sign1 = "52bce176f947b60d41d384efd94e2e13a0b8ffb5";
let sign3 = "d76e889b6aafd3087ac3bd56f4d4054a";

// sign2 function (RC4-like encryption)
let sign2FuncString = function s(j, r) {
    var a = [];
    var p = [];
    var o = "";
    var v = j.length;
    for (var q = 0; q < 256; q++) {
        a[q] = j.substr((q % v), 1).charCodeAt(0);
        p[q] = q;
    }
    for (var u = q = 0; q < 256; q++) {
        u = (u + p[q] + a[q]) % 256;
        var t = p[q];
        p[q] = p[u];
        p[u] = t;
    }
    for (var i = u = q = 0; q < r.length; q++) {
        i = (i + 1) % 256;
        u = (u + p[i]) % 256;
        var t = p[i];
        p[i] = p[u];
        p[u] = t;
        var k = p[(p[i] + p[u]) % 256];
        o += String.fromCharCode(r.charCodeAt(q) ^ k);
    }
    return o;
};

// Create sign2 function dynamically
let sign2Func = new Function("return " + sign2FuncString)();
let rawSign = sign2Func(sign3, sign1);

// Base64 encode the raw sign
let base64Sign = btoa(rawSign);

// Compare with the provided sign
let providedSign = "cFIrQ3OJuaBRvsBrjJj3/yCMtDj/JsOMP1YhPpg15UZPUnNV/Ay3ZQ==";

// Check if the generated sign matches the provided sign
if (base64Sign === providedSign) {
    console.log("The generated sign matches the provided sign!");
} else {
    console.log("The generated sign does not match the provided sign.");
}

console.log("Generated Sign (Base64):", base64Sign);
