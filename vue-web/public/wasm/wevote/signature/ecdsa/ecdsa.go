package p256ecdsa

import (
	"crypto/ecdsa"
	"crypto/elliptic"
	"crypto/rand"
	"crypto/sha256"
	"math/big"
)

type SignType struct {
	R, S *big.Int
}

func GenerateKey() (ecdsa.PublicKey, *big.Int) {
	privateKey, _ := ecdsa.GenerateKey(elliptic.P256(), rand.Reader)
	return privateKey.PublicKey, privateKey.D
}

func Sign(msg string, privateKey *ecdsa.PrivateKey) SignType {
	hash := sha256.Sum256([]byte(msg))
	r, s, _ := ecdsa.Sign(rand.Reader, privateKey, hash[:])
	return SignType{r, s}
}

func Verify(pk ecdsa.PublicKey, r, s *big.Int, msg string) bool {
	tmp := sha256.Sum256([]byte(msg))
	hash := tmp[:]
	valid := ecdsa.Verify(&pk, hash, r, s)
	return valid
}

/*
func main() {
	privateKey, err := ecdsa.GenerateKey(elliptic.P256(), rand.Reader)
	if err != nil {
		panic(err)
	}

	msg := "hello, world"
	hash := sha256.Sum256([]byte(msg))

	sig, err := ecdsa.SignASN1(rand.Reader, privateKey, hash[:])
	if err != nil {
		panic(err)
	}
	fmt.Printf("signature: %x\n", sig)

	valid := ecdsa.VerifyASN1(&privateKey.PublicKey, hash[:], sig)
	fmt.Println("signature verified:", valid)
}
*/
