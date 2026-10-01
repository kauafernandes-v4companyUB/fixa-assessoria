import { section } from '../content'
import CtaButton from './CtaButton'
import Eyebrow from './Eyebrow'

export default function Hero() {
  const s = section('hero')
  return (
    <section id="topo" className="survey-lines bg-nevoa">
      <div className="mx-auto max-w-6xl px-4 py-16 sm:py-24">
        <div className="max-w-3xl">
          <Eyebrow>{s.eyebrow}</Eyebrow>
          <h1 className="text-4xl font-extrabold leading-tight sm:text-5xl">{s.headline}</h1>
          <p className="mt-6 text-xl text-tinta/90">{s.subheadline}</p>
          <div className="mt-8 flex flex-col gap-3 sm:flex-row">
            <CtaButton location="hero">{s.cta_primary}</CtaButton>
            <a href="#como-funciona" className="inline-flex items-center justify-center rounded-lg border-2 border-fixa px-6 py-4 font-display text-lg font-bold text-fixa transition-colors hover:bg-fixa hover:text-white">
              {s.cta_secondary}
            </a>
          </div>
        </div>
        <dl className="mt-14 grid gap-6 sm:grid-cols-3">
          {s.stats?.map((st) => (
            <div key={st.number} className="border-l-4 border-serra pl-4">
              <dt className="font-display text-3xl font-extrabold text-fixa">{st.number}</dt>
              <dd className="text-base text-grafite">{st.label}</dd>
            </div>
          ))}
        </dl>
      </div>
    </section>
  )
}
