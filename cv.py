# TO DO
# - javascript hides headers with no content underneath them
#   - onClick: count divs under each header, hide zero, show non-zero
import yaml
import sys, os, pdb, re, datetime

# TEMPLATES

# section header and footer templates
section_header = '''<h1 class="entry-title">$$title$$</h1><br />
<table class="paper">'''
section_footer = '''</table>'''

section_header_cv = '''\\section{$$title$$}
 \\begin{enumerate}[leftmargin=0.15in]
'''
section_footer_cv = ''' \\end{enumerate}
 \\vspace{-16pt}
'''

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
template_paper_cv = '''\\item \\hangindent $$author-cv$$, ``$$title$$'', $$journal$$.'''

# paper template dictionary
template_list = {
    'published': template_paper,
    'review': template_paper,
    'progress': template_paper,
    'hold': template_paper,
    'retired': template_paper
}
template_list_cv = {
    'published': template_paper_cv,
    'review': template_paper_cv,
    'progress': template_paper_cv,
    'hold': template_paper_cv,
    'retired': template_paper_cv
}

# template for an extra bullet
extra_template = '    &rarr; $$content$$ <br />\n'

# mapping of paper types to titles
type_title_map = {
    'published': "Publications / In Press",
    'review': "Work in Progress",
    'progress': "Work in Progress",
    'hold': "On Hold or Retired",
    'retired': "On Hold or Retired"
    }
type_title_map_cv = {
    'published': "Publications / In Press",
    'review': "Work in Progress",
    'progress': "Work in Progress",
    'hold': "On Hold or Retired",
    'retired': "On Hold or Retired"
    }

# list of journals for auto-italicizing
journal_list = [
    'Science',
    'BMJ Open',
    'AEJ: Applied',
    'Economics and Politics Weekly',
    'India Policy Forum',
    'American Economic Review',
    'World Bank Economic Review',
    'Economic Journal',
    'Review of Economics and Statistics',
    'The Review of International Organizations']

#####################################################
# function to substitute a dictionary of $$string$$
def template_sub(template, sub_dict):

    # loop over each entry in the substitution dictionary
    for key in sub_dict:

        # perform the string replacement
        template = template.replace(f'$${key}$$', f'{sub_dict[key]}')

    return template

#############################################################
# function to add some extra bullets at the bottom of an entry
def template_sub_extras(content_str, extra_dict):

    # store entries in a long string
    line_list = ''
    
    # loop over each extra entry
    for key in extra_dict:

        # get the entry content into a template dictionary
        line_sub = {'content': extra_dict[key]}

        # sub the content into the entry template
        line = template_sub(extra_template, line_sub)

        # append it to the line list
        line_list = line_list + line

    # substitute the list of extras into the %%extras%% slot
    # if "Werker" in content_str: pdb.set_trace()
    return content_str.replace('%%extras%%', line_list)


def clean_template(c):

    # replace all unfilled template fields
    for s in ["\$\$[^$]+\$\$", "%%[^%]+%%"]:
        c = re.sub(s, "", c)

    # replace empty links
    c = re.sub('<a href="">([^<]+)</a>', r"\1", c)

    # replace double-newlines
    c = re.sub('<br />\s+</p>', '</p>', c)

    # put comma inside of double quotes
    c = c.replace("'',", ",''")
    
    return c

def italicize_journals(c, target):
    for journal in journal_list:
        if target == 'web':
            c = c.replace(journal, f'<i>{journal}</i>')
        elif target == 'cv':
            c = c.replace(journal, '\\textit{' + journal + '}')
    if target == 'cv':
        c = c.replace('Paul Novosad', '\\textbf{Paul Novosad}')
    return c

# function to create the paper content section
def create_paper_content(target):
        
    # create a dictionary of output sections
    content = {}

    # loop over the YAML information and fill in the content dictionary entries
    for key in yaml_data:

        entry = yaml_data[key]
    
        # get the entry type: this is the content key
        entry_type = entry['type']

        # choose template list based on target
        if target == 'web': tlist = template_list
        if target == 'cv': tlist = template_list_cv
        
        # select the correct template to use
        template = tlist[entry_type]

        # Write 'working paper' in CV if no journal
        if target == 'cv' and 'journal' not in entry:
            entry['journal'] = 'Working paper'
        
        # perform simple substitutions
        content_str = template_sub(template, entry)
    
        # perform complex substitions
        if 'extras' in entry:
            content_str = template_sub_extras(content_str, entry['extras'])
    
        # otherwise remove the placeholder from the template
        content_str = content_str.replace('%%extras%%', '')
        
        # add this type to the content dictionary if it's not there yet
        if entry_type not in content: content[entry_type] = []
    
        # clear out empty templates: journal, issue, and links
        content_str = clean_template(content_str)
    
        # italicize journals
        content_str = italicize_journals(content_str, target = target)
        
        # append this entry to the content list
        content[entry_type].append(content_str)

    return content

########
# MAIN #
########


########################################
# LOAD AND CLEAN CV / WEB SITE CONTENT #
########################################

# load content.yaml to a yaml structure
with open("cv-content.yaml", "r") as stream:
    try:
        yaml_data = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)

# get all content in a structured, formatted content dictionary
content_web = create_paper_content(target = 'web')
content_cv = create_paper_content(target = 'cv')

# for the CV, combine some content
content_cv['review'] = content_cv['review'] + content_cv['progress']
content_cv['retired'] = content_cv['hold'] + content_cv['retired']
del content_cv['progress']
del content_cv['hold']

# make same choices for the web
content_web['review'] = content_web['review'] + content_web['progress']
content_web['retired'] = content_web['hold'] + content_web['retired']
del content_web['progress']
del content_web['hold']

#####################################################
# BUILD CONTENT TEX AND HTML CONTENT FROM YAML INFO #
#####################################################

# store paper list in web format in a single long string
web_paper_str = ''
for type in content_web:

    # add the section header
    title_sub = {'title': type_title_map[type]}
    web_paper_str = web_paper_str + '\n' + template_sub(section_header, title_sub)

    # loop over the content list for this type
    for entry in content_web[type]:

        # add all non-empty entries
        if entry is not None:
            web_paper_str = web_paper_str + entry + '\n'
        
    # add the section footer
    web_paper_str = web_paper_str + section_footer + '\n'

# repeat the loop for the CV content
cv_paper_str = ''
for type in content_cv:

    # add the section header
    title_sub = {'title': type_title_map_cv[type]}
    cv_paper_str = cv_paper_str + '\n' + template_sub(section_header_cv, title_sub)

    # loop over the content list for this type
    for entry in content_cv[type]:

        # add all non-empty entries
        if entry is not None:
            cv_paper_str = cv_paper_str + entry + '\n'
        
    # add the section footer
    cv_paper_str = cv_paper_str + section_footer_cv + '\n'

#######################
# CREATE THE WEB PAGE #
#######################
    
# substitute content into web template
with open('index-template.html', 'rt') as f:
    web_str_list = f.readlines()

# write the output to index.html, filling in the content
with open('out/index.html', 'wt') as f:
    for line in web_str_list:

        # run core replacements and write to output file
        f.write(line.replace('$$PAPERLIST$$', web_paper_str))

###############################
############ MAKE CV ##########
###############################
# sys.exit()

# repeat substitution and copy for CV, with additional latex call
with open('cv-template.tex', 'rt') as f:
    cv_str_list = f.readlines()

# write the output to index.html, filling in the content
with open('out/cv.tex', 'wt') as f:
    for line in cv_str_list:

        # run core replacements
        l = line.replace('$$PAPERLIST$$', cv_paper_str)
        
        # run date replacement
        s = datetime.date.today().strftime("%B %d, %Y")
        l = l.replace('$$DATE$$', s)
        f.write(l)

# run pdflatex on the tex file
os.system('cd out; echo SSSS | pdflatex cv.tex >latex.log')
os.system('grep "Output written \\| Error" out/latex.log')


