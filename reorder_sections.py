# -*- coding: utf-8 -*-
import re

HTML = "C:/Users/haols/WorkBuddy/2026-07-19-10-33-47/new-site/index.html"

with open(HTML, encoding="utf-8") as f:
    h = f.read()

# ---------- 1) 导航菜单：把 People 移到 Publications 之后 ----------
nav_people = '<a href="#people">People</a>'
nav_pub = '<a href="#publications">Publications</a>'
assert nav_people in h and nav_pub in h, "nav link not found"
h = h.replace(nav_people, "")                       # 先移除
h = h.replace(nav_pub + "\n", nav_pub + "\n        " + nav_people + "\n")  # 插到 publications 后

# ---------- 2) 正文：把 people section 移到 publications section 之后 ----------
m_people = re.search(r'<section class="section" id="people">.*?</section>', h, re.S)
assert m_people, "people section not found"
people_block = m_people.group(0)
h = h[:m_people.start()] + h[m_people.end():]        # 删除原 people

m_pub = re.search(r'<section class="section" id="publications">.*?</section>', h, re.S)
assert m_pub, "publications section not found"
insert_at = m_pub.end()
h = h[:insert_at] + "\n" + people_block + "\n" + h[insert_at:]

with open(HTML, "w", encoding="utf-8") as f:
    f.write(h)

# ---------- 校验 ----------
order = re.findall(r'<section class="section" id="([a-z]+)"', h)
nav_order = re.findall(r'href="#([a-z]+)">', h)
print("section 顺序:", order)
print("nav 顺序    :", nav_order)
assert order.index("people") == order.index("publications") + 1, "people 未在 publications 后!"
assert nav_order[nav_order.index("publications")+1] == "people", "nav 未同步!"
print("OK: people 已移到 publications 之后，导航已同步。")
