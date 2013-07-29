## A noisy way to keep tabs on your kickstarter project

kickding.py is a very simple script to scrape a kickstarter project's page and play a sound for every new backer at choice levels. There's very little magic here, and it would be even less impressive if Kickstarter had an API. Until they do, at least scraping the site is pretty straightforward.

Usage: change `site` to point to the project you want to track. You can either change `pingsound` or just drop in a sound to play at `./ping.wav` (1 second or shorter works best), and if `aplay ./ping.wav` won't play the song on your system, you'll have to find a command that will.

This was inspired by the last entry in jwz's [nscp dorm](http://www.jwz.org/gruntle/nscpdorm.html) diaries.
