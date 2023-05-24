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

function test() {
  para = setup1(256);
  //console.log(para)
  var man = new Array()
  var elgamal_pubs = new Array()
  var ring_pubs = new Array()
  var n = 2
  //m = "secret"  //秘密值需要转为16进制,无需0x前缀
  var m = new Array()
  console.log(str2hex(m))
  for (var i = 0; i < n; i++) { //生成10个人的公私钥对
    man.push(generatekey1(para))
    elgamal_pubs.push(man[i].elgamal_pk)
    ring_pubs.push(man[i].ring_pk)
    m.push("汪子凯汪子凯")
  }
  //console.log(man)
  sender = man[0];
  CE = generatee(para, elgamal_pubs, n)
  //console.log(CE)
  k = 2
  r = CE //r是门限的秘密值，后续可用其他方式生成， 格式为无0x前缀的hex字符串
  C = new Array(n)
  signs = new Array(n)
  for (var i = 0; i < n; i++) {
    C[i] = encrypt1(para, n, k, r, str2hex(escape(m[i])), CE, elgamal_pubs)
    signs[i] = sign1(man[i].ring_sk, ring_pubs, JSON.stringify(C[i]), i, n)
  }
  //signs[5] = "0"
  // console.log(signs)
  console.log(escape(m[1]).length)
  console.log(C[0])
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
    for (var i = 0; i < 2; i++) {  //需要至少k个，这里取前5个
      tmpx.push(C[j].x[i])
      tmpy.push(decrypt00(para, C[j].g_r, C[j].y[i], man[i].elgamal_sk))
      console.log("tmpy", decrypt00(para, C[j].g_r, C[j].y[i], man[i].elgamal_sk))
    }
    console.log("tmpy", tmpy)
    x.push(tmpx)
    y.push(tmpy)
  }
  //x[i], y[i]

  //console.log(y)
  //C[i]:g_r, m * CE ^ r, x, y(解密后的y)

  console.log("encrypt success")

  var mm = new Array() //mm为解密后明文数组
  for (var i = 0; i < n; i++) {
    C[i].x = x[i]
    C[i].y = y[i]
    mm.push(decrypt11(para, C[i], CE, k))
  }

  console.log(mm)
  for (let i = 0; i < n; i++)
    console.log(hex2str(mm[i]))
}
