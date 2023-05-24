package elgamal

import (
	"crypto/rand"
	"errors"
	"fmt"
	"math/big"
	mathrand "math/rand"
	"time"
)

var zero = big.NewInt(0)
var one = big.NewInt(1)
var two = big.NewInt(2)

type PubKey struct {
	P, G, E *big.Int
}

type PriKey struct {
	P, G, D, Y *big.Int
}

type Elgamalpara struct {
	P, Q, G *big.Int
}

type CType struct {
	G_r, C *big.Int
}

type CountC struct {
	C1, C2 *big.Int
}

//计算大素数p和生成元p
func Setup(primebit int) (Elgamalpara, error) {
	P, Q, G, err := Gen(primebit, 50)
	para := Elgamalpara{P, Q, G}
	if err != nil {
		fmt.Println(err)
	}
	return para, nil
}

//生成公私钥
func (para *Elgamalpara) GenerateKey() (PubKey, PriKey) {
	randSource := mathrand.New(mathrand.NewSource(time.Now().UnixNano()))
	// choose random integer d from {1...(q-1)}
	d := new(big.Int).Rand(randSource, new(big.Int).Sub(para.Q, one))
	// e = g^d mod p
	e := new(big.Int).Exp(para.G, d, para.P)
	pubkey := PubKey{para.P, para.G, e}
	prikey := PriKey{para.P, para.G, d, big.NewInt(0)}
	return pubkey, prikey
}

//生成合公钥PK
func (para *Elgamalpara) GeneratePub(pubs []PubKey) *big.Int {
	PK := big.NewInt(1)
	//fmt.Println(PK)
	for _, v := range pubs {
		if para.P == v.P && para.G == v.G {
			PK.Mul(PK, v.E)
			PK.Mod(PK, para.P)
		}
	}
	return PK
}

//用合公钥加密
func (para *Elgamalpara) Encrypt(m, r, PK *big.Int) CType {
	g_r := big.NewInt(0).Exp(para.G, r, para.P)
	PK_r := big.NewInt(0).Exp(PK, r, para.P)
	g_m := big.NewInt(0).Exp(para.G, m, para.P)
	c := big.NewInt(0).Mul(g_m, PK_r)
	c.Mod(c, para.P)
	var C CType
	C.G_r = g_r //g ^ r
	C.C = c     //PK ^ r
	return C
}

//Count, 计算所有选票乘积
func (para *Elgamalpara) Count(Csum []CType) CountC {
	C1, C2 := big.NewInt(1), big.NewInt(1)
	for i := 0; i < len(Csum); i++ {
		C1.Mul(C1, Csum[i].G_r)
		C2.Mul(C2, Csum[i].C)
	}
	C1.Mod(C1, para.P)
	C2.Mod(C2, para.P)
	return CountC{C1, C2}
}

//Voter_i从VC得到C1, 计算C1^x, x为Voter_i的私钥
func (pri PriKey) Decrypt0(C1 *big.Int) *big.Int {
	tmp := big.NewInt(0)
	tmp.Exp(C1, pri.D, pri.P)
	return tmp
}

//得到g^b
func (para *Elgamalpara) Decrypt1(up *big.Int, S []*big.Int) *big.Int {
	down := big.NewInt(1)
	for i := 0; i < len(S); i++ {
		down.Mul(down, S[i])
	}
	down.Mod(down, para.P)
	//fmt.Println(up, down)
	tmp := big.NewInt(0).ModInverse(down, para.P)
	tmp.Mul(up, tmp)
	tmp.Mod(tmp, para.P)
	return tmp
}

//暴力!!!
//没破解出来就返回0
func (para *Elgamalpara) Force(max int, g_b *big.Int) int {
	for i := -1 * max; i < max; i++ {
		tmp := big.NewInt(int64(i))
		tmp.Exp(para.G, tmp, para.P)
		if tmp.Cmp(g_b) == 0 {
			return i
		}
	}
	return max + 1
}

// Note : this section of code is taken from (https://github.com/ldinc/pqg).
// Author of this code is "Drogunov Igor".
// Gen emit <p,q,g>.
// p = 2q + 1, p,q - safe primes
// g - cyclic group generator Zp
// performs n Miller-Rabin tests with 1 - 1/(4^n) probability false rate.
// Gain n - bit width for integer & probability rang for MR.
// It returns p, q, g and write error message.
func Gen(n, probability int) (*big.Int, *big.Int, *big.Int, error) {
	for {
		q, err := rand.Prime(rand.Reader, n-1)
		if err != nil {
			return nil, nil, nil, err
		}
		t := new(big.Int).Mul(q, two)
		p := new(big.Int).Add(t, one)
		if p.ProbablyPrime(probability) {
			for {
				g, err := rand.Int(rand.Reader, p)
				if err != nil {
					return nil, nil, nil, err
				}
				b := new(big.Int).Exp(g, two, p)
				if b.Cmp(one) == 0 {
					continue
				}
				b = new(big.Int).Exp(g, q, p)
				if b.Cmp(one) == 0 {
					return p, q, g, nil
				}
			}
		}
	}
	return nil, nil, nil, errors.New("can't emit <p,q,g>")
}
