# jomiel

[![pypi-pyversions](https://img.shields.io/pypi/pyversions/jomiel?color=%230a66dc)][pypi]
[![pypi-v](https://img.shields.io/pypi/v/jomiel?color=%230a66dc)][pypi]
[![pypi-wheel](https://img.shields.io/pypi/wheel/jomiel?color=%230a66dc)][pypi]
[![pypi-status](https://img.shields.io/pypi/status/jomiel?color=%230a66dc)][pypi]
[![code-style](https://img.shields.io/badge/code%20style-black-000000.svg)][black]

[pypi]: https://pypi.org/project/jomiel
[black]: https://pypi.org/project/black

`jomiel` is the meta inquiry middleware for distributed systems. It
returns data about content on [video-sharing] websites (e.g. YouTube).
Two technologies form the basis for `jomiel`:

- [ZeroMQ] (also known as ØMQ, 0MQ, or zmq) looks like an embeddable
  networking library but acts like a concurrency framework

- [Protocol Buffers] is a language-neutral, platform-neutral,
  extensible mechanism for serializing structured data

`jomiel` is a spiritual successor to (now defunct) [libquvi].

[libquvi]: https://github.com/guendto/libquvi

![Example: jomiel and yomiel working together](./docs/demo.svg)

## Features

- **Language and platform neutral**. It communicates using [Protocol
  Buffers] and [ZeroMQ]. There are plenty of [examples]. Pick your
  favorite language.

- **Secure**. It can authenticate and encrypt connections using [CURVE]
  and [SSH].

- **Extensible**. It has a plugin architecture.

[protocol buffers]: https://developers.google.com/protocol-buffers/
[ssh]: https://en.wikipedia.org/wiki/Ssh
[zeromq]: https://zeromq.org/
[curve]: http://curvezmq.org/

## Getting started

[![pypi-pyversions](https://img.shields.io/pypi/pyversions/jomiel?color=%230a66dc)][pypi]

Install from [PyPI]:

[pypi]: https://pypi.org/

```shell
pip install jomiel
```

Run from the repository:

```shell
git clone https://github.com/guendto/jomiel.git
cd jomiel
pip install -e .
```

Try sending inquiries to `jomiel` with:

- [examples] - the demo client programs written in most modern languages
- [yomiel] - the pretty printer for `jomiel` messages

Be sure to check out the [HOWTO](./docs/HOWTO.md#howto-jomiel), also.

[examples]: https://github.com/guendto/jomiel-examples/
[yomiel]: https://github.com/guendto/jomiel-yomiel/

## Website coverage

```shell
jomiel --plugin-list  # The current coverage is very limited
```

See the `src/jomiel/plugin/` directory for the existing plugins. The
plugin architecture is extensible. When you are contributing new
plugins, make sure that the website is **not**:

- dedicated to copyright infringement (whether they host the media or
  only link to it)

- [NSFW]

[video-sharing]: https://en.wikipedia.org/wiki/Video_hosting_service
[python]: https://www.python.org/about/gettingstarted/
[nsfw]: https://en.wikipedia.org/wiki/NSFW

## License

`jomiel` is licensed under the [Apache License version 2.0][aplv2].

[aplv2]: https://www.tldrlegal.com/l/apache2

## Acknowledgements

- [pre-commit] is used for linting and reformatting, see the
  [.pre-commit-config.yaml] file

[.pre-commit-config.yaml]: https://github.com/guendto/jomiel/blob/master/.pre-commit-config.yaml
[pre-commit]: https://pre-commit.com/
