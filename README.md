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

3. Run `python cv.py`, and it will replace `$$PAPERLIST$$` with the information from all your papers. Constants inside `cv.py` will determine which fields are displayed and how you want them displayed, e.g.

```
template_paper = '''<tr class="paper" data-tags="$$tags$$">
<td class="emoji"><div class="emoji">$$emoji$$</div></td>
<td class="paper">
  <p class="research">
    <strong><a href="$$link$$">$$title$$</a></strong>
    ($$author-web$$) <br /> 
    $$journal$$ <br />
    %%extras%%
  </p>
</td></tr>'''
```

4. Now you can modify your CV and web site in about 20 seconds. Just edit the YAML file and re-run `cv.py`.

# How to use this

1. Copy your existing web site into `index-template.html`. Replace the list of papers with the string `$$PAPERLIST$$`. Edit the `template_paper` string in `cv.py` so it looks like the code for your web site.

2. Same thing for your CV. Use the existing CV template `cv-template.tex` or paste in your own latex into `cv-template.tex`, with the same placeholder `$$PAPERLIST$$`. If you changed the template, edit the string list in `cv.py`.

3. Modify the other string lists in `cv.py` to match your circumstances, e.g. the categories, the journals you want italicized, etc.
