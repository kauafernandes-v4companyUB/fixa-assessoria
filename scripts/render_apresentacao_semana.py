#!/usr/bin/env python3
"""render_apresentacao_semana.py — Deck separado (NAO cumulativo) para uma semana especifica.

Diferente de apresentacao.html (gerado por render_apresentacao.py do plugin, que cresce
progressivamente S1 -> S2 -> S3 -> S4), este script gera um arquivo a parte contendo SO os
slides da semana pedida, usando delivery-map.json (mesma fonte que o plugin ja usa) pra
decidir quais skills pertencem a qual semana.

Reaproveita os slide builders do plugin (shared-templates/render_apresentacao.py) pra cada
entrega, mas monta capa/pauta/fechamento proprios, escopados so na semana — nao lista nem
menciona entregas de outras semanas.

So mexe neste projeto (Fixa). Nao altera nada do plugin nem do apresentacao.html cumulativo.

Uso:
    python3 scripts/render_apresentacao_semana.py <client_dir> <semana_n> [--exclude skill1,skill2]

Ex:
    python3 scripts/render_apresentacao_semana.py clientes/fixa 2
    -> escreve clientes/fixa/apresentacao-semana-2.html

--exclude serve pro caso (como a Fixa) em que uma skill esta bucketizada numa semana no
delivery-map.json mas ja foi apresentada numa reuniao anterior por ter sido adiantada — nao
faz sentido repeti-la no deck desta semana. Ex: ee-s1-diagnostico-maturidade esta em
comum.semana_2 no delivery-map, mas na Fixa foi apresentada junto com a Semana 1 (Reuniao 1).
"""
import sys
import os

PLUGIN_SHARED = os.path.expanduser(
    "~/.claude/plugins/cache/v4-estruturacao-marketplace/v4-estruturacao-ia/0.1.0/shared-templates"
)
sys.path.insert(0, PLUGIN_SHARED)
import render_apresentacao as ra  # noqa: E402  (reusa builders, SHELL_HTML, helpers do plugin)


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
        <p class="subtitle-text" style="margin-top:24px; font-size:clamp(1.1rem, 1.5vw, 1.5rem);">
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


# slide_id (do SLIDE_PLAN do plugin) -> texto de pauta amigavel
PAUTA_LABELS = {
    "maturidade": "Maturidade digital — scores por pilar",
    "swot": "SWOT — forças, fraquezas, oportunidades, ameaças",
    "swot_cruzada": "SWOT cruzada — estratégias derivadas",
    "persona": "Persona — ICP e jornada",
    "auditoria_comm": "Auditoria de comunicação — gaps por canal",
    "pesquisa_mercado": "Pesquisa de mercado (TAM · SAM · SOM)",
    "concorrentes": "Concorrentes-chave",
    "posicionamento": "Posicionamento estratégico",
    "midia_atual": "Diagnóstico de mídia paga",
    "midia_cenarios": "Cenários de budget de mídia",
    "organico_comparativo": "Conteúdo orgânico — Instagram vs. concorrentes",
    "organico_padroes": "Padrões dos concorrentes que faltam explorar",
    "criativos": "Diagnóstico de criativos — briefing de produção",
    "cro_tecnico": "Diagnóstico técnico do site (CRO)",
    "cro_muros": "Principais gargalos de conversão",
}


def main():
    if len(sys.argv) < 3:
        print("Uso: render_apresentacao_semana.py <client_dir> <semana_n> [--exclude skill1,skill2]", file=sys.stderr)
        sys.exit(2)
    client_dir = sys.argv[1].rstrip("/")
    week_n = int(sys.argv[2])
    exclude = set()
    if "--exclude" in sys.argv:
        idx = sys.argv.index("--exclude")
        if idx + 1 < len(sys.argv):
            exclude = {s.strip() for s in sys.argv[idx + 1].split(",") if s.strip()}
    if not os.path.isdir(client_dir):
        print(f"Diretório não encontrado: {client_dir}", file=sys.stderr)
        sys.exit(2)

    client = ra.load_client(client_dir)
    outputs = ra.load_outputs(client_dir)
    dm = ra.load_delivery_map()
    if not dm:
        print("delivery-map.json não encontrado", file=sys.stderr)
        sys.exit(2)

    week_map = dict(ra.week_sequence(client, dm))
    week_skills = set(week_map.get(week_n, []))
    if not week_skills:
        print(f"Nenhuma skill mapeada pra Semana {week_n} em delivery-map.json", file=sys.stderr)
        sys.exit(1)

    # Filtra o SLIDE_PLAN do plugin: só os slides cuja skill pertence a ESTA semana
    # (ignora os genéricos cover/pauta/onde_estamos/proximos_passos/fechamento do
    # plugin — este script monta capa/pauta/fechamento próprios, escopados).
    filtered = [
        (slide_id, builder_name, required_skill)
        for slide_id, builder_name, required_skill in ra.SLIDE_PLAN
        if required_skill and required_skill in week_skills and required_skill not in exclude
    ]

    pauta_items = []
    slides_html = []
    for slide_id, builder_name, required_skill in filtered:
        if required_skill not in outputs:
            continue  # skill dessa semana ainda não completou — pula em silêncio
        builder = ra.BUILDERS.get(builder_name)
        if not builder:
            continue
        try:
            chunk = builder(client, outputs) or ""
        except Exception as e:
            sys.stderr.write(f"[apresentacao-semana] builder {builder_name} falhou: {e}\n")
            continue
        if chunk.strip():
            slides_html.append(chunk)
            pauta_items.append(PAUTA_LABELS.get(slide_id, slide_id))

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

    out_path = os.path.join(client_dir, f"apresentacao-semana-{week_n}.html")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html_out)
    print(f"Apresentação da Semana {week_n} gerada: {out_path} ({len(slides_html)} slides de entrega + capa/pauta/fechamento)")


if __name__ == "__main__":
    main()
