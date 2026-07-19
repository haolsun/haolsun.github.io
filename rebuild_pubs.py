# -*- coding: utf-8 -*-
import re

HTML = "C:/Users/haols/WorkBuddy/2026-07-19-10-33-47/new-site/index.html"
IMG = "assets/img/pubs/RMF.png"

# (badge_single_line, title, authors_html, venue, [(link_text, url), ...])
groups = [
    ("Generative Models", [
        ("ICML 2026", "Riemannian MeanFlow for One-Step Generation on Manifolds",
         "Zichen Zhong, <span class=\"me\">Haoliang Sun</span>*, Yukun Zhao, Yongshun Gong, Yilong Yin",
         "International Conference on Machine Learning (ICML), 2026.",
         [("arXiv", "https://arxiv.org/abs/2603.10718"), ("Code", "https://github.com/haolsun/Riemannian_MeanFlow")]),
        ("ICCV 2019", "DUAL-GLOW: Conditional Flow-Based Generative Model for Modality Transfer",
         "<span class=\"me\">Haoliang Sun</span>*, Ronak Mehta, Hao H. Zhou, Zhichun Huang, Sterling C. Johnson, Vivek Prabhakaran, Vikas Singh",
         "IEEE International Conference on Computer Vision (ICCV), 2019.",
         [("arXiv", "https://arxiv.org/abs/1908.08074"), ("Code", "https://github.com/haolsun/dual-glow")]),
    ]),
    ("Robust Learning with Noisy Labels", [
        ("IJCV 2025", "Variational Rectification Inference for Learning with Noisy Labels",
         "<span class=\"me\">Haoliang Sun</span>#*, Qi Wei#, Lei Feng, Yupeng Hu, Fan Liu, Hehe Fan, Yilong Yin",
         "International Journal of Computer Vision (IJCV), 2025.",
         [("PDF", "https://qiwei98cn.top/2023/VRI.pdf"), ("Code", "https://github.com/haolsun/VRI")]),
        ("SCI 2024", "面向标签噪声学习的联合训练框架 (Joint Training Framework for Label Noise Learning)",
         "Qi Wei, <span class=\"me\">Haoliang Sun</span>*, Yuling Ma, Yilong Yin",
         "Scientia Sinica Informationis (中国科学:信息科学), 2024.",
         [("PDF", "https://www.sciengine.com/SSI/doi/10.1360/SSI-2022-0395")]),
        ("CVPR 2023", "Fine-Grained Classification with Noisy Labels",
         "Qi Wei, Lei Feng, <span class=\"me\">Haoliang Sun</span>*, Ren Wang, Chenhui Guo, Yilong Yin",
         "IEEE Conference on Computer Vision and Pattern Recognition (CVPR), 2023.",
         [("arXiv", "https://arxiv.org/abs/2303.02404")]),
        ("ECCV 2022", "Self-Filtering: A Noise-Aware Sample Selection for Label Noise with Confidence Penalization",
         "Qi Wei, <span class=\"me\">Haoliang Sun</span>*, Xiankai Lu, Yilong Yin",
         "European Conference on Computer Vision (ECCV), 2022.",
         [("arXiv", "https://arxiv.org/abs/2208.11351")]),
        ("PR 2021", "Learning to Rectify for Robust Learning with Noisy Labels",
         "<span class=\"me\">Haoliang Sun</span>#*, Chenhui Guo#, Qi Wei, Zhongyi Han, Yilong Yin",
         "Pattern Recognition (PR), 2021.",
         [("arXiv", "https://arxiv.org/abs/2111.04239"), ("Code", "https://github.com/haolsun/WarPI")]),
    ]),
    ("Learning in a Dynamic Environment", [
        ("CVPR 2025", "SeqMvRL: A Sequential Fusion Framework for Multi-view Representation Learning",
         "Ren Wang, <span class=\"me\">Haoliang Sun</span>*, Yuxiu Lin, Chuanhui Zuo, Yongshun Gong, Yilong Yin, Wenjia Meng",
         "IEEE Conference on Computer Vision and Pattern Recognition (CVPR), 2025.",
         [("PDF", "https://openaccess.thecvf.com/content/CVPR2025/papers/Wang_SeqMvRL_A_Sequential_Fusion_Framework_for_Multi-view_Representation_Learning_CVPR_2025_paper.pdf")]),
        ("ML 2024", "Learning Sample-Aware Threshold for Semi-Supervised Learning",
         "Qi Wei, Lei Feng, <span class=\"me\">Haoliang Sun</span>*, Ren Wang, Rundong He, Yilong Yin",
         "Machine Learning, 2024 (ACML 2023 Journal Track).",
         [("PDF", "https://link.springer.com/article/10.1007/s10994-023-06425-7")]),
        ("PR 2023", "Attentional Prototype Inference for Few-Shot Segmentation",
         "<span class=\"me\">Haoliang Sun</span>*, Xiankai Lu, Haochen Wang, Yilong Yin, Xiantong Zhen, Cees G. M. Snoek, Ling Shao",
         "Pattern Recognition (PR), 2023.",
         [("arXiv", "https://arxiv.org/abs/2105.06668"), ("Code", "https://github.com/haolsun/API")]),
        ("CVPR 2023", "MetaViewer: Towards A Unified Multi-View Representation",
         "Ren Wang, <span class=\"me\">Haoliang Sun</span>*, Yuling Ma, Xiaoming Xi, Yilong Yin",
         "IEEE Conference on Computer Vision and Pattern Recognition (CVPR), 2023.",
         [("arXiv", "https://arxiv.org/abs/2303.06329")]),
        ("KBS 2022", "SNIP-FSL: Finding Task-Specific Lottery Jackpots for Few-Shot Learning",
         "Ren Wang, <span class=\"me\">Haoliang Sun</span>*, Xiushan Nie, Yilong Yin",
         "Knowledge-Based Systems (KBS), 2022.",
         [("PDF", "https://www.sciencedirect.com/science/article/abs/pii/S0950705122001733")]),
        ("ICML 2020", "Learning to Learn Kernels with Variational Random Features",
         "Xiantong Zhen#, <span class=\"me\">Haoliang Sun</span>#, Yingjun Du#, Jun Xu, Yilong Yin, Ling Shao, Cees Snoek",
         "International Conference on Machine Learning (ICML), 2020.",
         [("arXiv", "https://arxiv.org/abs/2006.06707"), ("Code", "https://github.com/haolsun/MetaVRF")]),
    ]),
    ("Kernel Methods", [
        ("ICIP 2019", "Learning the Set Graphs: Image-Set Classification Using Sparse Graph Convolutional Networks",
         "<span class=\"me\">Haoliang Sun</span>*, Xiantong Zhen, Yilong Yin",
         "IEEE International Conference on Image Processing (ICIP), 2019.",
         [("arXiv", "https://arxiv.org/abs/2208.11351")]),
        ("CVPR 2017", "Learning Deep Match Kernels for Image-Set Classification",
         "<span class=\"me\">Haoliang Sun</span>*, Xiantong Zhen, Yuanjie Zheng, Gongping Yang, Yilong Yin, Shuo Li",
         "IEEE Conference on Computer Vision and Pattern Recognition (CVPR), 2017.",
         [("PDF", "https://web.archive.org/web/20181123142235id_/http://openaccess.thecvf.com:80/content_cvpr_2017/papers/Sun_Learning_Deep_Match_CVPR_2017_paper.pdf")]),
        ("IPMI 2017", "Directly Estimating Spinal Cobb Angles by Structured Multi-Output Regression",
         "<span class=\"me\">Haoliang Sun</span>*, Xiantong Zhen, Chris Bailey, Parham Rasoulinejad, Yilong Yin, Shuo Li",
         "Information Processing in Medical Imaging (IPMI), Oral Paper, 2017.",
         [("arXiv", "https://arxiv.org/abs/2012.12626")]),
    ]),
]

def card(badge, title, authors, venue, links):
    L = []
    L.append('        <div class="paper-box">')
    L.append('          <div class="paper-box-media">')
    L.append('            <div class="badge">%s</div>' % badge)
    L.append('            <div class="paper-box-image"><img src="%s" alt="" loading="lazy"></div>' % IMG)
    L.append('          </div>')
    L.append('          <div class="pub-body">')
    L.append('            <div class="pub-title">%s</div>' % title)
    L.append('            <div class="pub-authors">%s</div>' % authors)
    L.append('            <div class="pub-venue">%s</div>' % venue)
    L.append('            <div class="pub-links">')
    for t, u in links:
        L.append('              <a href="%s" target="_blank" rel="noopener">%s</a>' % (u, t))
    L.append('            </div>')
    L.append('          </div>')
    L.append('        </div>')
    return "\n".join(L)

out = []
for gname, papers in groups:
    out.append('        <h3 class="group">%s</h3>' % gname)
    for p in papers:
        out.append(card(*p))
body = "\n".join(out)

with open(HTML, encoding="utf-8") as f:
    h = f.read()

# Replace everything from the first group header up to (not including) the
# publications </section>, with the freshly-generated uniform body.
pat = re.compile(r'(<h3 class="group">Generative Models</h3>).*?\n      </section>', re.S)
new_h, n = pat.subn(lambda m: body + "\n      </section>", h, count=1)
assert n == 1, "replacements: %d" % n

with open(HTML, "w", encoding="utf-8") as f:
    f.write(new_h)

print("OK: regenerated publications with RMF.png for all", sum(len(p) for _, p in groups), "papers")
