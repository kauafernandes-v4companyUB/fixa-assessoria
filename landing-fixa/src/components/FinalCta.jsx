import { section } from '../content'
import CtaButton from './CtaButton'
import Eyebrow from './Eyebrow'

export default function FinalCta() {
  const s = section('final_cta')
  return (
    <section id="contato" className="survey-lines scroll-mt-20 bg-fixa">
      <div className="mx-auto max-w-3xl px-4 py-20 text-center">
        <Eyebrow light>{s.eyebrow}</Eyebrow>
        <h2 className="text-3xl font-extrabold leading-tight text-white sm:text-4xl">{s.headline}</h2>
        <p className="mx-auto mt-4 max-w-xl text-white/85">{s.subheadline}</p>
        <CtaButton location="cta_final" variant="light" className="mt-8">{s.cta_primary}</CtaButton>
      </div>
    </section>
  )
}
