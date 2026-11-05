Hello there! 

Make sure you've followed the [Contributing](https://github.com/chriskiehl/Gooey/blob/master/CONTRIBUTING.md) guidelines before finalizing your pull request. 

TL;DR: 

 - [ ] You're opening this PR against the current [release branch](https://github.com/chriskiehl/Gooey/blob/master/CONTRIBUTING.md#development-overview)
 - [ ] Works on Python 3.9+
 - [ ] Commits have been squashed and includes the relevant issue number
 - [ ] Pull request description contains link to relevant issue or detailed notes on changes
  - [ ] This **must** include example code demonstrating your feature or the bug being fixed
 - [ ] All existing tests pass 
 - [ ] Your bug fix / feature has associated test coverage 
 - [ ] A news item has been added to `news/` (see [Contributing](https://github.com/chriskiehl/Gooey/blob/master/CONTRIBUTING.md#adding-a-news-item))
  - Run `package add news -a "<your news item>"` ([scikit-package](https://scikit-package.github.io/scikit-package/)), or copy the template with `cp news/TEMPLATE.rst news/$(git rev-parse --abbrev-ref HEAD).rst` and fill it in
  - If no news is needed, run `package add news -n "<brief reason>"` or write `* No news added: <brief reason>` in your news file
 - [ ] README.md is updated (if relevant)
