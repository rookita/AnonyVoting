package sharesecret

import (
	"elgamir/elgamal"
	"elgamir/sharesecret/polynom"
	"math/big"
)

//y == c * e ^ r && c == f(x)
type Share struct {
	X, Y *big.Int
}

func Distribute(prime, secret *big.Int, n, k int64, Pubs []elgamal.PubKey) (shares []Share) {
	shares, _ = distribute(prime, secret, n, k, Pubs)
	return shares
}

func distribute(prime, secret *big.Int, n, k int64, Pubs []elgamal.PubKey) ([]Share, *big.Int) {
	if n < k {
		panic("irrecoverable: not enough shares to reconstruct the secret.")
	}
	if k <= 0 {
		panic("number of shares must be positive.")
	}
	p := polynom.NewRandom(k, prime)

	// Set the first coefficient to the secret (the value at x=0) if the secret was given. And
	// anyway store the first coefficient in the secret variable.
	if secret != nil {
		if secret.Cmp(prime) > 0 {
			panic("secret value is too big (must be lower than 2^127 - 1)")
		}
		p.SetCoeff(0, secret)
	}
	secret = p.Coeff(0)
	// Create the shares which are the value of p at any point but x != 0. Choose x in [1..n].
	shares := make([]Share, 0, n)
	tmp := big.NewInt(0)
	for i := int64(1); i <= n; i++ {
		x := big.NewInt(i)
		c := p.ValueAt(x)
		//fmt.Println(c)
		tmp.Exp(Pubs[i-1].E, secret, prime) //e ^ r
		y := big.NewInt(0).Mul(c, tmp)
		y.Mod(y, prime)
		shares = append(shares, Share{X: x, Y: y})
	}

	return shares, secret
}

func Recover(prime *big.Int, x []*big.Int, y *big.Int, i int) *big.Int {
	return polynom.Interpolate1(prime, x, y, i)
}

// Recover the secret from shares. Notice that the number of shares that is used should be at least
// the recover amount (k) that was used in order to create them in the New function.
func Recover1(prime *big.Int, xs []*big.Int, ys []*big.Int) (secret *big.Int) {
	// Evaluate the polynom that goes through all (x[i], y[i]) points at x=0.
	return polynom.Interpolate(big.NewInt(0), xs, ys, prime)
}
