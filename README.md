# auto-cv-web

This auto-fills a CV and a web site with your publication information, which is stored in a text database. It makes it easier to update your CV and web site and keeps them synced.

I use this to auto-update [my web site](http://paulnovosad.com), and [my CV](https://paulnovosad.com/pdf/paul-novosad-cv.pdf). 

## How it works

1. Your publication information is stored in a `.yaml` file with entries that look like this:

```
paper11:
  type: review
  title: "Intergenerational Mobility in India: New Methods and Estimates Across Time, Space, and Communities"
  author-web: with Sam Asher and Charlie Rafkin
  author-cv: Sam Asher, Paul Novosad, and Charlie Rafkin
  emoji: ☝
  link: "http://paulnovosad.com/pdf/anr-india-mobility.pdf"
  journal: 'Revision requested at AEJ: Applied'
  tags: india,access,cities
  extras:
    note1: '<a href="http://paulnovosad.com/pdf/anr-mobility-online-appendix.pdf">Online Methods Appendix</a>'
    note2: '<a href="http://paulnovosad.com/pdf/anr-mobility-fact-sheet.pdf">Fact Sheet</a> for media.'
    note3: '<a href="http://paulnovosad.com/mobility-india.html">All-India mobility map.</a>'
    note4: '<a href="http://paulnovosad.com/mobility-delhi.html">Interactive Delhi mobility map.</a>'
    note5: 'Code for generating bottom half mobility (mu-0-50), all-India town, subdistrict, and district-level local mobility estimates:
  ```

   Note that you can have entries that are only useful for either the web or the .tex CV.


2. You then build your web page and CV, leaving a placeholder for the list of publications, which is just a string:

```
$$$PAPERLIST$$$
```

3. Run `python cv.py`, and it will replace `$$PAPERLIST$$` with the information from all your papers.

4. When you want to add / modify a paper entry, just edit the YAML and re-run `cv.py`.

