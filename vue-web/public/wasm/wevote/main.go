package main

import (
	"crypto/ecdsa"
	"crypto/elliptic"
	"encoding/hex"
	"fmt"
	"math/big"
	"syscall/js"
	"wevote/elgamal"
	p256ecdsa "wevote/signature/ecdsa"
)

func getpara(jspara js.Value) elgamal.Elgamalpara {
	P, Q, G := hextoInt(jspara.Get("P").String()), hextoInt(jspara.Get("Q").String()), hextoInt(jspara.Get("G").String())
	return elgamal.Elgamalpara{P, Q, G}
}

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
func setup(this js.Value, args []js.Value) interface{} {
	bits := 256
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
func generatekey(this js.Value, args []js.Value) interface{} {
	para := getpara(args[0])
	pk, sk := para.GenerateKey()
	ecdsa_pk, ecdsa_sk := p256ecdsa.GenerateKey()

	//fmt.Println(pk)
	return js.ValueOf(map[string]interface{}{
		"pk":         inttoHex1(pk.E),
		"sk":         inttoHex1(sk.D),
		"ecdsa_pk_x": inttoHex1(ecdsa_pk.X),
		"ecdsa_pk_y": inttoHex1(ecdsa_pk.Y),
		"ecdsa_sk":   inttoHex1(ecdsa_sk),
	})
}

//生成合公钥PK
//args[0]为para, args[1]为公钥集合, args[2]为参与者人数
//返回string
func generatepub(this js.Value, args []js.Value) interface{} {
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

//加密选票
//args[0]为para, args[1]为随机数r, args[2]为合公钥PK, args[3]为m, args[4]为m是否为负数(0表示为正数)
//返回object C{g_r, g^m * PK^r}
func encrypt(this js.Value, args []js.Value) interface{} {
	para := getpara(args[0])
	r, PK, mm := hextoInt(args[1].String()), hextoInt(args[2].String()), args[3].Int()
	m := big.NewInt(int64(mm))
	neg := args[4].Int()
	var C elgamal.CType
	if neg == 0 { //m为正数
		C = para.Encrypt(m, r, PK)
	} else {
		negm := big.NewInt(0).Mul(m, big.NewInt(-1))
		C = para.Encrypt(negm, r, PK)
	}
	return js.ValueOf(map[string]interface{}{
		"g_r": inttoHex1(C.G_r),
		"c":   inttoHex1(C.C),
	})
}

//对json格式选票签名
//args[0]为选票(string), args[1]为私钥(string), args[2]为公钥(object{x,y})
//返回签名(string)
func sign(this js.Value, args []js.Value) interface{} {
	m, sk, x, y := args[0].String(), hextoInt(args[1].String()), hextoInt(args[2].Get("x").String()), hextoInt(args[2].Get("y").String())
	pub := ecdsa.PublicKey{elliptic.P256(), x, y}
	priv := ecdsa.PrivateKey{pub, sk}
	sign := p256ecdsa.Sign(m, &priv)
	return js.ValueOf(map[string]interface{}{
		"r": inttoHex1(sign.R),
		"s": inttoHex1(sign.S),
	})
}

//验证选票是否正确
//args[0]为para, args[1]为选票集合, args[2]为签名集合, args[3]为签名公钥集合(object), args[4]为json格式选票, args[5]为大小
//返回object C{C1, C2}
func count(this js.Value, args []js.Value) interface{} {
	para := getpara(args[0])
	n := args[5].Int()
	msg, signs, pubs := make([]string, n), make([]p256ecdsa.SignType, n), make([]ecdsa.PublicKey, n)
	Csum := make([]elgamal.CType, n)
	for i := 0; i < n; i++ {
		signs[i] = p256ecdsa.SignType{hextoInt(args[2].Index(i).Get("r").String()), hextoInt(args[2].Index(i).Get("s").String())}
		msg[i] = args[4].Index(i).String()
		pubs[i] = ecdsa.PublicKey{elliptic.P256(), hextoInt(args[3].Index(i).Get("x").String()), hextoInt(args[3].Index(i).Get("y").String())}
	}
	valid := make([]bool, n)

	for i := 0; i < n; i++ {
		valid[i] = p256ecdsa.Verify(pubs[i], signs[i].R, signs[i].S, msg[i])
		if valid[i] {
			Csum[i] = elgamal.CType{hextoInt(args[1].Index(i).Get("g_r").String()), hextoInt(args[1].Index(i).Get("c").String())}
		} else {
			//Csum[i] = elgamal.CType{hextoInt(args[1].Index(i).Get("g_r").String()), hextoInt(args[1].Index(i).Get("c").String())}
			fmt.Println("the", i, "signature is not valid")
			Csum[i] = elgamal.CType{big.NewInt(1), big.NewInt(1)}
		}
	}
	var C elgamal.CountC
	C = para.Count(Csum)
	return js.ValueOf(map[string]interface{}{
		"C1": js.ValueOf(inttoHex1(C.C1)),
		"C2": js.ValueOf(inttoHex1(C.C2)),
	})
}

//计算C1 ^ x
//args[0]为para, args[1]为C1, args[2]为私钥x
//返回string
func decrypt0(this js.Value, args []js.Value) interface{} {
	para := getpara(args[0])
	var pri elgamal.PriKey
	pri.P = para.P
	pri.G = para.G
	pri.D = hextoInt(args[2].String())
	res := pri.Decrypt0(hextoInt(args[1].String()))
	return js.ValueOf(inttoHex1(res))
}

//解密g^b
//args[0]为para, args[1]为C2, args[2]为S(C^x)集合, args[3]为S集合大小n, args[4]为暴力破解上限
func decrypt1(this js.Value, args []js.Value) interface{} {
	para := getpara(args[0])
	C2, n, max := hextoInt(args[1].String()), args[3].Int(), args[4].Int()
	//fmt.Println(max)
	S := make([]*big.Int, n)
	for i := 0; i < n; i++ {
		S[i] = hextoInt(args[2].Index(i).String())
	}
	g_b := para.Decrypt1(C2, S)
	//fmt.Println(g_b)
	res := para.Force(max, g_b)
	return js.ValueOf(res)
}

func registerCallbacks() {
	js.Global().Set("setup", js.FuncOf(setup))
	js.Global().Set("generatekey", js.FuncOf(generatekey))
	js.Global().Set("generatepub", js.FuncOf(generatepub))
	js.Global().Set("encrypt", js.FuncOf(encrypt))
	js.Global().Set("count", js.FuncOf(count))
	js.Global().Set("decrypt0", js.FuncOf(decrypt0))
	js.Global().Set("decrypt1", js.FuncOf(decrypt1))
	js.Global().Set("sign", js.FuncOf(sign))
}

func main() {
	c := make(chan struct{}, 0)
	fmt.Println("WASM Go Initialized")
	// register functions
	registerCallbacks()
	<-c
}
