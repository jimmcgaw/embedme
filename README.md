# Document Embedding and Chunking

For a vector database, to support RAG architectures, to be used in a Q&A about the text.

This is all for experimentating, with different levels of chunking and vector embeddings for retrieving matches, to get better levels of recall.

## The Corpus

The corpus for experimentation is the text of the Bible, sourced from [https://github.com/kenyonbowers/BibleJSON](https://github.com/kenyonbowers/BibleJSON).

The translation is the Pure Cambridge Edition (PCE), wherever that comes from. ([A supposed explanation](https://www.purecambridgetext.com/post/what-is-meant-by-the-pure-cambridge-text).)

I've cleaned up the text of HTML and oddball unicode code points, and created my own JSON in `bible/bible.json`.

I can't really call myself religious with a straight face, but it's a book I know fairly well.

## Odds 'n' Ends

I just learned that the makers of `uv` created a fast Rust-based typechecker called `ty`, and a linter / formatter called `ruff`. They are fabulous.

Included as uv dev dependencies; commands are in the `Makefile`.