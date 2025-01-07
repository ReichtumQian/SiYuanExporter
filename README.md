
本程序将思源笔记中的内容导出为 Mdbook 以及 Mkdocs 格式，以便于发布。同时保持双链（仅支持对文件的双链）。

## Quick Start

- 从 `RELEASE` 下载最新的 `exe` 文件
- 配置 `config.json` 文件，其中 `base_url` 为思源笔记的网络伺服地址，`token` 为访问令牌。


## 配置 Mkdocs

为了确保 `Mkdocs` 和 `SiYuan` 的表达力一样，要求使用 `section-index` 插件，如下安装

``` bash
pip install mkdocs-section-index
```

然后在 `mkdocs.yml` 中启用：

``` yaml
plugins:
  - section-index
```

注意生成的 `nav.yml` 还是得手动插入 `mkdocs.yml` 中，或者用脚本插入。

