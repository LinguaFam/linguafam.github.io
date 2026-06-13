"""
Portfolio Site Builder for Shilpa Deol
========================================
Reads data.json and generates index.html automatically.

Usage:
    python build_site.py

Run this after scrape_urbanpro.py, or anytime you edit data.json manually.
The output index.html is ready to upload to GitHub.
"""

import json
import os

DATA_FILE   = "data.json"
OUTPUT_FILE = "index.html"


def load_data():
    with open(DATA_FILE, encoding="utf-8") as f:
        return json.load(f)


def stars_html(n):
    return "★" * int(n) + "☆" * (5 - int(n))


def render_reviews(reviews):
    cards = ""
    for r in reviews:
        cards += f"""
      <div class="review-card fade-up">
        <div class="review-stars">{stars_html(r.get('stars', 5))}</div>
        <p class="review-text">"{r['text']}"</p>
        <div class="review-author">{r['name']}</div>
        <div class="review-context">{r.get('context','')}</div>
        <span class="verified-badge">✓ Verified Student</span>
      </div>"""
    return cards


def render_awards(awards):
    cards = ""
    for a in awards:
        cards += f"""
      <div class="award-card fade-up">
        <div class="award-icon">{a['icon']}</div>
        <div class="award-title">{a['title']}</div>
        <div class="award-desc">{a['desc']}</div>
      </div>"""
    return cards


def render_schools(schools):
    # Doubled for infinite scroll ticker
    chips = "".join(
        f'<div class="school-chip">{s}</div>'
        for s in schools * 2
    )
    return chips


def build(data):
    reviews_html = render_reviews(data.get("reviews", []))
    awards_html  = render_awards(data.get("awards", []))
    schools_html = render_schools(data.get("schools", []))

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>Shilpa Deol — French Language Educator</title>
  <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;1,400&family=DM+Sans:wght@300;400;500;600&display=swap" rel="stylesheet"/>
  <style>
    *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
    :root {{
      --navy:#1B3A5C; --navy2:#0F2540; --gold:#C9A84C; --gold2:#E8C96A;
      --cream:#F7F3EE; --dark:#1A1A2E; --mid:#4A6080; --light:#EAF0F7; --white:#FFFFFF;
    }}
    html {{ scroll-behavior: smooth; }}
    body {{ font-family:'DM Sans',sans-serif; background:var(--cream); color:var(--dark); overflow-x:hidden; }}

    nav {{
      position:fixed; top:0; left:0; right:0; z-index:100;
      background:rgba(27,58,92,0.96); backdrop-filter:blur(8px);
      display:flex; justify-content:space-between; align-items:center;
      padding:14px 48px;
    }}
    .nav-logo {{ font-family:'Playfair Display',serif; color:var(--gold); font-size:1.1rem; letter-spacing:1px; }}
    .nav-links {{ display:flex; gap:32px; }}
    .nav-links a {{ color:rgba(255,255,255,0.8); text-decoration:none; font-size:0.85rem; transition:color 0.2s; }}
    .nav-links a:hover {{ color:var(--gold); }}

    .hero {{
      min-height:100vh; background:linear-gradient(135deg,var(--navy2) 0%,var(--navy) 60%,#2D5B8E 100%);
      display:flex; align-items:center; padding:100px 48px 60px; position:relative; overflow:hidden;
    }}
    .hero::before {{
      content:"FRANÇAIS"; position:absolute; right:-40px; top:50%;
      transform:translateY(-50%) rotate(90deg);
      font-family:'Playfair Display',serif; font-size:10rem; font-weight:700;
      letter-spacing:20px; color:rgba(255,255,255,0.03); white-space:nowrap; pointer-events:none;
    }}
    .hero-inner {{ max-width:1100px; margin:0 auto; display:grid; grid-template-columns:1fr 1fr; gap:80px; align-items:center; width:100%; }}
    .hero-tag {{ display:inline-block; color:var(--gold); font-size:0.8rem; letter-spacing:3px; text-transform:uppercase; margin-bottom:16px; border-left:2px solid var(--gold); padding-left:12px; }}
    .hero h1 {{ font-family:'Playfair Display',serif; font-size:clamp(2.8rem,5vw,4.2rem); color:white; line-height:1.1; margin-bottom:20px; }}
    .hero h1 em {{ color:var(--gold); font-style:italic; }}
    .hero-sub {{ color:rgba(255,255,255,0.7); font-size:1.05rem; line-height:1.7; margin-bottom:36px; font-weight:300; }}
    .hero-btns {{ display:flex; gap:16px; flex-wrap:wrap; }}
    .btn-primary {{ background:var(--gold); color:var(--navy2); padding:14px 28px; border-radius:4px; text-decoration:none; font-weight:600; font-size:0.9rem; transition:background 0.2s,transform 0.2s; display:inline-flex; align-items:center; gap:8px; }}
    .btn-primary:hover {{ background:var(--gold2); transform:translateY(-2px); }}
    .btn-outline {{ border:1px solid rgba(255,255,255,0.4); color:white; padding:14px 28px; border-radius:4px; text-decoration:none; font-weight:400; font-size:0.9rem; transition:border-color 0.2s,background 0.2s; display:inline-flex; align-items:center; gap:8px; }}
    .btn-outline:hover {{ border-color:var(--gold); background:rgba(201,168,76,0.1); }}

    .hero-stats {{ display:grid; grid-template-columns:repeat(2,1fr); gap:20px; }}
    .stat-card {{ background:rgba(255,255,255,0.06); border:1px solid rgba(255,255,255,0.1); border-radius:8px; padding:24px 20px; text-align:center; transition:background 0.2s; }}
    .stat-card:hover {{ background:rgba(255,255,255,0.1); }}
    .stat-num {{ font-family:'Playfair Display',serif; font-size:2.6rem; color:var(--gold); font-weight:700; display:block; line-height:1; }}
    .stat-label {{ color:rgba(255,255,255,0.6); font-size:0.8rem; letter-spacing:1px; text-transform:uppercase; margin-top:6px; display:block; }}

    section {{ padding:90px 48px; }}
    .section-inner {{ max-width:1100px; margin:0 auto; }}
    .section-eyebrow {{ color:var(--gold); font-size:0.75rem; letter-spacing:3px; text-transform:uppercase; margin-bottom:12px; display:block; }}
    .section-title {{ font-family:'Playfair Display',serif; font-size:clamp(1.8rem,3vw,2.4rem); color:var(--navy); margin-bottom:48px; line-height:1.2; }}
    .section-title span {{ color:var(--gold); }}

    #about {{ background:var(--white); }}
    .about-grid {{ display:grid; grid-template-columns:1fr 1.6fr; gap:80px; align-items:start; }}
    .about-left {{ position:sticky; top:100px; }}
    .about-photo-wrap {{ width:100%; aspect-ratio:3/4; background:var(--navy); border-radius:4px; overflow:hidden; position:relative; }}
    .about-photo-wrap img {{ width:100%; height:100%; object-fit:cover; filter:grayscale(20%); }}
    .about-photo-badge {{ position:absolute; bottom:16px; left:16px; right:16px; background:var(--gold); border-radius:4px; padding:10px 14px; text-align:center; }}
    .about-photo-badge strong {{ display:block; color:var(--navy2); font-size:0.85rem; font-weight:700; }}
    .about-photo-badge span {{ color:var(--navy2); font-size:0.75rem; opacity:0.8; }}
    .about-body p {{ color:var(--mid); line-height:1.8; font-size:1rem; margin-bottom:20px; font-weight:300; }}
    .about-body p strong {{ color:var(--navy); font-weight:600; }}
    .badges {{ display:flex; flex-wrap:wrap; gap:10px; margin-top:28px; }}
    .badge {{ background:var(--light); color:var(--navy); padding:6px 14px; border-radius:20px; font-size:0.8rem; font-weight:500; border:1px solid rgba(27,58,92,0.12); }}
    .links-row {{ display:flex; gap:16px; margin-top:28px; flex-wrap:wrap; }}
    .profile-link {{ display:inline-flex; align-items:center; gap:8px; background:var(--navy); color:white; padding:10px 18px; border-radius:4px; text-decoration:none; font-size:0.85rem; font-weight:500; transition:background 0.2s; }}
    .profile-link:hover {{ background:var(--navy2); }}
    .profile-link.gold {{ background:var(--gold); color:var(--navy2); }}
    .profile-link.gold:hover {{ background:var(--gold2); }}

    #schools {{ background:var(--navy2); overflow:hidden; padding:80px 0; }}
    #schools .section-inner {{ padding:0 48px; }}
    #schools .section-title {{ color:white; }}
    .schools-intro {{ color:rgba(255,255,255,0.6); margin-bottom:48px; font-size:1rem; line-height:1.7; }}
    .ticker-wrap {{ overflow:hidden; position:relative; margin-top:20px; }}
    .ticker-wrap::before,.ticker-wrap::after {{ content:''; position:absolute; top:0; bottom:0; width:80px; z-index:2; }}
    .ticker-wrap::before {{ left:0; background:linear-gradient(to right,var(--navy2),transparent); }}
    .ticker-wrap::after  {{ right:0; background:linear-gradient(to left,var(--navy2),transparent); }}
    .ticker {{ display:flex; gap:0; animation:ticker 30s linear infinite; width:max-content; }}
    .ticker:hover {{ animation-play-state:paused; }}
    @keyframes ticker {{ 0%{{transform:translateX(0)}} 100%{{transform:translateX(-50%)}} }}
    .school-chip {{ background:rgba(255,255,255,0.07); border:1px solid rgba(255,255,255,0.1); color:rgba(255,255,255,0.85); padding:10px 22px; border-radius:4px; font-size:0.85rem; white-space:nowrap; margin:6px 8px; transition:background 0.2s,color 0.2s; }}
    .school-chip:hover {{ background:var(--gold); color:var(--navy2); }}

    #experience {{ background:var(--cream); }}
    .timeline {{ position:relative; padding-left:32px; }}
    .timeline::before {{ content:''; position:absolute; left:0; top:8px; bottom:8px; width:2px; background:linear-gradient(to bottom,var(--gold),rgba(201,168,76,0.1)); }}
    .tl-item {{ position:relative; margin-bottom:44px; }}
    .tl-dot {{ position:absolute; left:-39px; top:6px; width:14px; height:14px; border-radius:50%; background:var(--gold); border:3px solid var(--cream); box-shadow:0 0 0 2px var(--gold); }}
    .tl-item.current .tl-dot {{ background:var(--navy); box-shadow:0 0 0 2px var(--navy); }}
    .tl-period {{ font-size:0.75rem; color:var(--gold); letter-spacing:1px; text-transform:uppercase; margin-bottom:6px; font-weight:600; }}
    .tl-role {{ font-family:'Playfair Display',serif; font-size:1.15rem; color:var(--navy); font-weight:700; }}
    .tl-org {{ color:var(--mid); font-size:0.9rem; margin:4px 0 10px; }}
    .tl-bullets {{ list-style:none; }}
    .tl-bullets li {{ color:var(--mid); font-size:0.9rem; line-height:1.7; padding-left:14px; position:relative; margin-bottom:4px; }}
    .tl-bullets li::before {{ content:'›'; position:absolute; left:0; color:var(--gold); font-size:1rem; }}

    #reviews {{ background:var(--white); }}
    .reviews-meta {{ display:flex; align-items:center; gap:24px; margin-bottom:48px; flex-wrap:wrap; }}
    .rating-big {{ font-family:'Playfair Display',serif; font-size:4rem; color:var(--navy); font-weight:700; line-height:1; }}
    .stars {{ color:var(--gold); font-size:1.4rem; letter-spacing:2px; }}
    .rating-meta {{ color:var(--mid); font-size:0.9rem; }}
    .reviews-grid {{ display:grid; grid-template-columns:repeat(auto-fill,minmax(300px,1fr)); gap:24px; }}
    .review-card {{ background:var(--cream); border-radius:8px; padding:28px; border:1px solid rgba(27,58,92,0.08); position:relative; overflow:hidden; transition:transform 0.2s,box-shadow 0.2s; }}
    .review-card:hover {{ transform:translateY(-4px); box-shadow:0 12px 40px rgba(27,58,92,0.12); }}
    .review-card::before {{ content:'"'; position:absolute; top:-10px; right:16px; font-family:'Playfair Display',serif; font-size:6rem; color:rgba(201,168,76,0.15); line-height:1; pointer-events:none; }}
    .review-stars {{ color:var(--gold); font-size:0.85rem; margin-bottom:12px; }}
    .review-text {{ color:var(--dark); font-size:0.9rem; line-height:1.7; font-style:italic; margin-bottom:16px; }}
    .review-author {{ color:var(--navy); font-weight:600; font-size:0.85rem; }}
    .review-context {{ color:var(--mid); font-size:0.78rem; margin-top:2px; }}
    .verified-badge {{ display:inline-block; background:#e8f5e9; color:#2e7d32; font-size:0.7rem; padding:2px 8px; border-radius:10px; margin-top:6px; font-weight:500; }}

    #skills {{ background:var(--cream); }}
    .skills-grid {{ display:grid; grid-template-columns:repeat(auto-fill,minmax(240px,1fr)); gap:20px; }}
    .skill-card {{ background:var(--white); border-radius:8px; padding:28px 24px; border:1px solid rgba(27,58,92,0.08); transition:box-shadow 0.2s; }}
    .skill-card:hover {{ box-shadow:0 8px 32px rgba(27,58,92,0.1); }}
    .skill-icon {{ font-size:2rem; margin-bottom:14px; }}
    .skill-title {{ font-weight:600; color:var(--navy); margin-bottom:8px; font-size:0.95rem; }}
    .skill-desc {{ color:var(--mid); font-size:0.85rem; line-height:1.6; }}

    #awards {{ background:var(--navy); padding:80px 48px; }}
    #awards .section-title {{ color:white; }}
    #awards .section-eyebrow {{ color:var(--gold); }}
    .awards-grid {{ display:grid; grid-template-columns:repeat(auto-fill,minmax(260px,1fr)); gap:20px; }}
    .award-card {{ background:rgba(255,255,255,0.06); border:1px solid rgba(255,255,255,0.1); border-radius:8px; padding:28px; transition:background 0.2s; }}
    .award-card:hover {{ background:rgba(255,255,255,0.1); }}
    .award-icon {{ font-size:1.8rem; margin-bottom:12px; }}
    .award-title {{ color:var(--gold); font-weight:600; font-size:0.95rem; margin-bottom:6px; }}
    .award-desc {{ color:rgba(255,255,255,0.6); font-size:0.85rem; line-height:1.6; }}

    #contact {{ background:var(--cream); }}
    .contact-grid {{ display:grid; grid-template-columns:1.2fr 1fr; gap:80px; align-items:start; }}
    .contact-item {{ display:flex; align-items:center; gap:16px; margin-bottom:24px; }}
    .contact-icon {{ width:44px; height:44px; border-radius:50%; background:var(--navy); display:flex; align-items:center; justify-content:center; font-size:1.1rem; flex-shrink:0; }}
    .contact-label {{ font-size:0.75rem; color:var(--mid); text-transform:uppercase; letter-spacing:1px; }}
    .contact-value {{ color:var(--navy); font-weight:500; font-size:0.95rem; text-decoration:none; }}
    .contact-value:hover {{ color:var(--gold); }}
    .resume-box {{ background:var(--navy); border-radius:8px; padding:40px; text-align:center; color:white; }}
    .resume-box p {{ color:rgba(255,255,255,0.7); font-size:0.9rem; margin:12px 0 24px; }}
    .resume-box h3 {{ font-family:'Playfair Display',serif; font-size:1.5rem; }}

    footer {{ background:var(--navy2); color:rgba(255,255,255,0.5); text-align:center; padding:28px 48px; font-size:0.8rem; }}
    footer span {{ color:var(--gold); }}

    .fade-up {{ opacity:0; transform:translateY(30px); transition:opacity 0.6s ease,transform 0.6s ease; }}
    .fade-up.visible {{ opacity:1; transform:translateY(0); }}

    .last-updated {{ display:inline-block; background:rgba(201,168,76,0.15); color:var(--gold); font-size:0.75rem; padding:4px 12px; border-radius:20px; margin-bottom:20px; border:1px solid rgba(201,168,76,0.3); }}

    @media(max-width:768px){{
      nav{{padding:14px 24px;}} .nav-links{{display:none;}}
      section{{padding:60px 24px;}} .hero{{padding:100px 24px 60px;}}
      .hero-inner{{grid-template-columns:1fr; gap:48px;}}
      .hero-stats{{grid-template-columns:repeat(2,1fr);}}
      .about-grid{{grid-template-columns:1fr;}} .about-left{{position:static;}}
      .contact-grid{{grid-template-columns:1fr;}}
      #awards{{padding:60px 24px;}} #schools .section-inner{{padding:0 24px;}}
    }}
    @media(prefers-reduced-motion:reduce){{
      .ticker{{animation:none;}} .fade-up{{opacity:1;transform:none;}}
    }}
  </style>
</head>
<body>

<nav>
  <div class="nav-logo">Shilpa Deol</div>
  <div class="nav-links">
    <a href="#about">About</a>
    <a href="#schools">Schools</a>
    <a href="#experience">Experience</a>
    <a href="#reviews">Reviews</a>
    <a href="#contact">Contact</a>
  </div>
</nav>

<section class="hero" id="home">
  <div class="hero-inner">
    <div>
      <span class="hero-tag">French Language Educator</span>
      <h1>Bonjour,<br>I'm <em>Shilpa Deol</em></h1>
      <p class="hero-sub">Over a decade of bringing French to life — from classrooms in Delhi to students in Dubai, Canada, Germany, and France. I teach the language, and the love of it.</p>
      <div class="hero-btns">
        <a href="#reviews" class="btn-primary">⭐ See Student Reviews</a>
        <a href="#contact" class="btn-outline">Get in Touch</a>
      </div>
    </div>
    <div class="hero-stats">
      <div class="stat-card">
        <span class="stat-num" data-count="{data['years_experience']}">0</span>
        <span class="stat-label">Years Teaching</span>
      </div>
      <div class="stat-card">
        <span class="stat-num" data-count="{data['students']}">0</span>
        <span class="stat-label">Students Taught</span>
      </div>
      <div class="stat-card">
        <span class="stat-num" data-count="{data['hours']}">0</span>
        <span class="stat-label">Hours of Classes</span>
      </div>
      <div class="stat-card">
        <span class="stat-num">{data['rating']}★</span>
        <span class="stat-label">UrbanPro Rating</span>
      </div>
    </div>
  </div>
</section>

<section id="about">
  <div class="section-inner">
    <div class="about-grid">
      <div class="about-left fade-up">
        <div class="about-photo-wrap">
          <img src="https://p.urbanpro.com/tv-prod/auth/photo/2285419-large.jpg" alt="Shilpa Deol" onerror="this.parentElement.style.background='#1B3A5C'"/>
          <div class="about-photo-badge">
            <strong>UrbanPro Certified Tutor</strong>
            <span>Excellence Award Winner 2024</span>
          </div>
        </div>
        <div class="links-row" style="margin-top:20px;">
          <a href="{data['profile_url']}" target="_blank" class="profile-link gold">UrbanPro Profile ↗</a>
          <a href="{data['linkedin_url']}" target="_blank" class="profile-link">LinkedIn ↗</a>
        </div>
      </div>
      <div class="about-body fade-up">
        <span class="last-updated">Last updated: {data['last_updated']}</span>
        <span class="section-eyebrow">About Me</span>
        <h2 class="section-title">Passionate about <span>French</span>, dedicated to every learner</h2>
        <p>I'm a French Language Educator with <strong>over {data['years_experience']} years of teaching experience</strong> across CBSE, IGCSE, and IB boards. My students range from Grade 4 schoolchildren to working professionals preparing for careers in French-speaking countries.</p>
        <p>What sets me apart is my ability to adapt — I have taught students from <strong>Canada, Germany, the UK, France, Switzerland, and Dubai</strong>, tailoring my approach to each learner's cultural background and goals.</p>
        <p>Currently based in Punjab, I am also a <strong>freelance educator on UrbanPro</strong> with {data['review_count']} verified reviews and a {data['rating']}-star rating. I use AI tools to create custom songs, storybooks, and interactive activities that make French genuinely enjoyable.</p>
        <div class="badges">
          <span class="badge">CBSE</span><span class="badge">IGCSE</span><span class="badge">IB</span>
          <span class="badge">DELF Prep</span><span class="badge">TEF Prep</span><span class="badge">A1 → B2</span>
          <span class="badge">AI-Enhanced Teaching</span><span class="badge">Corporate Training</span>
        </div>
      </div>
    </div>
  </div>
</section>

<section id="schools">
  <div class="section-inner">
    <span class="section-eyebrow">Student Reach</span>
    <h2 class="section-title" style="color:white;">Students from <span>{len(data['schools'])}+ top schools</span></h2>
    <p class="schools-intro">My students have come from some of India's and the world's most prestigious institutions.</p>
  </div>
  <div class="ticker-wrap">
    <div class="ticker">{schools_html}</div>
  </div>
</section>

<section id="experience">
  <div class="section-inner">
    <span class="section-eyebrow">Work History</span>
    <h2 class="section-title">A decade of <span>teaching excellence</span></h2>
    <div class="timeline">
      <div class="tl-item current fade-up">
        <div class="tl-dot"></div>
        <div class="tl-period">April 2025 — Present</div>
        <div class="tl-role">TGT French</div>
        <div class="tl-org">Doon International School, New Chandigarh</div>
        <ul class="tl-bullets">
          <li>Teaching French to Grades 4–9 aligned with CBSE curriculum</li>
          <li>Designing interactive, differentiated lesson plans</li>
          <li>Using AI tools to create songs, storybooks and language activities</li>
        </ul>
      </div>
      <div class="tl-item fade-up">
        <div class="tl-dot"></div>
        <div class="tl-period">December 2013 — Present</div>
        <div class="tl-role">Online French Educator (Freelance)</div>
        <div class="tl-org">UrbanPro · <a href="{data['profile_url']}" target="_blank" style="color:var(--gold);">View Profile ↗</a></div>
        <ul class="tl-bullets">
          <li>{data['students']} students taught across India and internationally</li>
          <li>{data['hours']}+ hours of classes · {data['rating']}★ rating · {data['review_count']} verified reviews</li>
          <li>IGCSE, IB, and CBSE curriculum; DELF B1/B2 exam preparation</li>
        </ul>
      </div>
      <div class="tl-item fade-up">
        <div class="tl-dot"></div>
        <div class="tl-period">August 2022 — October 2023</div>
        <div class="tl-role">TGT French</div>
        <div class="tl-org">Bal Bhavan Public School, Mayur Vihar</div>
      </div>
      <div class="tl-item fade-up">
        <div class="tl-dot"></div>
        <div class="tl-period">August 2021 — January 2024</div>
        <div class="tl-role">French Faculty</div>
        <div class="tl-org">British Express, Laxmi Nagar</div>
      </div>
      <div class="tl-item fade-up">
        <div class="tl-dot"></div>
        <div class="tl-period">December 2016 — May 2018</div>
        <div class="tl-role">French Faculty</div>
        <div class="tl-org">Binary Talk Institute</div>
      </div>
      <div class="tl-item fade-up">
        <div class="tl-dot"></div>
        <div class="tl-period">February 2015 — September 2015</div>
        <div class="tl-role">French Faculty</div>
        <div class="tl-org">Academy of British & Foreign Languages</div>
      </div>
    </div>
  </div>
</section>

<section id="reviews">
  <div class="section-inner">
    <span class="section-eyebrow">Student Testimonials</span>
    <h2 class="section-title">What my <span>students say</span></h2>
    <div class="reviews-meta">
      <div class="rating-big">{data['rating']}</div>
      <div>
        <div class="stars">★★★★★</div>
        <div class="rating-meta">{data['review_count']} verified reviews on UrbanPro</div>
        <div class="rating-meta" style="margin-top:4px;">UrbanPro Certified Tutor · Excellence Award 2024</div>
      </div>
      <a href="{data['profile_url']}" target="_blank" class="btn-primary" style="margin-left:auto;">All Reviews ↗</a>
    </div>
    <div class="reviews-grid">{reviews_html}</div>
  </div>
</section>

<section id="skills">
  <div class="section-inner">
    <span class="section-eyebrow">What I Bring</span>
    <h2 class="section-title">Skills & <span>Expertise</span></h2>
    <div class="skills-grid">
      <div class="skill-card fade-up"><div class="skill-icon">🇫🇷</div><div class="skill-title">French Language Mastery</div><div class="skill-desc">Fluent French educator teaching A1 to B2 levels. Expert in DELF & TEF exam preparation.</div></div>
      <div class="skill-card fade-up"><div class="skill-icon">📚</div><div class="skill-title">Multi-Board Expertise</div><div class="skill-desc">Deep experience with CBSE, IGCSE, and IB curriculum frameworks and assessment methods.</div></div>
      <div class="skill-card fade-up"><div class="skill-icon">🌍</div><div class="skill-title">International Teaching</div><div class="skill-desc">Taught students from Canada, Germany, UK, France, Switzerland, and Dubai with cultural adaptability.</div></div>
      <div class="skill-card fade-up"><div class="skill-icon">🤖</div><div class="skill-title">AI-Enhanced Teaching</div><div class="skill-desc">Using AI tools to create custom French songs, storybooks, and interactive activities for deeper engagement.</div></div>
      <div class="skill-card fade-up"><div class="skill-icon">🎯</div><div class="skill-title">Differentiated Learning</div><div class="skill-desc">Tailored lesson plans for school students, college learners, and working professionals at every level.</div></div>
      <div class="skill-card fade-up"><div class="skill-icon">🏆</div><div class="skill-title">Event & Project Design</div><div class="skill-desc">Organiser of French quizzes, offline Olympiads, cultural workshops and interdisciplinary school projects.</div></div>
    </div>
  </div>
</section>

<section id="awards">
  <div class="section-inner">
    <span class="section-eyebrow">Recognition</span>
    <h2 class="section-title">Achievements & <span>Development</span></h2>
    <div class="awards-grid">{awards_html}</div>
  </div>
</section>

<section id="contact">
  <div class="section-inner">
    <span class="section-eyebrow">Get in Touch</span>
    <h2 class="section-title">Let's <span>connect</span></h2>
    <div class="contact-grid">
      <div>
        <div class="contact-item"><div class="contact-icon">✉️</div><div><div class="contact-label">Email</div><a href="mailto:chandershilpa24@gmail.com" class="contact-value">chandershilpa24@gmail.com</a></div></div>
        <div class="contact-item"><div class="contact-icon">📞</div><div><div class="contact-label">Phone</div><a href="tel:+919899460324" class="contact-value">+91 98994 60324</a></div></div>
        <div class="contact-item"><div class="contact-icon">📍</div><div><div class="contact-label">Location</div><span class="contact-value">Punjab, India</span></div></div>
        <div class="contact-item"><div class="contact-icon">🔗</div><div><div class="contact-label">UrbanPro</div><a href="{data['profile_url']}" target="_blank" class="contact-value">View Profile & Reviews ↗</a></div></div>
        <div class="contact-item"><div class="contact-icon">💼</div><div><div class="contact-label">LinkedIn</div><a href="{data['linkedin_url']}" target="_blank" class="contact-value">linkedin.com/in/shilpa-chander ↗</a></div></div>
      </div>
      <div class="resume-box">
        <h3>Download My Resume</h3>
        <p>Full CV with work history, education, certifications, and declaration — ready to send to schools.</p>
        <a href="Shilpa_Deol_Resume.docx" download class="btn-primary" style="justify-content:center;">⬇ Download Resume (.docx)</a>
      </div>
    </div>
  </div>
</section>

<footer>
  <p>© 2026 <span>Shilpa Deol</span> · French Language Educator · Punjab, India · Last updated: {data['last_updated']}</p>
</footer>

<script>
  function animateCount(el, target, duration=1800) {{
    let start=0; const step=target/(duration/16);
    const tick=()=>{{ start=Math.min(start+step,target); el.textContent=Math.floor(start)+(el.dataset.suffix||''); if(start<target) requestAnimationFrame(tick); else el.textContent=target+(el.dataset.suffix||''); }};
    tick();
  }}
  const observer=new IntersectionObserver((entries)=>{{ entries.forEach(e=>{{ if(e.isIntersecting){{ e.target.classList.add('visible'); e.target.querySelectorAll('[data-count]').forEach(el=>animateCount(el,parseInt(el.dataset.count))); observer.unobserve(e.target); }} }}); }},{{threshold:0.1}});
  document.querySelectorAll('.fade-up').forEach(el=>observer.observe(el));
  window.addEventListener('load',()=>{{ document.querySelectorAll('.hero [data-count]').forEach(el=>animateCount(el,parseInt(el.dataset.count))); }});
</script>
</body>
</html>"""
    return html


def main():
    print(f"📖 Reading {DATA_FILE}...")
    data = load_data()

    print("🔨 Building site...")
    html = build(data)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(html)

    size = os.path.getsize(OUTPUT_FILE) / 1024
    print(f"✅ Generated {OUTPUT_FILE} ({size:.1f} KB)")
    print(f"\n📋 Site stats baked in:")
    print(f"   Rating     : {data['rating']} ★")
    print(f"   Reviews    : {data['review_count']}")
    print(f"   Students   : {data['students']}")
    print(f"   Hours      : {data['hours']}")
    print(f"   Schools    : {len(data['schools'])}")
    print(f"   Reviews    : {len(data['reviews'])} shown")
    print(f"\n🚀 Upload index.html to GitHub → your site is updated!")


if __name__ == "__main__":
    main()
