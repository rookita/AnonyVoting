package main

import (
	crand "crypto/rand"
	"elgamir/elgamal"
	"elgamir/ring"
	"elgamir/sharesecret"
	"encoding/hex"
	"fmt"
	"math/big"
	"syscall/js"
)

func getpara(jspara js.Value) elgamal.Elgamalpara {
	P, Q, G := hextoInt(jspara.Get("P").String()), hextoInt(jspara.Get("Q").String()), hextoInt(jspara.Get("G").String())
	return elgamal.Elgamalpara{P, Q, G}
}

//将big.Int转为Hex的字符串，大端序
//len为字节数
func inttoHex(a *big.Int, len int) string {
	v := a.FillBytes(make([]byte, len))
	return hex.EncodeToString(v)
}

func inttoHex1(a *big.Int) string {
	return hex.EncodeToString(a.Bytes())
}

//将Hex字符串转为big.Int
func hextoInt(h string) *big.Int {
	v := big.NewInt(0)
	v.SetString(h, 16)
	return v
}

//初始化系统参数, 模数p, 生成元g, Q
//args[0](int)为模数p位数，默认为128
//返回值为object
func setup1(this js.Value, args []js.Value) interface{} {
	bits := 128
	if len(args) != 0 {
		bits = args[0].Int()
	}
	para, _ := elgamal.Setup(bits)
	pstr := inttoHex(para.P, int(bits/8))
	qstr := inttoHex(para.Q, int(bits/8))
	gstr := inttoHex(para.G, int(bits/8))
	return js.ValueOf(map[string]interface{}{
		"P": pstr,
		"Q": qstr,
		"G": gstr,
	})
}

//生成公私钥
//args[0]为para对象
//返回object
func generatekey1(this js.Value, args []js.Value) interface{} {
	para := getpara(args[0])
	elgamal_pk, elgamal_sk := para.GenerateKey()
	ring_pk, ring_sk := ring.Generate(crand.Reader)
	//fmt.Println(pk)

	return js.ValueOf(map[string]interface{}{
		"elgamal_pk": inttoHex1(elgamal_pk.E),
		"elgamal_sk": inttoHex1(elgamal_sk.D),
		"ring_pk":    ring.ConfigEncodeKey(ring_pk),
		"ring_sk":    ring.ConfigEncodeKey(ring_sk),
	})
}

//生成合公钥E
//args[0] para, args[1]为参与者公钥, args[2]为参与人数
//返回合公钥
func generatee(this js.Value, args []js.Value) interface{} {
	para := getpara(args[0])
	n := args[2].Int()
	Pubs := make([]elgamal.PubKey, n)
	for i := 0; i < n; i++ {
		Pubs[i].E = hextoInt(args[1].Index(i).String())
		Pubs[i].P = para.P
		Pubs[i].G = para.G
	}
	CE := para.GeneratePub(Pubs)
	return js.ValueOf(inttoHex1(CE))
}

//生成多项式并加密
//args[0]为para对象 args[1]为n(参与人数), args[2]为k(门限阈值), args[3]为r(门限秘密值), args[4]为m(秘密值), args[5]为合公钥, args[6]为参与者公钥集合
//返回密文集合(object)
func encrypt1(this js.Value, args []js.Value) interface{} {
	para := getpara(args[0])
	n, k, r, m, CE := int64(args[1].Int()), int64(args[2].Int()), hextoInt(args[3].String()), hextoInt(args[4].String()), hextoInt(args[5].String())
	Pubs := make([]elgamal.PubKey, n)
	for i := 0; int64(i) < n; i++ {
		Pubs[i].E = hextoInt(args[6].Index(i).String())
		Pubs[i].P = para.P
		Pubs[i].G = para.G
	}
	C1 := para.Encrypt(m, r, CE)
	points := sharesecret.Distribute(para.P, r, n, k, Pubs)
	var X []interface{}
	var Y []interface{}
	for i := 0; int64(i) < n; i++ {
		X = append(X, inttoHex1(points[i].X))
		Y = append(Y, inttoHex1(points[i].Y))
	}
	return js.ValueOf(map[string]interface{}{
		"g_r": inttoHex1(C1[0]), //g ^ r
		"c":   inttoHex1(C1[1]), //m * E ^ r
		"x":   js.ValueOf(X),    //array
		"y":   js.ValueOf(Y),    //array,与x一一对应
	})

}

//解密y
//args[0]为para, args[1]为g_r, args[2]为c, args[3]为d
//返回值为Y
func decrypt00(this js.Value, args []js.Value) interface{} {
	para := getpara(args[0])
	g_r, c, d := hextoInt(args[1].String()), hextoInt(args[2].String()), hextoInt(args[3].String())
	pri := elgamal.PriKey{para.P, para.G, d, big.NewInt(0)}
	y := pri.Decrypt(g_r, c)
	yy := inttoHex1(y)
	return js.ValueOf(yy)
}

//解密m
//args[0]为para, args[1]为密文C, args[2]为合公钥CE, args[3]为点个数
//返回值为明文
func decrypt11(this js.Value, args []js.Value) interface{} {
	para := getpara(args[0])
	CE := hextoInt(args[2].String())
	_, c, X, Y, n := args[1].Get("g_r"), hextoInt(args[1].Get("c").String()), args[1].Get("x"), args[1].Get("y"), args[3].Int()
	x, y := []*big.Int{}, []*big.Int{}
	var i = 0
	for i = 0; i < n; i++ {
		x = append(x, hextoInt(X.Index(i).String()))
		y = append(y, hextoInt(Y.Index(i).String())) // (x[i], y[i])为一个点
	}
	rsum := big.NewInt(0)
	for i = 0; i < n; i++ {
		tmp := sharesecret.Recover(para.P, x, y[i], i)
		rsum.Add(rsum, tmp)
	}
	rsum.Mod(rsum, para.P)
	tmp := big.NewInt(0).Exp(CE, rsum, para.P)
	tmp.ModInverse(tmp, para.P)
	mm := big.NewInt(0).Mul(c, tmp)
	mm.Mod(mm, para.P)
	return js.ValueOf(inttoHex1(mm)) //明文
}

//产生签名
//args[0]为签名者私钥,args[1]为所有公钥, args[2]为message, args[3]签名者公钥次序,args[4]为公钥个数
//返回值为签名值(string)
func sign(this js.Value, args []js.Value) interface{} {
	//fmt.Println(n)
	var r []string
	nn := args[4].Int()
	for i := 0; i < nn; i++ {
		r = append(r, args[1].Index(i).String())
	}
	//fmt.Println(len(r))
	var ringKeys []ring.PublicKey
	for _, key := range r {
		pkBytes, _ := ring.ConfigDecodeKey(key)
		ringKeys = append(ringKeys, ring.PublicKey(pkBytes))
	}
	//fmt.Println(len(ringKeys))
	m := args[2].String()
	sk := args[0].String()
	privKeyBytes, _ := ring.ConfigDecodeKey(sk)
	privKey := ring.PrivateKey(privKeyBytes)
	//fmt.Println("Signing message...")
	sig, err := privKey.Sign(crand.Reader, []byte(m), ringKeys, args[3].Int())
	if err != nil {
		fmt.Println(err)
	}
	sigStr, _ := sig.Encode()
	return js.ValueOf(sigStr)
}

//args[0]为signature,args[1]为message
//返回值为bool值
func verify(this js.Value, args []js.Value) interface{} {
	sigStr := args[0].String()
	m := args[1].String()
	sig := &ring.Signature{}
	err := sig.Decode(sigStr)
	if err != nil {
		fmt.Println(err)
	}
	valid := sig.Verify([]byte(m))
	return js.ValueOf(valid)
}

func registerCallbacks() {
	js.Global().Set("setup1", js.FuncOf(setup1))
	js.Global().Set("generatekey1", js.FuncOf(generatekey1))
	js.Global().Set("generatee", js.FuncOf(generatee))
	js.Global().Set("encrypt1", js.FuncOf(encrypt1))
	js.Global().Set("decrypt00", js.FuncOf(decrypt00))
	js.Global().Set("decrypt11", js.FuncOf(decrypt11))
	js.Global().Set("sign1", js.FuncOf(sign))
	js.Global().Set("verify", js.FuncOf(verify))
}

func main() {
	c := make(chan struct{}, 0)
	fmt.Println("WASM Go Initialized")
	// register functions
	registerCallbacks()
	<-c
}

/*
func main() {
	m, r := big.NewInt(7), big.NewInt(5)
	k, n := int64(8), int64(10)
	para, _ := elgamal.Setup(128)
	i := int64(0)
	Pubs := make([]elgamal.PubKey, 10)
	Pris := make([]elgamal.PriKey, 10)
	X := make([]*big.Int, n)
	Y := make([]*big.Int, n)
	R := make([]*big.Int, k)
	for i < n {
		pub, pri := para.GenerateKey()
		Pubs[i] = pub
		Pris[i] = pri
		i++
	}
	CE := para.GeneratePub(Pubs)
	C1 := para.Encrypt(m, r, CE)
	C2 := sharesecret.Distribute(para.P, r, n, k, Pubs)

	i = 0
	for i < n {
		Pris[i].Y = Pris[i].Decrypt(C1[0], C2[i].Y)
		X[i] = C2[i].X
		Y[i] = Pris[i].Y
		i++
	}
	//fmt.Println(sharesecret.Recover1(para.P, X, Y))
	rsum := big.NewInt(0)
	i = 0
	for i < k {
		R[i] = sharesecret.Recover(para.P, X[0:k], Pris[i].Y, int(i))
		rsum.Add(rsum, R[i])
		i++
	}
	rsum.Mod(rsum, para.P)
	//fmt.Println(rsum)
	tmp := big.NewInt(0).Exp(CE, rsum, para.P)
	tmp.ModInverse(tmp, para.P)
	mm := big.NewInt(0).Mul(C1[1], tmp)
	mm.Mod(mm, para.P)
	fmt.Println(mm, m)

}
*/
