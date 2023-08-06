# UDFT: Unitary Discrete Fourier Transform (and related)

This module implements unitary discrete Fourier transform, that is orthonormal.
This module existed before the introduction of the `norm="ortho"` keyword and is
now a very thin wrapper around Numpy or pyFFTW (maybe others in the future),
mainly done for my personal usage. There is also functions related to Fourier
and convolution like `ir2fr`.

It is useful for convolution [1]: they respect the Perceval equality, e.g., the
value of the null frequency is equal to `1/√N * ∑ₙ xₙ`.

```
[1] B. R. Hunt "A matrix theory proof of the discrete convolution theorem", IEEE
Trans. on Audio and Electroacoustics, vol. au-19, no. 4, pp. 285-288, dec. 1971
```

If you are having issues, please let me know

francois.orieux AT l2s.centralesupelec.fr

## Installation and documentation

UDFT is just the file `udft.py` and depends on `numpy` and Python 3.7 only. We
recommend using poetry for installation

```
   poetry add udft
```

but the package is available with pip also. For a quick and dirty installation,
just copy the `udft.py` file: it is quite stable, follow the [Semantic
Versioning](https://semver.org/spec/v2.0.0.html), and major changes are
unlikely.

## License

The code is in the public domain.
