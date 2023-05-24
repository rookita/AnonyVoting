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

//生成合公钥E
func (para *Elgamalpara) GeneratePub(pubs []PubKey) *big.Int {
	E := one
	for _, v := range pubs {
		if para.P == v.P && para.G == v.G {
			E.Mul(E, v.E)
			E.Mod(E, para.P)
		}
	}
	return E
}

//用合公钥加密
func (para *Elgamalpara) Encrypt(m, r, E *big.Int) [2]*big.Int {
	c1 := big.NewInt(0).Exp(para.G, r, para.P)
	tmp := big.NewInt(0).Exp(E, r, para.P)
	c2 := big.NewInt(0).Mul(m, tmp)
	c2.Mod(c2, para.P)
	var C [2]*big.Int
	C[0] = c1
	C[1] = c2
	return C
}

//用私钥解密
func (pri PriKey) Decrypt(g_r *big.Int, c *big.Int) *big.Int {
	y := big.NewInt(0)
	y.Exp(g_r, pri.D, pri.P)
	y.ModInverse(y, pri.P)
	y.Mul(y, c)
	y.Mod(y, pri.P)
	return y
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
