# The Mathematics of the Caesar Cipher

## Alphabet mapping

```
A=0  B=1  C=2  D=3  E=4  F=5  G=6  H=7  I=8  J=9  K=10 L=11 M=12
N=13 O=14 P=15 Q=16 R=17 S=18 T=19 U=20 V=21 W=22 X=23 Y=24 Z=25
```

## Encryption

```
C = (P + K) mod 26
```

Where `P` is the plaintext letter's value, `K` is the key (shift), and
`C` is the resulting ciphertext letter's value.

## Decryption

```
P = (C - K) mod 26
```

## Worked example

Plaintext: `HELLO`, Key: `3`

```
H = 7   (7 + 3) mod 26 = 10  -> K
E = 4   (4 + 3) mod 26 = 7   -> H
L = 11  (11 + 3) mod 26 = 14 -> O
L = 11  (11 + 3) mod 26 = 14 -> O
O = 14  (14 + 3) mod 26 = 17 -> R
```

Result: `KHOOR`

## Why modulo 26?

The alphabet has 26 letters. Modulo 26 arithmetic "wraps around" so a
shift that would go past `Z` (25) continues from `A` (0) again. This is
why `Z` shifted by 1 becomes `A`, and why key `26` behaves identically
to key `0`, and key `-1` behaves identically to key `25`.

## Key normalization

Any integer key is normalized into the 0-25 range before use:

```
normalize(26) = 0
normalize(27) = 1
normalize(-1) = 25
```

This means you can pass keys outside 0-25 and the tool will still do
the right thing.

## Security note

The Caesar cipher is a classical substitution cipher with only 26
possible keys, so it can be broken in a fraction of a second by brute
force (as this tool does). It is not suitable for protecting real,
sensitive information - it exists here purely for education, CTFs, and
authorized security research.
