#!/usr/bin/env python3
"""render_apresentacao_semana.py — Deck separado (NAO cumulativo), condensado pra apresentação
ao vivo (Google Meet): fonte maior, sem scroll, uma ideia por slide.

Diferente de apresentacao.html (gerado por render_apresentacao.py do plugin, que cresce
progressivamente S1 -> S2 -> S3 -> S4 e reusa builders genericos pensados pra qualquer
cliente), este script:
  1) gera um arquivo a parte contendo SO os slides da semana pedida (via delivery-map.json);
  2) usa slide builders PROPRIOS, escritos pra caber numa tela sem rolar e com fonte legivel
     de longe — o detalhe fino (metodologia, numeros completos, contexto) fica no roteiro
     de reuniao (roteiro-reuniao-semana-N.html), nao no slide.

So mexe neste projeto (Fixa). Nao altera nada do plugin nem do apresentacao.html cumulativo.

Uso:
    python3 scripts/render_apresentacao_semana.py <client_dir> <semana_n>

Ex:
    python3 scripts/render_apresentacao_semana.py clientes/fixa 2
    -> escreve clientes/fixa/apresentacao-semana-2.html
"""
import sys
import os

PLUGIN_SHARED = os.path.expanduser(
    "~/.claude/plugins/cache/v4-estruturacao-marketplace/v4-estruturacao-ia/0.1.0/shared-templates"
)
sys.path.insert(0, PLUGIN_SHARED)
import render_apresentacao as ra  # noqa: E402  (reusa load_client/load_outputs/SHELL_HTML/etc.)


# ---------------------------------------------------------------------------
# Override de CSS — fonte maior e mais legivel numa tela compartilhada
# (Meet/projetor), aplicado só neste deck (nao mexe no CSS do plugin).
# ---------------------------------------------------------------------------
FONT_OVERRIDE_CSS = """
<style>
  /* Ajuste pra apresentação ao vivo: fonte maior, conteúdo condensado pra caber sem rolar. */
  h2.title-section { font-size: clamp(2.6rem, 5vw, 4.6rem); }
  .subtitle-text { font-size: clamp(1.5rem, 2vw, 2.1rem); line-height: 1.45; }
  .eyebrow { font-size: clamp(0.95rem, 1.1vw, 1.15rem); }
  .kpi__label { font-size: clamp(0.95rem, 1.1vw, 1.15rem); }
  .kpi__value { font-size: clamp(2.4rem, 3.6vw, 3.4rem) !important; }
  .kpi__hint { font-size: clamp(1.1rem, 1.3vw, 1.35rem); line-height: 1.4; }
  ul.bullets li { font-size: clamp(1.25rem, 1.5vw, 1.55rem); padding: 10px 0 10px 30px; }
  .highlight-box__label { font-size: 0.9rem; }
  .highlight-box__text { font-size: clamp(1.35rem, 1.7vw, 1.85rem); line-height: 1.45; }
  .compare th { font-size: 0.95rem; }
  .compare th, .compare td { font-size: clamp(1.2rem, 1.4vw, 1.5rem); padding: 16px 16px; }
  .pattern-card__title { font-size: clamp(1.15rem, 1.35vw, 1.4rem); font-weight: 700; color: #ffd0a8; margin-bottom: 10px; line-height: 1.3; }
  .pattern-card__body { font-size: clamp(1.05rem, 1.2vw, 1.25rem); line-height: 1.4; color: rgba(255,245,230,0.95); }
  .pattern-card__tag { display:inline-block; font-size:0.8rem; font-weight:700; text-transform:uppercase; letter-spacing:.05em; color:#ffd0a8; background:rgba(255,208,168,0.15); border-radius:100px; padding:3px 12px; margin-bottom:12px; }
</style>
</head>"""


def build_cover_semana(client, week_n):
    name = client.get("meta", {}).get("name", "Cliente")
    parts = name.split()
    title = f"{parts[0]}<br/>{' '.join(parts[1:])}" if len(parts) > 1 else name
    return f"""
    <section class="slide slide--alt">
      {ra.LOGO}
      <div class="slide__content" style="justify-content:center;">
        <span class="eyebrow">Diagnóstico Estratégico</span>
        <h1 class="title-mega">{title}</h1>
        <p class="subtitle-text" style="margin-top:24px;">
          Estruturação V4 · Semana {week_n}
        </p>
      </div>
      <div class="slide__footer">
        <span>Reunião de acompanhamento</span>
        <span>V4 Company · Estruturação Estratégica</span>
      </div>
      <div class="deco-square deco-s1"></div>
      <div class="deco-square deco-s2"></div>
    </section>
    """


def build_pauta_semana(week_n, week_items):
    if not week_items:
        return ""
    mid = (len(week_items) + 1) // 2
    col1 = "".join(f'<div class="pill">{i + 1} · {ra.esc(t)}</div>' for i, t in enumerate(week_items[:mid]))
    col2 = "".join(f'<div class="pill">{mid + i + 1} · {ra.esc(t)}</div>' for i, t in enumerate(week_items[mid:]))
    return f"""
    <section class="slide">
      {ra.LOGO}
      <div class="slide__content" style="justify-content:center;">
        <span class="eyebrow">Pauta de hoje · Semana {week_n}</span>
        <h2 class="title-section">O que vamos cobrir</h2>
        <div class="row-2" style="margin-top:3vh;">
          <div class="stack">{col1}</div>
          <div class="stack">{col2}</div>
        </div>
      </div>
    </section>
    """


def build_posicionamento_slide(client, outputs):
    d = outputs.get("ee-s2-posicionamento")
    if not d:
        return ""
    tagline = d.get("recommended_tagline") or "—"
    territory = (d.get("brand_territory") or {}).get("three_words") or []
    puv_short = (
        "A Fixa resolve engenharia e a parte jurídica da regularização em um único "
        "processo — sem contratar dois prestadores — com 10 anos de relacionamento "
        "direto com cartórios e prefeitura."
    )
    pills = "".join(
        f'<span class="pill" style="font-size:clamp(1.1rem,1.5vw,1.5rem); padding:14px 32px; '
        f'background:rgba(255,225,180,0.18); border-color:rgba(255,225,180,0.4);">{ra.esc(w)}</span>'
        for w in territory[:3]
    )
    return f"""
    <section class="slide slide--soft">
      {ra.LOGO}
      <div class="slide__content">
        <span class="eyebrow">Posicionamento aprovado</span>
        <h2 class="title-section">Como vamos ser percebidos</h2>
        <div style="margin:2.5vh 0; text-align:center;">
          <div style="display:inline-flex; gap:14px; flex-wrap:wrap; justify-content:center;">{pills}</div>
        </div>
        <div class="row-2" style="gap:18px; flex:1;">
          <div class="glass" style="display:flex; flex-direction:column; justify-content:center;">
            <div class="highlight-box__label">PUV</div>
            <p style="font-weight:600; font-size:clamp(1.3rem,1.7vw,1.75rem); line-height:1.4; color:#fff; margin-top:10px;">
              {ra.esc(puv_short)}
            </p>
          </div>
          <div class="glass" style="display:flex; flex-direction:column; justify-content:center;">
            <div class="highlight-box__label">Tagline aprovada</div>
            <h3 style="font-weight:700; font-size:clamp(2rem, 3vw, 2.8rem); color:#fff; margin-top:10px; line-height:1.15;">
              {ra.esc(tagline)}
            </h3>
          </div>
        </div>
      </div>
    </section>
    """


def build_midia_ponto_partida_slide(client, outputs):
    d = outputs.get("ee-s2-diagnostico-midia")
    if not d:
        return ""
    cm = d.get("current_metrics") or {}
    scenarios = d.get("budget_reallocation_scenarios") or {}
    b = scenarios.get("scenario_b_realistic") or {}
    key_insight = (d.get("key_insight") or {}).get("headline") or d.get("summary_headline", "")

    invest = cm.get("total_investment")
    leads = cm.get("total_leads")
    budget_b = b.get("total_budget_monthly")
    cpl_b = b.get("expected_cpl")

    kpis = [
        ("Investimento hoje", ra.fmt_brl(invest) if invest is not None else "R$ 0", "0 campanhas ativas (90d)"),
        ("Leads hoje", str(leads) if leads is not None else "0", "Nunca rodou mídia paga"),
        ("Budget de lançamento", ra.fmt_brl(budget_b) if budget_b is not None else "—", "Cenário B · recomendado"),
        ("CPL alvo", ra.fmt_brl(cpl_b) if cpl_b is not None else "—", "Após LP + CRM prontos"),
    ]
    kpi_html = "".join(f"""
          <div class="glass">
            <div class="kpi__label">{ra.esc(label)}</div>
            <div class="kpi__value">{ra.esc(value)}</div>
            <div class="kpi__hint">{ra.esc(hint)}</div>
          </div>""" for label, value, hint in kpis)

    return f"""
    <section class="slide slide--diag">
      {ra.LOGO}
      <div class="slide__content">
        <span class="eyebrow">Mídia paga · ponto de partida</span>
        <h2 class="title-section">Plano de lançamento, não otimização</h2>
        <div class="row-4" style="margin-top:2vh;">{kpi_html}</div>
        <div class="highlight-box" style="margin-top:3vh;">
          <div class="highlight-box__label">Leitura V4</div>
          <div class="highlight-box__text">{ra.esc(ra.truncate(key_insight, 180))}</div>
        </div>
      </div>
    </section>
    """


def build_midia_cenarios_slide(client, outputs):
    d = outputs.get("ee-s2-diagnostico-midia")
    if not d:
        return ""
    scenarios = d.get("budget_reallocation_scenarios")
    if not isinstance(scenarios, dict):
        return ""
    cards = []
    for key, label in [
        ("scenario_a_conservative", "A · Conservador"),
        ("scenario_b_realistic", "B · Recomendado"),
        ("scenario_c_aggressive", "C · Agressivo"),
    ]:
        sc = scenarios.get(key)
        if not isinstance(sc, dict):
            continue
        total = sc.get("total_budget_monthly")
        leads = sc.get("expected_leads_monthly")
        cpl = sc.get("expected_cpl")
        is_reco = "realistic" in key
        border = "border: 2px solid rgba(255,208,168,0.4);" if is_reco else ""
        color = "color:#ffd0a8;" if is_reco else ""
        total_fmt = f"R$ {int(total):,}".replace(",", ".") if isinstance(total, (int, float)) else str(total or "—")
        hint = f"~{leads} leads/mês · CPL {ra.fmt_brl(cpl)}" if leads else ""
        cards.append(f"""
          <div class="glass" style="{border}">
            <div class="kpi__label" style="{color}">Cenário {ra.esc(label)}</div>
            <div class="kpi__value" style="{color}">{ra.esc(total_fmt)}<span style="font-size:1rem; opacity:0.6">/mês</span></div>
            <div class="kpi__hint" style="margin-top:8px;">{ra.esc(hint)}</div>
          </div>""")
    if not cards:
        return ""
    return f"""
    <section class="slide">
      {ra.LOGO}
      <div class="slide__content">
        <span class="eyebrow">Mídia paga · cenários de lançamento</span>
        <h2 class="title-section">Quanto investir quando o funil estiver pronto</h2>
        <div class="row-{len(cards)}" style="margin-top:3vh;">{''.join(cards)}</div>
        <div class="highlight-box" style="margin-top:3vh;">
          <div class="highlight-box__label">Recomendação V4</div>
          <div class="highlight-box__text">Cenário B — dá volume pra sair da fase de aprendizado do algoritmo sem comprometer caixa.</div>
        </div>
      </div>
    </section>
    """


def build_organico_comparativo_slide(client, outputs):
    d = outputs.get("ee-s2-diagnostico-organico-ig")
    if not d:
        return ""
    me = d.get("client_account") or {}
    comps = d.get("competitor_accounts") or []
    cadence_by_user = {r["username"]: r for r in (d.get("cadence") or {}).get("by_account", []) if isinstance(r, dict) and r.get("username")}
    eng_by_user = {r["username"]: r for r in (d.get("engagement_benchmark") or {}).get("by_account", []) if isinstance(r, dict) and r.get("username")}

    def _row(acc, is_me=False):
        u = acc.get("username", "")
        eng = eng_by_user.get(u, {})
        cad = cadence_by_user.get(u, {})
        followers = acc.get("followers_count")
        engagement = eng.get("avg_engagement_proxy")
        eng_str = f"{float(engagement):.2f}%" if engagement is not None else "—"
        fol_str = f"{int(followers):,}".replace(",", ".") if followers is not None else "—"
        posts_str = f"{float(cad.get('posts_per_week')):.2f}".replace(".", ",") if cad.get("posts_per_week") is not None else "—"
        row_style = 'style="background:rgba(255,225,180,0.12);"' if is_me else ""
        name_cell = f'<td class="strong">@{ra.esc(u)} (você)</td>' if is_me else f'<td>@{ra.esc(u)}</td>'
        eng_cell = f'<td class="accent-cell">{ra.esc(eng_str)}</td>' if is_me else f'<td>{ra.esc(eng_str)}</td>'
        return f"<tr {row_style}>{name_cell}<td>{ra.esc(fol_str)}</td><td>{ra.esc(posts_str)}</td>{eng_cell}</tr>"

    rows = [_row(me, is_me=True)] + [_row(c) for c in comps[:2] if isinstance(c, dict)]

    return f"""
    <section class="slide slide--diag">
      {ra.LOGO}
      <div class="slide__content">
        <span class="eyebrow">Conteúdo orgânico · Instagram</span>
        <h2 class="title-section">Você vs. concorrentes (90 dias)</h2>
        <table class="compare" style="margin-top:2.5vh;">
          <thead><tr><th>Conta</th><th>Seguidores</th><th>Posts/sem</th><th>Engajamento</th></tr></thead>
          <tbody>{''.join(rows)}</tbody>
        </table>
        <div class="highlight-box" style="margin-top:3vh;">
          <div class="highlight-box__label">Leitura V4</div>
          <div class="highlight-box__text">Fixa tem o maior engajamento das 3 contas — mesmo com menos seguidores que Balen e DCA.</div>
        </div>
      </div>
    </section>
    """


def build_organico_padroes_slide(client, outputs):
    d = outputs.get("ee-s2-diagnostico-organico-ig")
    if not d:
        return ""
    missing = d.get("competitor_patterns_missing") or []
    if not missing:
        return ""
    short_titles = {
        0: "Legenda curta + número na 1ª linha",
        1: "Relacionamento institucional como conteúdo",
        2: "Geolocalização do case no texto",
        3: "Presença em eventos do setor",
    }
    short_bodies = {
        0: "Prova social nos primeiros segundos, sem exigir leitura longa.",
        1: "Fixa tem o mesmo ativo (10 anos) — nunca mostrou. Gap mais barato de fechar.",
        2: "Reforça relevância local imediata pra quem mora no bairro.",
        3: "Mostra atividade de mercado e networking.",
    }
    cards = []
    for i, p in enumerate(missing[:3]):
        if not isinstance(p, dict):
            continue
        who = ", ".join(p.get("seen_in_competitors") or []) or "concorrente"
        cards.append(f"""
          <div class="glass" style="padding:22px;">
            <span class="pattern-card__tag">visto em {ra.esc(who)}</span>
            <div class="pattern-card__title">{ra.esc(short_titles.get(i, ra.truncate(p.get('pattern', ''), 50)))}</div>
            <p class="pattern-card__body">{ra.esc(short_bodies.get(i, ra.truncate(p.get('why_works', ''), 100)))}</p>
          </div>""")
    if not cards:
        return ""
    return f"""
    <section class="slide slide--alt">
      {ra.LOGO}
      <div class="slide__content">
        <span class="eyebrow">Conteúdo orgânico · gaps</span>
        <h2 class="title-section">Padrões dos concorrentes que faltam explorar</h2>
        <div class="row-3" style="margin-top:3vh; gap:16px; flex:1;">{''.join(cards)}</div>
      </div>
    </section>
    """


def build_criativos_slide(client, outputs):
    d = outputs.get("ee-s2-diagnostico-criativos")
    if not d:
        return ""
    pb = d.get("production_briefing") or {}
    if not pb:
        return ""
    format_labels = {
        "stories_vertical": "Stories vertical", "feed_quadrado": "Feed quadrado",
        "carrossel": "Carrossel", "video_curto": "Vídeo curto",
        "video_longo": "Vídeo longo", "reels": "Reels",
    }
    fmt = format_labels.get(pb.get("priority_format"), pb.get("priority_format") or "—")
    qty = pb.get("recommended_quantity")

    kpi_html = f"""
          <div class="glass">
            <div class="kpi__label">Formato prioritário</div>
            <div class="kpi__value">{ra.esc(fmt)}</div>
            <div class="kpi__hint">Primeiro lote de anúncios</div>
          </div>
          <div class="glass">
            <div class="kpi__label">Criativos recomendados</div>
            <div class="kpi__value">{ra.esc(qty) if qty is not None else '—'}</div>
            <div class="kpi__hint">3 hooks × 2 formatos × 2 CTAs</div>
          </div>"""

    avoid_short = ["Banco de imagens", "Jargão jurídico sem tradução", "Qualquer menção a prazo/data"]
    avoid_html = "".join(f"<li>{ra.esc(a)}</li>" for a in avoid_short)

    key_insight = (d.get("key_insight") or {}).get("headline") or d.get("summary_headline", "")

    return f"""
    <section class="slide">
      {ra.LOGO}
      <div class="slide__content">
        <span class="eyebrow">Criativos · briefing de produção</span>
        <h2 class="title-section">Pronto pra Semana 3</h2>
        <div class="row-2" style="margin-top:2vh;">{kpi_html}</div>
        <div class="glass" style="margin-top:2vh; border-left:3px solid #ff8080;">
          <h3 class="subtitle" style="color:#ff9c9c; margin-bottom:10px; font-size:1.3rem;">Evitar</h3>
          <ul class="bullets">{avoid_html}</ul>
        </div>
        <div class="highlight-box" style="margin-top:2.5vh;">
          <div class="highlight-box__label">Leitura V4</div>
          <div class="highlight-box__text">{ra.esc(ra.truncate(key_insight, 170))}</div>
        </div>
      </div>
    </section>
    """


# slide_id -> (builder, required_skill, pauta_label)
WEEK2_SLIDES = [
    ("posicionamento", build_posicionamento_slide, "ee-s2-posicionamento", "Posicionamento estratégico"),
    ("midia_ponto_partida", build_midia_ponto_partida_slide, "ee-s2-diagnostico-midia", "Diagnóstico de mídia paga"),
    ("midia_cenarios", build_midia_cenarios_slide, "ee-s2-diagnostico-midia", "Cenários de budget de mídia"),
    ("organico_comparativo", build_organico_comparativo_slide, "ee-s2-diagnostico-organico-ig", "Orgânico — Instagram vs. concorrentes"),
    ("organico_padroes", build_organico_padroes_slide, "ee-s2-diagnostico-organico-ig", "Orgânico — padrões que faltam explorar"),
    ("criativos", build_criativos_slide, "ee-s2-diagnostico-criativos", "Diagnóstico de criativos"),
]


def main():
    if len(sys.argv) < 3:
        print("Uso: render_apresentacao_semana.py <client_dir> <semana_n>", file=sys.stderr)
        sys.exit(2)
    client_dir = sys.argv[1].rstrip("/")
    week_n = int(sys.argv[2])
    if not os.path.isdir(client_dir):
        print(f"Diretório não encontrado: {client_dir}", file=sys.stderr)
        sys.exit(2)

    client = ra.load_client(client_dir)
    outputs = ra.load_outputs(client_dir)

    # Semana 2 é hardcoded aqui (WEEK2_SLIDES) porque os builders são escritos à mão,
    # condensados pra caber numa tela sem rolar — não são genéricos como os do plugin.
    # Pra Semana 3+, escrever o WEEK3_SLIDES equivalente quando os outputs existirem.
    if week_n != 2:
        print(f"Semana {week_n} ainda não tem builders condensados neste script — só Semana 2 por enquanto.", file=sys.stderr)
        sys.exit(1)

    pauta_items = []
    slides_html = []
    for slide_id, builder, required_skill, pauta_label in WEEK2_SLIDES:
        if required_skill not in outputs:
            continue
        chunk = builder(client, outputs) or ""
        if chunk.strip():
            slides_html.append(chunk)
            pauta_items.append(pauta_label)

    if not slides_html:
        print(f"Nenhum output completo encontrado pra Semana {week_n} ainda.", file=sys.stderr)
        sys.exit(1)

    cover = build_cover_semana(client, week_n)
    pauta = build_pauta_semana(week_n, pauta_items)
    fechamento = ra.build_fechamento(client, outputs)

    all_slides = "\n".join([cover, pauta] + slides_html + [fechamento])
    name = client.get("meta", {}).get("name", "Cliente")
    title = f"{name} · Diagnóstico Estratégico · Semana {week_n}"
    total_slides = all_slides.count('<section class="slide')
    html_out = ra.SHELL_HTML.format(title=ra.esc(title), slides=all_slides, total_slides=total_slides)
    html_out = html_out.replace("__LOGO_URI__", ra._logo_data_uri())
    html_out = html_out.replace("</style>\n</head>", "</style>" + FONT_OVERRIDE_CSS)

    out_path = os.path.join(client_dir, f"apresentacao-semana-{week_n}.html")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html_out)
    print(f"Apresentação da Semana {week_n} gerada: {out_path} ({len(slides_html)} slides de entrega + capa/pauta/fechamento)")


if __name__ == "__main__":
    main()
