with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Replace in initial markup
text = text.replace(
    'id="broadcastTitleText">Week 5 Official Audio Recap (Pat McAfee Edition)</span>',
    'id="broadcastTitleText">Week 6 Official Audio Recap (Pat McAfee Edition)</span>'
)
text = text.replace(
    "Alex's 167.94 record, Franky's 3.96 heartbreak, Robert's Pick-Em lead, and Pedro's 5K panic.",
    "Franky's 149.80 shootout win, Pedro's $10 DEF bounty, Herrador's 50-pt blowout, and Robert's 5K panic."
)

# Replace in switchVoice
old_mcafee_title = "if (title) title.innerText = 'Week 5 Official Audio Recap (Pat McAfee Edition)';"
new_mcafee_title = "if (title) title.innerText = 'Week 6 Official Audio Recap (Pat McAfee Edition)';"
text = text.replace(old_mcafee_title, new_mcafee_title)

old_freeman_title = "if (title) title.innerText = 'Week 5 Official Audio Recap (Morgan Freeman Edition)';"
new_freeman_title = "if (title) title.innerText = 'Week 6 Official Audio Recap (Morgan Freeman Edition)';"
text = text.replace(old_freeman_title, new_freeman_title)

old_freeman_desc = "if (desc) desc.innerText = 'Smooth dramatic recap: Alex\\'s 167.94 record, Franky\\'s 3.96 heartbreak, Robert\\'s Pick-Em lead, and Pedro\\'s toilet watch.';"
new_freeman_desc = "if (desc) desc.innerText = 'Smooth dramatic recap: Franky\\'s 149.80 triumph, Pedro\\'s resurrection, Herrador\\'s clinic, and Robert\\'s toilet slide.';"
text = text.replace(old_freeman_desc, new_freeman_desc)

old_mcafee_desc = "if (desc) desc.innerText = 'High-energy recap: Alex\\'s 167.94 record, Franky\\'s 3.96 heartbreak, Robert\\'s Pick-Em lead, and Pedro\\'s 5K panic.';"
new_mcafee_desc = "if (desc) desc.innerText = 'High-energy recap: Franky\\'s 149.80 shootout win, Pedro\\'s $10 DEF bounty, Herrador\\'s 50-pt blowout, and Robert\\'s 5K panic.';"
text = text.replace(old_mcafee_desc, new_mcafee_desc)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(text)

print('Updated audio titles and descriptions in index.html!')
