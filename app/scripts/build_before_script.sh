#!/bin/bash
mkdir -p /kaniko/.docker
echo "{\"auths\":{\"${CI_REGISTRY}\":{\"auth\":\"$(printf "%s:%s" "${CI_REGISTRY_USER}" "${CI_REGISTRY_PASSWORD}" | base64 | tr -d '\n')\"}}}" > /kaniko/.docker/config.json
| echo "-----BEGIN CERTIFICATE-----
    MIIFQTCCAymgAwIBAgIDdBlgMA0GCSqGSIb3DQEBCwUAMEExCzAJBgNVBAYTAkZS \
    MRcwFQYDVQQKDA5JTVQtQXRsYW50aXF1ZTEZMBcGA1UEAwwQUm9vdCBUZWFjaGlu \
    ZyBDQTAeFw0xNzEwMTUyMjI4MjFaFw0yNzEwMTMyMjI4MjFaMEExCzAJBgNVBAYT \
    AkZSMRcwFQYDVQQKDA5JTVQtQXRsYW50aXF1ZTEZMBcGA1UEAwwQUm9vdCBUZWFj \
    aGluZyBDQTCCAiIwDQYJKoZIhvcNAQEBBQADggIPADCCAgoCggIBAMA53qjbSmUZ \
    8bZTH54k4LRSA18BjdI5PMaNaGbBO3dAgEZ26eOuR9pioRtcHjQKoLe/ldPiqunF \
    GrZnwMlh68Wod1BVBsmcW1vw6WD+KK9d2wBfcOCGFO4cKJFIYoxGzMEIOBR8drLO \
    xXhzhTPESPkWDqmTLaMX6ycSfD3qBGY9PlWOHtArKbLSgR2+qWb1LrsiBOqZ0uUy \
    aRW1SnfQUlSbPlduP6xBWS/CWnd91r/VUMjKxItopwKT79EOgl+4fpe8WTo3EkRN \
    flYrEWUFE/FgEq4u5WxGQdp4brvco1ya7PgUjr0ZgMImB0u1uMklcHG1pr0k53/X \
    zO36eHAkgCRwJ9bm8jWto6G6ZNzwjJni00+hzrlNiy9Wz9d84UpY07Y3n7H+pQEf \
    ZyLCyklsoj53khu6Rg47w1IYNorUXzkJxu0esnLp8pXNWd4SmEAYyAKZ/CJgsvPk \
    idZS/mDl+qj+m47xQezjxCoJS+eR2l7Iq2Cs8JdEGXqbJCtfOdvWrfPDBimYwjby \
    pmq/GXFzwjkjyJVJYp/VLv1P1jqssZ2V6B53zb3QbgvI9VTcNuIWQAVIfA++tQLI \
    3ZX6FKrqLYTvLVzLqKPAg4uFzqvU6XloIOdobGNeosDZ3V+FJoIre9sCbCRtffXp \
    LwQWmw/D4uJ2P6Ewe0LUViaGkgSkn2XzAgMBAAGjQjBAMA8GA1UdEwEB/wQFMAMB \
    Af8wDgYDVR0PAQH/BAQDAgEGMB0GA1UdDgQWBBSLPF9tp3Z/h3gR3HnKCbUC0adh \
    KTANBgkqhkiG9w0BAQsFAAOCAgEAb4cqFn8BbKbpYnzpcpxdDe/RLeiyC1q9MCsL \
    LG198oJBZi1WufPsYuTCqW2T3SAt5WYoLjLy2V76Gvg4OSyNmP/OzrasqYmnkDr2 \
    kI/LHJ1RewMNb/vjeWmg6vmtecQGdPuaq6fUTpfIzx3b+TM76XqktSO5GF11lNJh \
    8/gkjPKGW2rJ5T41ue1uqYHEwZbuEW0m9Q7eV/PQahEt34VH9B9RI3kzeqnpbSzg \
    FfuiUdv4fxLkN88cPTfoOWPOPaXoqdAz2wCc9yHT6ypMYjxYUL9gJaQy08OoIcO2 \
    RR3vQrNqqFArIa18oUtt1REF0KS7w/SAxGKrhwuCcfRg9Z3mSx4gwnrKd6QTN0P+ \
    Xk+KTQht/y11ZBLpxcfE0S5fZ1Q6bRx9xUAgqHOEsQiwm4c6pUsXG9V3QnBMt5Ja \
    GqJnHEvEtM4lHPFkfrwXcUeB/gaMvxSRjkMmIBXst8uJL0U+QKj4sSfm1OMJYlmG \
    ag+MOlme4p8TBY+LzqEIbgInlUdYXHw4/uCBMtNQ9ZeRemZJBjkHkpQVgU0DCLlH \
    XxVvZn54tM8Lqw1PYqBKvtpmpAxj3F4NToy6u5NjL1rKXLFmDJdlwv/m0f4Gm7AQ \
    N4QyqV8jvzn5R3xSBvLMjoGjlfBClVVoNRJt8LqYzeLwSkfrrknFYBAo+lX+Vqn6 \
    0SnGgM4= \
    -----END CERTIFICATE-----" >> /kaniko/ssl/certs/additional-ca-cert-bundle.crt
