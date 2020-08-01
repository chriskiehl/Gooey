
## How to Contribute 

All contributions are welcome! This guide will get you up to speed with the contribution process for Gooey. 

Some Caveats Up Front: 

* Opening a PR does not guarantee it will be merged 
* Feedback may take time
* Merges may take time 

**--> The current release branch is [1.0.5](https://github.com/chriskiehl/Gooey/tree/1.0.5-release) <--**. All PRs should be opened against this branch. 


### Getting Started: 

All bugs and non-trivial changes must have an associated [issue](https://github.com/chriskiehl/Gooey/issues/new). So, step one should be making sure that your [issue doesn't already exist](https://github.com/chriskiehl/Gooey/issues?utf8=%E2%9C%93&q=is%3Aissue). If you find a relevant issue, feel free to add a comment with any additional details or problems specific to your use case. Otherwise, open a new issue and fill out the template in its entirety. 

An exception to this rule is for any "trivial" change such as language additions, documentation fixes, typo corrections, etc.. no issue is required for these. Just include a good description / overview in your PR. 

  
### Development Overview

All development and pull requests should be made against the **current release branch**. Master is reserved for the last stable working version of the code. As such, it will often be outdated.

Release branches take the form of `{semvar}-release`. For example:

* `1.0.2-release`  
* `2.0.0-release` 

You can find the current release branch by checking out the [branches page](https://github.com/chriskiehl/Gooey/branches). 



**Making Changes:**

* Create a branch for your changes
	* Use the current release branch
	* Don't branch from `master`! This will cause you pain! 
	* Ideal branch naming would reference the issue number it is resolving (e.g. `issue-xxx-enabling-cool-feature` ). 
* Group your commits into coarse feature-level chunks (preferably one) and reference the issue number in the message (e.g. `"closes #322 - added cool feature XXX"`)
	* Make your commits about One Thing. 
	* Avoid stream of consciousness style commits as they'll just be asked to be cleaned up during code review
* Make sure you've added tests for your feature / bug fix
* Make sure it works on both Python 2.7 and Python 3.x (this is often overlooked!) 
* Backwards compatibility must be honored 

**When to PEP8:**

The vast majority of Gooey's code does _not_ follow PEP8. This is because the vast majority of Gooey's code is build on top of WxPython code, which does not follow PEP8. Everything in Gooey's core honors the general camelCase style used throughout Wx. 

The exception to this rule is for everything in the `python_bindings/` package. This package holds the public API for Gooey, and thus honors PEP8. So the general rule is that if you're making a change to the public bindings: use PEP8. For all other internal Gooey code, honor the house style you find. 



## Pull Request Process

Pull Requests should be made against the **current release branch**. You can find the current release branch [here](https://github.com/chriskiehl/Gooey/branches).

A good PR should hit these essentials.

Basic Checklist: 
 - [ ] Works on both Python 2.7 & Python 3.x 
 - [ ] Commit message includes the relevant issue number
 - [ ] Pull request description contains link to relevant issue
 - [ ] Bug fix / feature has associated tests
 - [ ] README.md is updated (if relevant)
 - [ ] PR has summary of the change and links to the detailed issue.  

Super Cool Person Above and Beyond Checklist Additions:
 - [ ] A sister commit in the [Examples Repo](https://github.com/chriskiehl/GooeyExamples) was created demonstrating your new feature 










## Code of Conduct

None. Use your best judgement. 



## Grumpy Stuff:

* Please do not email me directly to ask why your PR hasn't been merged 
* Please do not email me directly to ask why your issue hasn't been addressed. 

The answer will always be some stock variant of (1) I'm just _a_ guy, (2) I work on this for free (3) It's not a priority at the moment, (4) yes, I feel guilty all the time, (5) some weekends I just want to play a video game or something. 

[Worth a read.](https://gist.github.com/richhickey/1563cddea1002958f96e7ba9519972d9)



