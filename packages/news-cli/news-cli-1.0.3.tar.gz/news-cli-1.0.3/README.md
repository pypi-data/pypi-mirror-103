## The Local News

Get the local news on your cli about the any topic

### Install
====================

```bash
pip install news-cli

Usage: news [OPTIONS]
  Read news on your command line.

Options:
  --area    TEXT  headlines for areas  [default: USA ; options: [india|israel|france|usa|us|uk|england|technology|
            business|science|health|general|sports]
  --keyword TEXT  Specific news for the keyword
  --help          Show this message and exit.

```

![](resources/news-cli_v2.gif)


### Run
====================

```javascript

news # displays top news from US
news --area technology # display tech news
news --keyword coronavirus # show news about coronavirus keyword
```