My personal page repo hosted [here](https://bastiencarreres.com)

## Running locally

Environment (Ruby, Node, Python) is managed with [pixi](https://pixi.sh).

```bash
curl -fsSL https://pixi.sh/install.sh | bash  # if not already installed
pixi run install   # bundle install + npm install + vendor reveal.js (once, or after Gemfile/package.json changes)
pixi run serve      # http://localhost:4000
pixi run build      # build into _site/
pixi run test       # run bin/tests Python test suite
```

## Aknowledgment

Based on **al-folio** theme available on this [repo](https://github.com/alshedivat/al-folio)

## License

The theme is available as open source under the terms of the [MIT License](https://github.com/alshedivat/al-folio/blob/master/LICENSE).
