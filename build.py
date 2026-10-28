#!/usr/bin/env python3
"""Static site generator for the Nexivo site. Run:  python build.py"""
import os, re, html

import time
VER = str(int(time.time()))
ROOT = os.path.dirname(os.path.abspath(__file__))
IMGDIR = os.path.join(ROOT, "assets", "img")
FILES = os.listdir(IMGDIR)


def img(prefix):
    for f in FILES:
        if f.startswith(prefix):
            return "assets/img/" + f
    raise KeyError(prefix)


def i(prefix, alt="", cls="", extra=""):
    return f'<img src="{{R}}{img(prefix)}" alt="{alt}" {("class=%s" % chr(34) + cls + chr(34)) if cls else ""} loading="lazy" decoding="async" {extra}>'


# ---------- icons ----------
CHEV = '<svg viewBox="2 2 12 12" fill="none" stroke="currentColor" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round"><path d="M3.2 3.2L7.8 8l-4.6 4.8M8.2 3.2L12.8 8l-4.6 4.8"/></svg>'
CHECK = '<svg viewBox="0 0 16 16"><path d="M3 8.5l3.2 3.2L13 4.8"/></svg>'
STAR = '<svg viewBox="0 0 24 24"><path d="M12 2l2.9 6.6 7.1.6-5.4 4.7 1.6 7-6.2-3.7-6.2 3.7 1.6-7L2 9.2l7.1-.6z"/></svg>'
ARL = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M19 12H5M11 6l-6 6 6 6"/></svg>'
ARR = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'
IC = {
    "user": '<svg viewBox="0 0 24 24"><circle cx="12" cy="8" r="4"/><path d="M4 21c0-4.4 3.6-7 8-7s8 2.6 8 7"/></svg>',
    "book": '<svg viewBox="0 0 24 24"><path d="M12 6c-2-1.5-5-2-9-2v14c4 0 7 .5 9 2 2-1.5 5-2 9-2V4c-4 0-7 .5-9 2zM12 6v14M6 8h3M6 11h3M15 8h3M15 11h3"/></svg>',
    "cap": '<svg viewBox="0 0 24 24"><path d="M2 9l10-5 10 5-10 5zM6 11.5V16c0 1.5 3 3 6 3s6-1.5 6-3v-4.5M22 9v6"/></svg>',
    "bolt": '<svg viewBox="0 0 24 24"><path d="M13 2L4 14h7l-1 8 9-12h-7z"/></svg>',
    "chat": '<svg viewBox="0 0 24 24"><path d="M21 12a8 8 0 01-11.6 7.1L3 21l1.9-6.4A8 8 0 1121 12z"/></svg>',
    "chart": '<svg viewBox="0 0 24 24"><path d="M4 20V10M10 20V4M16 20v-7M22 20H2"/></svg>',
    "path": '<svg viewBox="0 0 24 24"><circle cx="6" cy="18" r="2.5"/><circle cx="18" cy="6" r="2.5"/><path d="M8.5 18H15a3 3 0 000-6H9a3 3 0 010-6h6.5"/></svg>',
    "note": '<svg viewBox="0 0 24 24"><path d="M5 3h10l4 4v14H5zM15 3v4h4M8 12h8M8 16h5"/></svg>',
    "fire": '<svg viewBox="0 0 24 24"><path d="M12 22c4 0 7-2.6 7-6.5 0-3-2-5-3.5-6.5-.3 2-1.5 3-2.5 3 0-3-1.5-6-4-8 0 4-4 6-4 11 0 4 3 7 7 7z"/></svg>',
    "clock": '<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg>',
    "target": '<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1"/></svg>',
    "bell": '<svg viewBox="0 0 24 24"><path d="M6 17V11a6 6 0 0112 0v6l2 2H4zM10 21h4"/></svg>',
    "users": '<svg viewBox="0 0 24 24"><circle cx="9" cy="8" r="3.5"/><path d="M2 20c0-3.5 3-6 7-6s7 2.5 7 6M16 4.5a3.5 3.5 0 010 7M22 20c0-2.8-1.8-4.8-4.5-5.6"/></svg>',
    "phone": '<svg viewBox="0 0 24 24"><path d="M5 4h4l2 5-2.5 1.5a11 11 0 005 5L15 13l5 2v4a2 2 0 01-2 2A16 16 0 013 6a2 2 0 012-2z"/></svg>',
    "mail": '<svg viewBox="0 0 24 24"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/></svg>',
    "globe": '<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c3 3 3 15 0 18M12 3c-3 3-3 15 0 18"/></svg>',
}
SOC = {
    "Instagram": "gN3zRJ", "x.com": "qFQLrw", "LinkedIn": "DVeOb1", "Facebook": "Y5nB02",
}

NAV = [("Home", "index.html"), ("Features", "features.html"), ("About us", "about-us.html"), ("Pricing", "pricing.html"), ("Blog", "blog.html")]


def header(active):
    links = "".join(f'<a href="{{R}}{h}" class="{"on" if h == active else ""}">{t}</a>' for t, h in NAV)
    mlinks = "".join(f'<a href="{{R}}{h}">{t}</a>' for t, h in NAV) + '<a href="{R}contact-us.html">Contact Us</a>'
    return f'''<header class="nav"><div class="nav-in">
<a class="logo" href="{{R}}index.html" aria-label="Nexivo home">{i("nexivo-logo.", "Nexivo", extra='style="height:28px"')}<span class="pwr">Powered by <b>Nexum</b></span></a>
<nav class="menu" aria-label="Main">{links}</nav>
<a class="btn btn-line btn-sm" href="{{R}}contact-us.html"><span class="ic">{CHEV}</span>Contact Us</a>
<button class="burger" aria-label="Menu"><i></i><i></i><i></i></button></div></header>
<div class="mobile-menu">{mlinks}</div>'''


def footer(active=""):
    def li(t, h):
        return f'<li><a href="{{R}}{h}" class="{"on" if h == active else ""}">{t}</a></li>'
    useful = "".join(li(t, h) for t, h in [("Home", "index.html"), ("Features", "features.html"), ("About Us", "about-us.html"), ("Pricing Plan", "pricing.html")])
    quick = "".join(li(t, h) for t, h in [("Contact Us", "contact-us.html"), ("Blog & Articles", "blog.html"), ("Terms of Use", "terms-of-use.html"), ("Privacy Policy", "privacy-policy.html"), ("404", "404.html")])
    soc = "".join(f'<li><a href="#" aria-label="{n}">{i(p, "").replace("loading=", "width=20 height=20 loading=")}{n}</a></li>' for n, p in SOC.items())
    return f'''<footer class="foot" id="top-footer"><div class="wrap"><div class="foot-top">
<div class="fb rv"><a class="logo" href="{{R}}index.html">{i("nexivo-logo.", "Nexivo")}</a>
<p>Nexivo is a complete, customizable learning management solution for educational institutions and organizations — schools, colleges, academies, companies and training teams alike.</p></div>
<div class="rv" style="--d:.08s"><h4>Useful Links</h4><ul>{useful}</ul></div>
<div class="rv" style="--d:.16s"><h4>Quick Links</h4><ul>{quick}</ul></div>
<div class="rv" style="--d:.24s"><h4>Let’s Connect</h4><ul class="soc">{soc}</ul></div></div>
<div class="foot-bar rv" style="--d:.3s"><p>© 2026 Nexivo. All rights reserved.</p><p class="powered">Powered by <b>Nexum</b></p></div></div></footer>
<a class="totop" href="#" aria-label="Back to top"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 19V5M6 11l6-6 6 6"/></svg></a>'''



def tp_stars(rating=4.5):
    """Trustpilot-style rating squares: green = filled, left-half green for a half star, grey = empty."""
    out = ""
    for k in range(5):
        fill = max(0.0, min(1.0, rating - k))
        if fill >= 1:
            bg = '<rect width="24" height="24" fill="#00B67A"/>'
        elif fill <= 0:
            bg = '<rect width="24" height="24" fill="#DCDCE6"/>'
        else:
            bg = '<rect width="24" height="24" fill="#DCDCE6"/><rect width="%d" height="24" fill="#00B67A"/>' % round(24 * fill)
        out += '<svg viewBox="0 0 24 24" width="20" height="20" aria-hidden="true">%s<path fill="#fff" d="M12 4.6l1.9 5.2h5.5l-4.5 3.2 1.7 5.3L12 15.1l-4.6 3.2 1.7-5.3-4.5-3.2h5.5z"/></svg>' % bg
    return '<span class="tp-stars" role="img" aria-label="Rated %s out of 5">%s</span>' % (rating, out)


def vp(icon, hue=1):
    """Brand panel (no photo) for slots that have no unique real product screenshot yet."""
    return f'<div class="vpanel h{hue}"><span class="vp-tile">{IC[icon]}</span></div>'


def btn(label, href, kind="fill", extra=""):
    return f'<a class="btn btn-{kind}"{extra} href="{{R}}{href}"><span class="ic">{CHEV}</span>{label}</a>'


def cta():
    return f'''<section class="sec" style="padding-bottom:0"><div class="cta"><div class="cta-box rv">
<h2>Ready to Transform the Way You Manage Learning?</h2>
<p>Book a demo to see how Nexivo can help you manage learners, courses, batches and results from one centralized platform, and discuss your organization’s requirements with our team.</p>
{btn("Book a Demo", "contact-us.html")}
</div></div></section>'''


FAQS = [
    ("What is Nexivo?", "Nexivo is a learning management system that educational institutions and organizations can purchase and use to manage their own courses, learners, trainers, batches and enrollments from one centralized platform."),
    ("Who is Nexivo for?", "Schools, colleges, academies, coaching centers and training institutes, as well as companies, corporate training teams and other organizations. Each one uses Nexivo to manage its own learning and training activities."),
    ("What can we manage with Nexivo?", "Learner management, batch and class management, courses and training programs, trainers and staff, online and mock tests, results and performance tracking, attendance, grades and organized records, all from one dashboard."),
    ("Can Nexivo be customized for our organization?", "Nexivo is designed to be flexible. Book a demo and tell us about your requirements, and our team will discuss how the platform can fit the way your institution or organization works, including multiple campuses, branches and departments."),
    ("How do we purchase Nexivo?", "Get in touch through the contact page to book a demo. Once we understand your requirements, our team will walk you through the next steps to get your institution or organization started."),
    ("Can we see the platform before we decide?", "Yes. Book a demo and we will show you the platform and answer your questions."),
    ("How can we contact the team?", "Use the contact page to send us your questions or request a demo, and our team will get back to you."),
]


def faq(more=True):
    items = "".join(
        f'<div class="qa{" open" if n == 0 else ""} rv" style="--d:{n*.05}s"><button aria-expanded="{"true" if n == 0 else "false"}">{q}<span class="pm"></span></button><div class="ans"><div><p>{a}</p></div></div></div>'
        for n, (q, a) in enumerate(FAQS))
    tail = f'''<div class="faq-more rv"><h3>Still Have Questions?</h3><p>Can't find what you need? Contact our team and we'll be happy to help.</p>
{btn("Contact Us", "contact-us.html")}</div>''' if more else ""
    return f'''<section class="sec grad-bg"><div class="wrap"><div class="sec-head rv"><h2 class="h2">Everything You Need to Know About Nexivo</h2>
<p>Got questions? Here are the answers institutions and organizations ask most, and if you need more, we’re a message away.</p></div>
<div class="faq">{items}</div>{tail}</div></section>'''


# ---------- page shell ----------
def page(fname, title, body, active="", depth=0, desc="Nexivo – a complete learning management solution for educational institutions and organizations, from schools and colleges to companies and training teams."):
    R = "../" * depth
    doc = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title><meta name="description" content="{desc}">
<link rel="icon" href="{{R}}{img("t5WQFF")}">
<link rel="preload" href="{{R}}assets/fonts/PlusJakartaSans.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="{{R}}assets/fonts/DMSans.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{{R}}css/style.css?v={VER}"></head><body>
{header(active)}
<main>{body}</main>
{footer(active)}
<script src="{{R}}js/main.js?v={VER}"></script></body></html>'''
    doc = re.sub(r'(<span class="ic">.*?</span>)([^<>]+)(</(?:a|button)>)', lambda m: m.group(1) + '<span class="lb">' + m.group(2) + '</span>' + m.group(3), doc, flags=re.S)
    doc = doc.replace("{R}", R).replace("{VER}", VER)
    with open(os.path.join(ROOT, fname), "w", encoding="utf8") as f:
        f.write(doc)


# ---------- HOME ----------
def home():
    hero = f'''<section class="hero" style="padding-bottom:56px"><div class="bg-glow"></div>
<div class="float pf" aria-hidden="true">{i("card-staff", "", extra='width=222 height=203 loading="eager"')}</div><div class="float ts" aria-hidden="true">{i("card-trainees", "", extra='width=222 height=203 loading="eager"')}</div><div class="wrap" style="position:relative">
<div class="badge rv">{i("Gk7czz", "")}Built for institutions &amp; organizations of every kind</div>
<h1 class="h1 rv" style="--d:.08s">Scale Your Impact, <b>Simplify Your Operations</b></h1>
<p class="lead rv" style="--d:.16s">Nexivo is a complete, customizable learning management solution that brings your learners, trainers, courses, batches and results together on one centralized platform.</p>
{btn("Book a Demo", "contact-us.html", "fill", ' style="--d:.24s"').replace('class="btn btn-fill"', 'class="btn btn-fill rv"')}
<div class="rate rv" style="--d:.3s"><div class="src">{i("YJtCU4", "Trustpilot")}{tp_stars(4.5)}<span>4.5/5</span></div></div>
<div class="hero-visual rv rv-s" style="--d:.35s;margin-top:76px">
<div class="dash devframe">{i("nexivo-app-hero", "Nexivo coordinator dashboard", extra='width=1592 height=750 loading="eager"')}</div>
</div></div></section>'''

    bento = f'''<section class="sec"><div class="wrap"><div class="sec-head rv"><h2 class="h2">One Platform to Run Your Entire Organization</h2>
<p>Nexivo gives administrators, coordinators and trainers a single place to manage learners, batches, courses, assessments and results, with less manual work and more control.</p></div>
<div class="bento">
<article class="fcard wide span-4 rv" style="display:flex;flex-direction:column;padding-right:24px"><div><h3>Role-Based Dashboards</h3><p>Admins manage campuses and coordinators, while coordinators track registrations, batches and learners for their own campus or department.</p></div>
<div class="shot dots wshot">{i("nexivo-mpcs", "Nexivo MPCs management screen", extra='style="border-radius:12px 12px 0 0;box-shadow:0 14px 34px rgba(0,0,0,.12)"')}</div></article>
<article class="fcard span-2 rv" style="--d:.1s"><h3>Live &amp; Online Classes</h3><p>Schedule, join and review live classes and their recordings for each batch.</p><div class="shot">{i("nexivo-live", "Nexivo live classes screen", extra='style="border-radius:14px"')}</div></article>
<article class="fcard span-2 rv"><h3>Registration Tracking</h3><p>Follow every registration from review to approved account.</p><div class="shot" style="display:grid;place-items:center;background:#fbf7f4;padding:20px">{i("nexivo-analytics-card", "Nexivo registration funnel", extra='style="width:100%;border-radius:12px;box-shadow:0 14px 34px rgba(0,0,0,.10)"')}</div></article>
<article class="fcard span-2 rv" style="--d:.1s"><h3>Online &amp; Mock Tests</h3><p>Conduct online and mock tests and review results without the manual effort.</p><div class="shot">{i("oLnsEY", "Test results")}</div></article>
<article class="fcard span-2 rv" style="--d:.2s"><h3>Enrollments &amp; Registrations</h3><p>Track registrations, verification and admissions across every campus or branch.</p><div class="shot" style="padding:0;overflow:hidden">{i("nexivo-enrollments.", "Nexivo enrollments and registrations screen", extra='style="width:100%;height:260px;object-fit:cover;object-position:left top;display:block"')}</div></article>
</div><div class="center-cta rv">{btn("Explore All Features", "features.html", "line")}</div></div></section>'''

    steps = f'''<section class="sec grad-bg"><div class="wrap"><div class="sec-head rv"><h2 class="h2">Getting Started with Nexivo</h2></div>
<div class="steps rv">
<div class="step"><div class="ico">{IC["user"]}</div><h3>Book a Demo</h3><p>Tell us about your institution or organization and see Nexivo in action.</p></div>
<div class="step"><div class="ico">{IC["chat"]}</div><h3>Share Your Requirements</h3><p>Discuss your courses, batches, staff and workflows with our team so the platform fits your needs.</p></div>
<div class="step"><div class="ico">{IC["cap"]}</div><h3>Launch &amp; Manage</h3><p>Bring your learners, trainers and courses onto one centralized platform and manage everything with more control.</p></div></div></div>
<div class="wrap" style="margin-top:72px"><div class="sec-head rv" style="margin-bottom:30px"><h2 class="h2">Benefits of Nexivo – Why Institutions &amp; Organizations Choose It</h2>
<p>Less manual work, faster updates and better learning management, all from one centralized platform.</p></div>
<div class="stack rv">
<div class="scard"><div class="im">{i("zDhZ8K", "Course management")}</div><h3>Course &amp; Batch Management</h3><p>Manage courses, programs, batches and classes without juggling spreadsheets.</p></div>
<div class="scard"><div class="im">{i("nexivo-staff", "Nexivo staff management screen")}</div><h3>Trainer &amp; Staff Management</h3><p>Manage coordinators, trainers and platform roles from one screen.</p></div>
<div class="scard"><div class="im">{i("nexivo-attendance", "Nexivo attendance screen")}</div><h3>Organized Attendance Records</h3><p>Review batch session attendance and records without the paperwork.</p></div>
<div class="scard"><div class="im">{i("nexivo-grades", "Nexivo grades screen")}</div><h3>Grades &amp; Results</h3><p>Review and assign grades and keep results organized for every learner.</p></div>
<div class="scard"><div class="im">{i("mSuIih", "Online class")}</div><h3>Online Learning &amp; Live Classes</h3><p>Deliver classes online so your learners can join and learn from anywhere.</p></div></div>
<div class="arrows rv"><button class="arr prev" aria-label="Previous">{ARL}</button><button class="arr next" aria-label="Next">{ARR}</button></div></div></section>'''

    about = f'''<section class="sec"><div class="wrap"><div class="about">
<div class="rv rv-l"><h2 class="h2" style="font-size:44px">One Platform for Every Institution &amp; Organization</h2>
<p>Nexivo is built for institutions and organizations alike. Whether you run a school, college or academy, or a company with its own training programs, you can use Nexivo to manage your own courses, learners, trainers and enrollments across every campus, branch or department.</p>
<div class="pills"><span class="pill"><i></i>Complete &amp; flexible</span><span class="pill"><i></i>Customizable to your needs</span></div>
{btn("Learn More", "about-us.html", "line")}</div>
<div class="photo rv rv-r" style="aspect-ratio:auto;border:8px solid #1a1b22;border-radius:26px;box-shadow:0 24px 50px rgba(17,19,24,.14);background:#fff">{i("nexivo-admin", "Nexivo admin operations dashboard", extra='width=1592 height=724 style="height:auto"')}</div></div></div></section>'''

    mods = [("users", "Learners"), ("path", "Batches & Classes"), ("book", "Courses"), ("cap", "Trainers & Staff"),
            ("note", "Online Tests"), ("target", "Results"), ("clock", "Attendance & Grades"), ("chart", "Reports")]
    xs = [45, 175, 305, 435, 565, 695, 825, 955]
    R_, Y_, B_ = 32, 91, 162
    paths = ""
    for x in xs:
        if x in (435, 565):
            d = f"M500 0V{Y_}H{x}V{B_}"
        elif x < 500:
            d = f"M500 0V{Y_}H{x + R_}Q{x} {Y_} {x} {Y_ + R_}V{B_}"
        else:
            d = f"M500 0V{Y_}H{x - R_}Q{x} {Y_} {x} {Y_ + R_}V{B_}"
        paths += f'<path class="tl" pathLength="1" d="{d}"/>'
    dots = "".join(f'<circle r="3.2" fill="#ff6400"><animateMotion dur="3.6s" begin="-{k * .45:.2f}s" repeatCount="indefinite" path="{re.search(r"d=.([^\"]+)", p).group(1)}"/></circle>' for k, p in enumerate(re.findall(r'<path[^>]*/>', paths)))
    tiles = "".join(f'<div class="tn" style="left:{x - 41.5}px"><div class="tt">{IC[ic]}</div><span>{t}</span></div>' for x, (ic, t) in zip(xs, mods))
    tree = f'''<section class="sec integ"><div class="wrap"><div class="sec-head rv" style="margin-bottom:10px"><h2 class="h2">One Platform for Every Part of Your Organization</h2>
<p>Nexivo connects the core areas of running your institution or organization (learners, batches, courses, trainers, tests, results, attendance and reports) in one centralized platform.</p></div>
<div class="tree rv"><div class="tree-stage"><div class="hub">{i("nexivo-icon", "Nexivo")}</div>
<svg class="tlines" viewBox="0 0 1000 {B_}" width="1000" height="{B_}" aria-hidden="true">{paths}{dots}</svg>{tiles}</div></div>
<div class="center-cta rv">{btn("Request a Demo", "contact-us.html")}</div></div></section>'''

    kinds = [("cap", "Schools &amp; Colleges", "Manage classes, students, teachers and results in one place."),
             ("book", "Academies &amp; Institutes", "Keep courses, trainers and enrollments organized."),
             ("users", "Coaching Centers", "Run batches, tests and performance tracking with ease."),
             ("bolt", "Companies &amp; Corporate Teams", "Deliver employee training and track learning across departments."),
             ("globe", "Multi-Campus Groups", "Manage multiple campuses, branches and centers under one system."),
             ("target", "Any Organization", "Adapt Nexivo to the way your organization works.")]
    kb = "".join(f'<article class="fbox rv" style="--d:{(n%3)*.08}s"><div class="ico">{IC[ic]}</div><h3>{t}</h3><p>{d}</p></article>' for n, (ic, t, d) in enumerate(kinds))
    who = f'''<section class="sec"><div class="wrap"><div class="sec-head rv"><h2 class="h2">Built for Every Kind of Institution &amp; Organization</h2>
<p>Purchase Nexivo and use it to manage your own learning and training activities, courses, learners, trainers and enrollments.</p></div><div class="frow">{kb}</div></div></section>'''

    body = hero + bento + steps + about + tree + who + faq() + cta()
    page("index.html", "Nexivo – Learning Management System for Institutions &amp; Organizations", body, "index.html", desc="Nexivo is a complete, customizable learning management solution for educational institutions and organizations, from schools and colleges to companies and training teams.")


# ---------- FEATURES ----------
def features():
    hero = f'''<section class="phero"><div class="wrap"><h1 class="rv">Everything Your Institution or Organization Needs, on One Platform</h1>
<p class="rv" style="--d:.1s">Nexivo brings course management, learner enrollment, trainer management, online learning, assessments and reporting together, so your team can run with more control and less manual work.</p></div></section>'''
    rows = f'''<section class="sec" style="padding-top:60px"><div class="wrap"><div class="bento">
<article class="fcard span-3 rv"><h3>Live &amp; Online Classes</h3><p>Schedule, join and review live classes and their recordings for each batch.</p><div class="shot" style="padding:0;overflow:hidden">{i("nexivo-live.", "Nexivo live and online classes screen", extra='style="width:100%;height:auto;display:block"')}</div></article>
<article class="fcard span-3 rv" style="--d:.1s;padding:0"><div class="offer" style="min-height:100%;grid-template-columns:1fr;border-radius:30px;height:100%"><div class="t"><span class="tag">Book a Demo</span><h3>Run Your Organization <b>Smarter</b></h3><p>See Nexivo in action and discuss your requirements with our team.</p>{btn("Book a Demo", "contact-us.html", "line", ' style="margin-top:24px"')}</div></div></article>
<article class="fcard span-6 rv" style="grid-column:span 6"><h3>Batch &amp; Enrollment Overview</h3><p>Monitor active learners, staff, batches and registrations across your campuses at a glance.</p><div class="shot" style="padding:0;overflow:hidden">{i("nexivo-reports", "Nexivo reports and impact review screen", extra='style="width:100%;height:auto;display:block"')}</div></article>
</div></div></section>'''
    items = [
        ("users", "Learner Management", "Manage learner and employee profiles, enrollments and records in one place."),
        ("path", "Batch & Class Management", "Organize your batches and classes and keep them running smoothly."),
        ("book", "Course Management", "Create and manage the courses and training programs your organization offers."),
        ("cap", "Trainer & Staff Management", "Manage trainers and staff alongside your learners and courses."),
        ("note", "Online & Mock Tests", "Conduct online assessments and mock tests for your learners."),
        ("target", "Results & Performance Tracking", "Track results and monitor learner performance over time."),
        ("clock", "Attendance & Grades", "Keep attendance and grades organized and up to date."),
        ("fire", "Admissions & Enrollments", "Handle registrations and enrollments for your institution or organization."),
        ("chart", "Reports & Admin Dashboard", "Get a platform-wide overview of users, batches and admissions activity."),
    ]
    boxes = "".join(f'<article class="fbox rv" style="--d:{(n%3)*.08}s"><div class="ico">{IC[ic]}</div><h3>{t}</h3><p>{d}</p></article>' for n, (ic, t, d) in enumerate(items))
    future = f'''<section class="sec grad-bg"><div class="wrap"><div class="sec-head rv"><h2 class="h2">Built to Manage Your Institution or Organization</h2>
<p>Everything administrators, coordinators and trainers need to manage daily learning and training operations from one centralized platform.</p></div><div class="frow">{boxes}</div></div></section>'''
    nxt = [("Role-Based Dashboards", "Give admins and coordinators dashboards built around the work they do.", "users"),
           ("Multi-Campus & Branch Management", "Oversee your campuses, branches and departments from a single platform.", "globe"),
           ("Faster Updates, Better Efficiency", "Reduce manual work and keep information current across your organization.", "bolt"),
           ("Less Manual Work, More Control", "Replace scattered records with one centralized platform.", "note")]
    nb = "".join(f'<article class="fbox rv" style="--d:{(n%2)*.1}s"><div class="ico" style="flex:none;margin:0">{IC[ic]}</div><div><h3>{t}</h3><p>{d}</p></div></article>' for n, (t, d, ic) in enumerate(nxt))
    nextgen = f'''<section class="sec"><div class="wrap"><div class="sec-head rv"><h2 class="h2">Organization-Level Management</h2><p>Designed so every institution and organization can manage its own learning and training its own way.</p></div><div class="nextgrid">{nb}</div></div></section>'''
    page("features.html", "Features - Nexivo", hero + rows + future + nextgen + cta(), "features.html", desc="Explore Nexivo features for learner, batch, course and trainer management, online tests and results tracking.")


# ---------- ABOUT ----------
def about():
    hero = f'''<section class="phero"><div class="wrap">
<h1 class="rv">Built for the Institutions &amp; Organizations That Shape Learners</h1>
<p class="rv" style="--d:.16s">Nexivo is a commercial learning management solution that any educational institution or organization can purchase and use to manage its own courses, learners, trainers and enrollments across every campus, branch or department.</p>
{btn("Book a Demo", "contact-us.html", "fill", ' style="--d:.24s"').replace('class="btn btn-fill"', 'class="btn btn-fill rv"')}</div></section>'''
    story = f'''<section class="sec"><div class="wrap"><div class="story">
<div class="rv rv-l"><h2>Run Your Organization Smarter with Nexivo</h2><p>Still managing learner records, batches, mock tests and results manually? There’s a smarter way. With Nexivo you can manage your institution or organization from one centralized platform.</p>
{btn("Explore Nexivo Features", "features.html", "line")}</div>
<div class="duo rv rv-r"><article class="fcard"><h3 style="font-size:22px">Learner &amp; Batch Management</h3><p style="font-size:16px">Keep learners, batches and classes organized in one place.</p></article>
<article class="fcard"><h3 style="font-size:22px">Online &amp; Mock Tests</h3><p style="font-size:16px">Assess your learners and keep track of their results.</p></article></div></div></div></section>'''
    gap = f'''<section class="sec grad-bg"><div class="wrap"><div class="sec-head rv"><h2 class="h2">Bring Your Learning &amp; Training Online</h2>
{btn("Book a Demo", "contact-us.html", "fill", ' style="margin-top:26px"')}</div>
<div class="duo"><div class="photo rv" style="aspect-ratio:1/1">{i("nexivo-about-1", "Nexivo live classes")}</div><div class="photo rv" style="--d:.1s;aspect-ratio:1/1">{i("nexivo-about-2", "Nexivo dashboard overview", extra='style="object-position:left top"')}</div></div></div></section>'''
    comm = f'''<section class="sec"><div class="wrap"><div class="about"><div class="rv rv-l"><h2 class="h2" style="font-size:44px">Customized for Your Organization</h2>
<p>Every institution and organization works differently. Tell us how yours does, and we’ll discuss how Nexivo can fit your requirements.</p>
<div style="margin-top:28px">{btn("Discuss Your Requirements", "contact-us.html", "line")}</div></div>
<div class="photo rv rv-r">{i("nexivo-about-3", "Nexivo admin operations", extra='style="object-position:left top"')}</div></div></div></section>'''
    xp = f'''<section class="sec" style="padding-top:0"><div class="wrap"><div class="xp">
<article class="card rv" style="background:var(--peach)"><h3>One Centralized Platform</h3><p>Learners, trainers, courses, batches, attendance, grades and results, managed together instead of scattered across different tools.</p></article>
<article class="card rv" style="--d:.1s;background:#f6f4ff"><h3>Flexible &amp; Customizable</h3><p>Designed for educational institutions and organizations alike, and adaptable to the way each one operates across its campuses, branches and departments.</p></article></div></div></section>'''
    page("about-us.html", "About Us - Nexivo", hero + story + gap + comm + xp + cta(), "about-us.html", desc="Nexivo is a learning management solution that educational institutions and organizations can purchase and use for their own needs.")


# ---------- PRICING ----------
def pricing():
    hero = f'''<section class="phero" style="padding-bottom:50px"><div class="wrap"><h1 class="rv">Simple, Flexible Pricing</h1><p class="rv" style="--d:.1s">Plans for educational institutions and organizations of every size, from a single campus to multi-campus groups and large enterprises. Pick the plan that fits how you operate, and scale as you grow.</p></div></section>'''
    # (nm, price, period, description, hot, cta label, cta kind, lead-in line, [features])
    cards = [
        ("Single Campus", "$49", "/mo", "For a single institution running at one location.", False, "Get Started", "line", "Core LMS included:",
         ["One campus or location", "Up to 500 learners", "Course &amp; batch management", "Trainer &amp; staff management", "Online &amp; mock tests", "Attendance, grades &amp; results", "Reports &amp; admin dashboard", "Email support"]),
        ("Multi-Campus", "$149", "/mo", "For organizations running multiple campuses, branches and departments.", True, "Book a Demo", "fill", "Everything in Single Campus, plus:",
         ["Multiple campuses &amp; branches", "Department-level management", "Up to 5,000 learners", "Role-based dashboards per campus", "Consolidated reports across campuses", "Bulk enrollments &amp; admissions", "Priority support"]),
        ("Enterprise", "Custom", "", "For large institutions and organizations with custom requirements.", False, "Contact Sales", "line", "Everything in Multi-Campus, plus:",
         ["Unlimited campuses &amp; learners", "Custom roles &amp; permissions", "Custom integrations &amp; branding", "Dedicated account manager", "Onboarding &amp; training", "SLA-backed support"]),
    ]
    cb = ""
    for n, (nm, price, period, ds, hot, bt, kind, lead, feats) in enumerate(cards):
        pr = f'{price}<small>{period} *</small>' if period else price
        lis = f'<li class="hd">{lead}</li>' + "".join(f"<li>{CHECK}{f}</li>" for f in feats)
        tag = '<span class="tag" style="display:inline-block;margin-bottom:12px">Most popular</span>' if hot else ""
        cb += f'''<article class="plan{" hot" if hot else ""} rv" style="--d:{n*.1}s">{tag}<div class="nm">{nm}</div><div class="pr">{pr}</div><p class="ds">{ds}</p>
{btn(bt, "contact-us.html", kind)}<ul>{lis}</ul></article>'''
    plans = f'''<section class="sec" style="padding-top:40px"><div class="wrap"><div class="sec-head rv"><h2 class="h2">Plans for Every Size of Institution &amp; Organization</h2>
<p>Every plan is licensed to your institution or organization and billed per month. Add campuses, branches and departments as you grow.</p></div><div class="plans">{cb}</div>
<p class="rv" style="text-align:center;margin-top:28px;font-size:15px;color:var(--gray)">* Example figures shown for layout. <a href="{{R}}contact-us.html" style="color:var(--orange)">Contact us</a> for a tailored quote based on your campuses, learners and requirements.</p></div></section>'''
    caps = ["Learner management", "Batch & class management", "Course & program management", "Trainer & staff management", "Online & mock tests", "Results & performance tracking", "Attendance & grades", "Organized records", "Admissions & enrollments", "Reports & admin dashboard"]
    cl = "".join(f"<li>{CHECK}{c}</li>" for c in caps)
    cmp_ = f'''<section class="sec grad-bg"><div class="wrap"><div class="sec-head rv"><h2 class="h2">Included in Every Plan</h2>
<p>Whatever plan you choose, these are the core tools you’ll use to manage your learning and training activities.</p></div>
<div class="plan rv" style="max-width:860px;margin:0 auto"><ul class="capgrid" style="border-top:0;padding-top:0;grid-template-columns:repeat(2,1fr)">{cl}</ul></div></div></section>'''
    page("pricing.html", "Pricing - Nexivo", hero + plans + cmp_ + faq(False) + cta(), "pricing.html", desc="Nexivo pricing plans for educational institutions and organizations — single campus, multi-campus and enterprise, with multi-branch and department support.")


# ---------- BLOG ----------
POSTS = [
    ("Institutions & Organizations", "Why Centralized Records Matter", "How keeping learner, batch and result data in one platform reduces manual work for administrators.", "img:nexivo-enrollments-blog."),
    ("Institutions & Organizations", "Managing Batches and Classes Without the Spreadsheets", "A practical look at organizing batches, classes and schedules across your campuses and departments.", "img:nexivo-batches."),
    ("Institutions & Organizations", "Choosing a Learning Management System", "Key questions institutions and organizations should ask before they buy.", "img:nexivo-courses."),
    ("Online Learning & Assessments", "Running Live Classes for Your Batches", "How to schedule, join and review live classes and their recordings for each batch.", "img:nexivo-blog-4."),
    ("Online Learning & Assessments", "Tracking Learner Performance Over Time", "Why consistent results tracking helps trainers and administrators act earlier.", "img:nexivo-analytics."),
    ("Nexivo Features & Updates", "What’s New in Nexivo", "Product updates and announcements from the Nexivo team.", "img:nexivo-support."),
]


def post(p, hidden=False):
    cat, t, x, im = p
    ic, hue = im.split(":")
    return f'<a class="post rv{" hidden" if hidden else ""}" data-cat="{cat}" href="{{R}}blog.html" style="{"display:none" if hidden else ""}"><div class="im">{i(hue, t, extra='style="width:100%;height:100%;object-fit:cover;object-position:left top"') if ic == "img" else vp(ic, int(hue))}</div><div class="tx"><div class="meta"><span>{cat}</span></div><h3>{t}</h3><p>{x}</p></div></a>'


def blog():
    hero = f'''<section class="phero" style="padding-bottom:50px"><div class="wrap"><h1 class="rv">Insights for Institutions &amp; Organizations</h1>
<p class="rv" style="--d:.1s">Practical ideas on managing learners, batches, tests and results, and on getting more from your learning management system.</p>
<div class="search rv" style="--d:.2s"><input type="text" placeholder="Ex. Managing batches" aria-label="Search articles"><span>{'<svg viewBox="0 0 24 24"><circle cx="11" cy="11" r="7"/><path d="M20 20l-4-4"/></svg>'}</span></div></div></section>'''
    cats = ["All Categories", "Institutions & Organizations", "Online Learning & Assessments", "Nexivo Features & Updates"]
    chips = "".join(f'<button class="chip{" on" if n == 0 else ""}" data-cat="{"all" if n == 0 else c}">{c}</button>' for n, c in enumerate(cats))
    grid = f'''<section class="sec" style="padding-top:40px"><div class="wrap"><div class="sec-head rv" style="margin-bottom:30px"><h2 class="h2" style="font-size:40px">Latest Articles</h2></div>
<div class="chips rv">{chips}</div><div class="bgrid">{"".join(post(p, n >= 4) for n, p in enumerate(POSTS))}</div>
<div class="center-cta rv"><a id="loadmore" class="btn btn-line" href="#"><span class="ic">{CHEV}</span>Load More Articles</a></div></div></section>'''
    page("blog.html", "Blog - Nexivo", hero + grid + cta(), "blog.html", desc="Articles for educational institutions and organizations from the Nexivo team.")


# ---------- CONTACT ----------
def contact():
    hero = f'''<section class="phero" style="padding-bottom:50px"><div class="wrap"><h1 class="rv">Let’s Talk About Your Organization</h1>
<p class="rv" style="--d:.1s">Book a demo, share your requirements or ask us anything about Nexivo. Tell us about your institution or organization and our team will get back to you.</p></div></section>'''
    opts = "".join(f"<option>{o}</option>" for o in ["Book a Demo", "Discuss My Requirements", "Request a Quote", "Ask a Question"])
    form = f'''<section class="sec" style="padding-top:40px"><div class="wrap"><div class="contact">
<div class="cinfo rv rv-l"><h2>Book a Demo</h2><p>See how Nexivo can help your organization run smarter. Fill in the form and tell us what you need.</p>
<div class="cline"><span class="ico">{IC["chat"]}</span><div><small>Discuss</small><b>Your requirements</b></div></div>
<div class="cline"><span class="ico">{IC["cap"]}</span><div><small>See</small><b>The platform in action</b></div></div></div>
<form class="form rv rv-r" id="contactForm" novalidate>
<label>Full Name*<input type="text" name="name" placeholder="Enter your full name" required><span class="err">Please enter your name.</span></label>
<label>Email Address*<input type="email" name="email" placeholder="Enter your email" required><span class="err">Please enter a valid email.</span></label>
<label>Institution / Organization Name<input type="text" name="institution" placeholder="Enter your institution or organization name"></label>
<label>How can we help?<select name="service"><option value="">Select an option</option>{opts}</select></label>
<label>Leave a Message<textarea name="message" placeholder="Tell us about your organization and requirements"></textarea></label>
<label class="ck"><input type="checkbox" required> I agree to the&nbsp;<a href="{{R}}privacy-policy.html">privacy policy</a><span class="err" style="margin-left:8px">Required.</span></label>
<button class="btn btn-fill" type="submit" style="justify-self:start"><span class="ic">{CHEV}</span>Send Request</button></form></div></div></section>'''
    page("contact-us.html", "Contact Us - Nexivo", hero + form + faq(False) + cta(), "contact-us.html", desc="Book a demo or discuss your requirements with the Nexivo team.")


# ---------- LEGAL ----------
def legal(fname, title, text):
    blocks = [b.strip() for b in text.strip().split("\n\n") if b.strip()]
    out = ""
    for b in blocks:
        lines = b.split("\n")
        out += '<div class="rv"><h2>' + html.escape(lines[0]) + "</h2>" + "".join(f"<p>{html.escape(l)}</p>" for l in lines[1:]) + "</div>"
    body = f'<section class="legal"><h1 class="rv">{title}</h1><div>{out}</div></section>'
    page(fname, f"{title} - Nexivo", body, "")


def legal_from_txt(fname, title, srcfile):
    p = os.path.join(ROOT, "content", srcfile)
    if os.path.exists(p):
        legal(fname, title, open(p, encoding="utf8").read())


def notfound():
    body = f'<section class="nf"><div><b class="rv">404</b><h1 class="rv" style="--d:.1s">Oops! This page took a day off.</h1><a class="btn btn-fill rv" style="--d:.2s" href="{{R}}index.html"><span class="ic">{CHEV}</span>Back to Home</a></div></section>'
    page("404.html", "404 - Nexivo", body, "")


if __name__ == "__main__":
    home(); features(); about(); pricing(); blog(); contact(); notfound()
    legal_from_txt("privacy-policy.html", "Privacy Policy", "privacy-policy.txt")
    legal_from_txt("terms-of-use.html", "Terms of Use", "terms-of-use.txt")
    print("built")
