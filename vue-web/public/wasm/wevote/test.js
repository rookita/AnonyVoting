// 字符串转16进制
// function str2hex(str) {
//   if (str === "") {
//     return "";
//   }
//   var arr = [];
//   //arr.push("0x");
//   for (var i = 0; i < str.length; i++) {
//     arr.push(str.charCodeAt(i).toString(16));
//   }
//   return arr.join('');
// }

function test() {
  para = setup(256)
  n = 10
  var man = new Array(n)
  var elgamal_pubs = new Array(n)
  var ecdsa_pubs = new Array(n)
  signs = new Array(n)
  for (let i = 0; i < n; i++) {
    ecdsa_pubs[i] = { x: "0", y: "0" }
  }

  var m = new Array(n)
  var C = new Array(n)
  var jsonC = new Array(n)
  var Cx = new Array(n) //C^x
  for (let i = 0; i < n; i++) {
    man[i] = generatekey(para)  //模拟产生n对公私钥
    elgamal_pubs[i] = man[i].pk
    //用于签名的公私钥
    ecdsa_pubs[i].x = man[i].ecdsa_pk_x
    ecdsa_pubs[i].y = man[i].ecdsa_pk_y
    if (i % 2)
      m[i] = -i
    else
      m[i] = i
  }
  //console.log(ecdsa_pubs)
  //console.log(man)
  PK = generatepub(para, elgamal_pubs, n)   //产生合公钥PK, 传入参数见main.go的同名函数
  console.log("PK:", PK)

  PK1 = generatepub(para, elgamal_pubs, n)   //产生合公钥PK, 传入参数见main.go的同名函数
  console.log("PK1:", PK1)

  r = "123456" //实际r由用户随机产生
  for (let i = 0; i < n; i++) {
    C[i] = encrypt(para, r, PK, m[i], 0)    //0表示m是正数
    //console.log(C[i])
    jsonC[i] = JSON.stringify(C[i])
    signs[i] = sign(jsonC[i], man[i].ecdsa_sk, ecdsa_pubs[i])
  }
  console.log(jsonC)
  //console.log(signs)
  countC = count(para, C, signs, ecdsa_pubs, jsonC, n)

  //console.log("CountC:", countC)
  for (let i = 0; i < n; i++) {
    Cx[i] = decrypt0(para, countC.C1, man[i].sk)
  }
  //console.log("Cx:", Cx)
  //console.log("C2:", countC.C2)
  //console.log("Cx:", Cx)
  max = 100 //max为暴力破解上限
  bsum = decrypt1(para, countC.C2, Cx, n, max)
  console.log("b:", bsum) //sum[m]
}
// 字符串转16进制
function str2hex(str) {
  if (str === "") {
    return "";
  }
  var arr = [];
  //arr.push("0x");
  for (var i = 0; i < str.length; i++) {
    arr.push(str.charCodeAt(i).toString(16));
  }
  return arr.join('');
}

function hex2str(hex) {
  var trimedStr = hex.trim();
  var rawStr = trimedStr.substr(0, 2).toLowerCase() === "0x" ? trimedStr.substr(2) : trimedStr;
  var len = rawStr.length;
  if (len % 2 !== 0) {
    alert("Illegal Format ASCII Code!");
    return "";
  }
  var curCharCode;
  var resultStr = [];
  for (var i = 0; i < len; i = i + 2) {
    curCharCode = parseInt(rawStr.substr(i, 2), 16);
    resultStr.push(String.fromCharCode(curCharCode));
  }
  return resultStr.join("");
}

function test1() {
  para = setup1(256);
  //console.log(para)
  var man = new Array()
  var elgamal_pubs = new Array()
  var ring_pubs = new Array()
  var n = 3
  //m = "secret"  //秘密值需要转为16进制,无需0x前缀
  var m = new Array()
  console.log(str2hex(m))
  for (var i = 0; i < n; i++) { //生成10个人的公私钥对
    man.push(generatekey1(para))
    elgamal_pubs.push(man[i].elgamal_pk)
    ring_pubs.push(man[i].ring_pk)
    m.push(encodeURIComponent("汪子凯"))
  }
  console.log(man)
  sender = man[0];
  CE = generatee(para, elgamal_pubs, n)
  //console.log(CE)
  k = 2
  r = CE //r是门限的秘密值，后续可用其他方式生成， 格式为无0x前缀的hex字符串
  C = new Array(n)
  signs = new Array(n)
  for (var i = 0; i < n; i++) {
    C[i] = encrypt1(para, n, k, r, str2hex(m[i]), CE, elgamal_pubs)
    signs[i] = sign1(man[i].ring_sk, ring_pubs, JSON.stringify(C[i]), i, n)
  }
  //signs[5] = "0"
  console.log(signs[1])
  //console.log(str2hex(m),C)
  console.log(C)
  var x = new Array()
  var y = new Array()
  for (var j = 0; j < n; j++) { //解密每一个voter的密文
    var tmpx = new Array()
    var tmpy = new Array()
    //判断签名
    if (!verify(signs[j], JSON.stringify(C[j]))) {
      console.log(j)
      continue
    }
    for (var i = 0; i < k; i++) {  //需要至少k个，这里取前5个
      tmpx.push(C[j].x[i])
      tmpy.push(decrypt00(para, C[j].g_r, C[j].y[i], man[i].elgamal_sk))
      console.log("tmpy", decrypt00(para, C[j].g_r, C[j].y[i], man[i].elgamal_sk))
    }
    console.log("tmpy", tmpy)
    x.push(tmpx)
    y.push(tmpy)
  }

  console.log(y)
  //C[i]:g_r, m * CE ^ r, x, y(解密后的y)

  console.log("encrypt success")

  var mm = new Array() //mm为解密后明文数组
  for (var i = 0; i < n; i++) {
    C[i].x = x[i]
    C[i].y = y[i]
    mm.push(decrypt11(para, C[i], CE, k))
  }

  console.log(mm)
  for (let i = 0; i < n; i++) {
    console.log(decodeURIComponent(hex2str(mm[i])))
  }
}
